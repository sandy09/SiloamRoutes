"""
DEVELOPED BY SANDRA GARCIA LAMADRID
LAST UPDATED SEPTEMBER 25 2017
UNIVERSITY OF LIVERPOOL MSC PROJECT

The source library holds all the main and basic fuctions to be called from the options, most 
of the functions here are in charge of extracting data from servers and formatting data.

"""

import urllib, json
import folium
import gpxpy 
import gpxpy.gpx
import geopy
from geopy.geocoders import Nominatim
import plotly
import pandas as pd
import osmread
from osgeo import ogr
import shapely
from shapely.geometry import *
import webbrowser
import string
import math
import sys


reload(sys)
sys.setdefaultencoding('utf8')

#Gets a pair of latitude and longitude an converts it into a string anddress (returns a string)
def getaddress (lat, lng):
	try:
		geolocator = Nominatim()
		coord = lat + "," + lng
		address = geolocator.reverse(coord)
		address = str(address)
		address = address.split(",")
		address = str(address[0]) + ',' + str(address[1])
	except:
		address = "No found"

	return address

#Extract the gpx from the GraphHopper API from one point to another
def getgpxfile(lat, lng, lat2, lng2):

	try:
		
		#Set API credentials
		gh_key = "344c6bbd-b560-4ed8-9e2d-fe1c43cfd85a"
		gh_url = "https://graphhopper.com/api/1/route?point=" + str(lat) + "%2C" + str(lng) + "&point=" + str(lat2) + "%2C" + str(lng2) + "&vehicle=foot&locale=en&type=gpx&gpx.waypoints=true&key=" + gh_key

		testfile = urllib.URLopener()
		testfile.retrieve(gh_url, "instructions.gpx")

		#Saves and parse the gpx file
		gpx_file = open('instructions.gpx', 'r') 
		gpx=gpxpy.parse(gpx_file)
		return gpx, testfile
		
	except:
		sys.exit('Error extracting the gpx file')

#Gets the osm file from the Open Street Maps API
def getosmfeatures ():

	try:
		#Define bounding box, the area was defined in coordination with supervisor 
		minlng=str(-2.968712)
		maxlng=str(-2.957078)
		minlat=str(53.393565) 
		maxlat=str(53.408164)

		mapfile = urllib.URLopener()
		#Saves osm file in working directory 
		mapfile.retrieve("http://api.openstreetmap.org/api/0.6/map?bbox=" + minlng + "," + minlat +
		"," + maxlng + "," + maxlat, "map.osm")
		
	except:
		sys.exit('Error extracting the osm file')


#Gets the obstacle database, update couchbase and returns an obstacle dataframe as output 
def getcbfeatures():
	try:
		
		#Open JSON file (output from SiloamLearn)
		json_file = open("dummy_database_N1QL_output.json")
		database = json.load(json_file)

		#Update couchbase database for simplicity purposes don't
		#cb = Bucket('couchbase://localhost/testing')
		#counter = 0
		#for feature in database: 
		#	cb.upsert('u:feature' + str(counter), feature['Dummy_SiloamLearn'])
		#	counter = counter + 1	

		#Create pandas df to merge with amenities data frame
		index = range(0,len(database))
		columns = ['Name','Amenity','geometry', 'lng', 'lat']
		df_ = pd.DataFrame(index=index, columns=columns)
		df_ = df_.fillna(0) # Fill df with 0s and then fill values
		i = 0
		
		#Get obstacle category
		for feature in database: 
			df_.loc[i, 'Name'] = feature['Dummy_SiloamLearn']['category'] #Could be the bustop number for example (in this case we don't have so we keep category)
			i = i + 1
		i = 0

		#Create obstacle dataframe to merge with the amenities dataframe 
		for feature in database: 
			df_.loc[i, 'Amenity'] = feature['Dummy_SiloamLearn']['category']
			df_.loc[i, 'lng'] = feature['Dummy_SiloamLearn']['geo']['long']
			df_.loc[i, 'lat'] = feature['Dummy_SiloamLearn']['geo']['lat']  
			df_.loc[i, 'geometry'] = 'obstacle'
			i = i + 1

		#Return obstacle database
		return df_
	except:
		sys.exit('Error in the Couchbase DataFrame')

#Create the amenities database		
def getAmenities():
	try: 

		#Extract the osm file from the Open Street Maps API
		getosmfeatures()
		driver=ogr.GetDriverByName('OSM')
		map_data = driver.Open('map.osm')
		layer = map_data.GetLayer('points')
		features=[x for x in layer]

		#Analyze data and filter amenities to hold only ('cafe','pub','bar','restaurant', 'fast_food') 
		#as defined in the project specifications, this settings can be adjusted to show other amenities
		data_list=[]
		for feature in features:
		    map_data=feature.ExportToJson(as_object=True)
		    coords=map_data['geometry']['coordinates']
		    shapely_geo=Point(coords[0],coords[1])
		    am_lat=coords[1]
		    am_lng=coords[0]
		    name=map_data['properties']['name']
		    other_tags=map_data['properties']['other_tags']
		    if other_tags and 'amenity' in other_tags:
		        feat=[x for x in other_tags.split(',') if 'amenity' in x][0]
		        amenity=feat[feat.rfind('>')+2:feat.rfind('"')]
		    else:
		        amenity=None
		    data_list.append([name,amenity,shapely_geo, am_lng, am_lat])
		gdf=pd.DataFrame(data_list,columns=['Name','Amenity','geometry', 'lng', 'lat'])
		bb_amenities=gdf[gdf.Amenity.isin(['cafe','pub','bar','restaurant', 'fast_food'])]
		bb_amenities = pd.DataFrame(bb_amenities)		
		return bb_amenities
	except:
		 sys.exit('Error extracting the Amenities')

#Merge obstacle and amenities dataframes
def concatFeatures():
	features = getosmfeatures()
	bb_amenities = getAmenities()
	obstacles_df = getcbfeatures()
	frames = [bb_amenities, obstacles_df]
	allFeatures = pd.concat(frames)
	return allFeatures

#Defines the output text for the feature category
def function(x):
    return {
        'steps': 'There are steps at your',
        'door': 'There is a door at your',
        'crossing': 'There is a crossing at your',
        'bus stop':'There is a bus stop at your'

    }.get(x, "There is an obstacle at your") 

#Recieves two consecutive route points and define the turning direction for the instruction
def getTurnDirection(direction1 , direction2):
	try:
		if (direction1 == 'N'):
			if (direction2 == 'E'):
				return 'Turn right'
			else:
				return 'Turn left'
		elif (direction1 == 'S'): 
			if (direction2 == 'E'):
				return 'Turn left'
			else:
				return 'Turn right'
		elif (direction1 == 'W'):
			if (direction2 == 'N'):
				return 'Turn right'
			else:
				return 'Turn left'
		else:
			if (direction2 == 'N'):
				return 'Turn left'
			else:
				return 'Turn right'

	except:
		sys.exit('Error gettiing turning directions')

#Calculates the great circle distance between two points on Earth
def getDistanceToLocation(lon1, lat1, lon2, lat2):
	try:
	   # Cnvert decimal degrees to radians 
	    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

	    #Haversine formula 
	    dlon = lon2 - lon1 
	    dlat = lat2 - lat1 
	    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
	    c = 2 * math.asin(math.sqrt(a)) 
	    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
	    distance = c *r
	    return distance

	except:
		sys.exit('Error gettiing distance to locations')

    


