from flask import Flask,request,render_template 
app = Flask(__name__)
import requests
import pandas as pd
import googlemaps
import gmplot
import webbrowser
import os
import urllib.request as urllib2
import json
READ_API_KEY='RSM668VKEAVTD39O'
CHANNEL_ID= '2329603'

def reverse_geocode(api_key, latitude, longitude):
    gmaps = googlemaps.Client(key=api_key)
    reverse_geocode_result = gmaps.reverse_geocode((latitude, longitude))
    return reverse_geocode_result

def get_multiple_routes(api_key, origin, destination, num_routes=3):
    # Create the URL for the Google Maps Directions API with multiple routes
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "alternatives": "true",  # Request multiple routes
    }

    # Send a request to the Google Maps API
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        routes = data["routes"]
        
        # Limit the number of routes if requested
        if num_routes < len(routes):
            routes = routes[:num_routes]
        
        # Extract locations for each route
        locations_per_route = []
        for route in routes:
            locations = []
            for step in route["legs"][0]["steps"]:
                locations.append(step["end_location"])
            locations_per_route.append(locations)
        
        return locations_per_route
    else:
        print("Error: Unable to fetch directions.")
        return []




@app.route("/",methods=["GET","POST"])
def home():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method=='POST':
        file_path='dbGenerate.py'
        os.system(f'python {file_path}')
        origin = str(request.form.get("origin"))
        destination = str(request.form.get("destination"))
        print(origin + " "+ destination)
        
        api_key = "AIzaSyCqUmmHsIHVV2pDO7mQVbYUBmpr1YdUZFM"
        num_routes = 4
        routes_with_locations = get_multiple_routes(api_key, origin, destination, num_routes)
            # Print locations for each route
        formatted_address=''
        formatted_address2=''
        for i, locations in enumerate(routes_with_locations):
            
            df = pd.read_csv('file1.csv')
            my_dict = dict(zip(df.Locations,df.score))
            formatted_address += "<br/><table bgcolor='white' border=5 style='font-size:14px;'><tr><td>Route :"+str((i+1))+"</td></tr>"
            formatted_address2 +="<br/><br/>Route :"+str((i+1))
            Latitude_list=[]
            Longitude_list=[]
            gmap3 = gmplot.GoogleMapPlotter(12.9716, 77.5946,80) 
            for idx, location in enumerate(locations):
                
                formatted_address += '<br/><tr><td>Step '+ str((idx+1)) +"  "+"Latitude:"+str(location['lat'])+" "+"Longitude"+str(location['lng'])+"<br/><ol>"
                Latitude_list.append(location['lat'])
                Longitude_list.append(location['lng'])
                results = reverse_geocode(api_key, location['lat'], location['lng'])
                if results:
                    for result in results[:-3]:
                        formatted_address += "<li>"+result['formatted_address']+"</li><br/>"
                    
                else:
                    print("No results found")
                formatted_address += "</ol></td></tr><br/>"
            gmap3.plot(Latitude_list, Longitude_list,'cornflowerblue', edge_width = 5.5) 
            gmap3.draw( "my_map"+str(i+1)+".html" )
            file_path="my_map"+str(i+1)+".html"
            webbrowser.open_new(f'file://{os.path.realpath(file_path)}') 
            route_score=0
            for key in my_dict:
                if key in formatted_address:
                    route_score += my_dict[key]
            formatted_address += "<br/><h2>" + "Route Pollution Score = "+str(route_score)+ "<br/>" + "Number of steps = "+str(idx+1)+"</h2><br/><br/>"
            formatted_address2 += "<br/>" + "Route Pollution Score = "+str(route_score)+ "<br/>" + "Number of steps = "+str(idx+1)+"<br/><br/>"
            
        return "<html><body bgcolor='cyan' style='font-weight:bold,font-size:14px'><h1>View Routes with their Pollution Scores</h1><br/><h2>Origin: "+origin+"</h2><br/>"+"<h2>Destination :"+destination+"</h2><br/>"+formatted_address+'</body></html>'

@app.route("/get_data",methods=["GET","POST"])
def data_from_cloud():
    data=""
    if request.method=='POST':
        TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))

        response = TS.read()
        data=json.loads(response)   
        TS.close()
        air_str= "<body bgcolor=cyan style='font-weight:bold;font-size:large;'><center><p style='text-align:left;width:40%;border:3px double blue;background-color:white;'> Timestamp &nbsp;"+data['created_at'] +"<br/><br/> Temperature &nbsp;"+data['field1']+"<br/><br/> Humidity &nbsp;"+data['field2']+"<br/><br/> Concentration of CO2( in PPM) &nbsp;"+data['field3']+"<br/><br/> Concentration of CO( in PPM) &nbsp;"+data['field4']+"<br/><br/> Concentration of NH3( in PPM) &nbsp;"+data['field5']+"<br/><br/> Air Quality Index &nbsp;"+data['field6']+"</p></center></body>"
        return air_str
    return(str(data))
        
