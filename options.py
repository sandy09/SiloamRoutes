"""
DEVELOPED BY SANDRA GARCIA LAMADRID
LAST UPDATED SEPTEMBER 25 2017
UNIVERSITY OF LIVERPOOL MSC PROJECT

This script contains the process to build the options avaliable in the main menu.
Uses the source script as a base to produce the text and html output.

"""

import urllib2, json
import folium
import source
import plotly
import webbrowser
import string
import os

#Defines the center coordintes to focus the map on this point 
centerCoord = [53.403341, -2.966834] #HARD DATA Liverpool coordinates for this project purpose
dir_path = os.path.dirname(os.path.abspath(__file__))
#Ask user its starting and destination coordinates and add this markers to the output map 
def askBothCoordinates ():

	lat = -100
	lng = -200
	while (lat > 90 or lat < -90) or (lng > 180 or lng < -180):
		print "Please enter your starting point coordinates separated by a comma: "		
		try:
			lat,lng = raw_input().split(",") #uncomment to get user input
			lat = float(lat)
			lng = float (lng)
			if 	(lat > 90 or lat < -90) or (lng > 180 or lng < -180):
				print "ERROR  enter valid coordinates (e.g 53.25,-2.7)"
		except:
			print "ERROR  enter valid coordinates (e.g 53.25,-2.7)"
	#lat=str(53.40094200948914) #HARD DATA
	#lng=str(-2.964162826538086) #HARD DATA
	start = source.getaddress(str(lat), str(lng)) #Converts coordinates to address
	print 'Your starting point is ' + str (start)
	lat2 = -100
	lng2 = -200
	while lat2 > 90 or lat2 < -90 or lng2 > 180 or lng2 < -180:
	    try:
	    	print "Please enter your destination point coordinates separated by a comma: "
	    	lat2,lng2 = raw_input().split(",") #uncomment to get user input
	    	lat2 = float(lat2)
	    	lng2 = float(lng2)
	    	if 	(lat2 > 90 or lat2 < -90) or (lng2 > 180 or lng2 < -180):
				print "ERROR  enter valid coordinates (e.g 53.25,-2.7)"
	    except:
	    	print "ERROR  enter valid coordinates (e.g 53.25,-2.7)"
	#lat2=str(53.4067731) #HARD DATA
	#lng2=str(-2.965722700000015) #HARD DATA
	destination= source.getaddress (str(lat2), str(lng2)) #Converts coordinates to address
	print "You are going from " + start + " to " + destination

	#Get gpx file for this route
	gpx, testfile = source.getgpxfile(lat, lng, lat2, lng2)
	allfeatures = source.concatFeatures() #Get amenities and obstacles dataframe for the route

	#Create map with dataframe 
	route_data = []
	route = gpx.routes[0]
	for point in route.points:
		route_data = route_data + [[point.latitude, point.longitude]]
	map_osm= folium.Map(location=centerCoord, zoom_start=16)
	folium.Marker(route_data[0],
				 popup= str(start)).add_to(map_osm)
	folium.Marker(route_data[-1],
				popup = str(destination)).add_to(map_osm)
	df_waypointsline = folium.PolyLine(
	    route_data,
	    weight=10,
	    color='#08306b'
	).add_to(map_osm)
	printfeatures(route.points, allfeatures, map_osm) #Call function to print route text output
	map_osm.save('SiloamRoutes.html') #Create an html file with the route on the map
	webbrowser.get().open("file://" + dir_path + "/SiloamRoutes.html?",new=0) #Open html file		

		
#Search method, gets a string with the location or address and converts it into coodinates for the route
def searchLocation(string): #Input if you are searching starting or destination point
	search = raw_input('Search ' + string + ' point:')
	#Search location from the Open Street Map API
	url = 'http://nominatim.openstreetmap.org/search?format=json&q=%s' % (search)
	url = url.replace(" ", "%20")
	#Store the seraching results into a json file
	response = json.loads(urllib2.urlopen(url).read())
	#Print results and select the starting point	
	if response == 0:
		print "No location found"
	else:
		i = 0
		for location in response:
			i = i + 1 
			print str(i) + ": " + location['display_name'] #Print address found
		i = i +1
		print str(i) +  ":  " + 'TRY AGAIN'
		option3 = 0
		while (option3 <=0 or option3 > i): 
			option3 = input('Choose your ' + string + ' point:') #Get option input
			if (option3 <=0 or option3 > i):
				print 'Invalid option'
			elif (option3 == i):
				string = str(string)
				searchLocation (string) #Try again
			else:
				#Assign the selected option's latitude, longitude and name
				for j in range(1 , i):
					if (j==option3):
						option_i= j-1
						name = str(response[option_i]['display_name'])						
						print 'Your ' + string +  ' point is ' + str(response[option_i]['display_name'])
						lat = float(response[option_i]['lat'])
						lng = float(response[option_i]['lon'])
				return lat, lng, name #Returns latitude, longitude and starting point 

#Ask user to search locations and builds the map and route from user's input
def getSearchedRoute():
	string = 'starting'
	lat, lng, name = searchLocation(string) #Search starting point
	start = [lat, lng]
	string = 'destination'
	lat2, lng2, name2 = searchLocation(string) #Search destination point
	destination = [lat2, lng2]
	if (lat == lat2 and lng == lng2):
		print 'You arrived at destination'
	else: 
		
		#Get route gpx file for the selected points
		gpx, testfile = source.getgpxfile(lat, lng, lat2, lng2)
		allfeatures = source.concatFeatures()
		
		#Create map
		route_data = []
		route = gpx.routes[0]
		for point in route.points:
			route_data = route_data + [[point.latitude, point.longitude]]
		map_osm= folium.Map(location=centerCoord, zoom_start=16)
		folium.Marker(route_data[0],
					 popup= str(name)).add_to(map_osm)
		folium.Marker(route_data[-1],
					popup = str(name2)).add_to(map_osm)
		df_waypointsline = folium.PolyLine(
		    route_data,
		    weight=10,
			color='#08306b'
			).add_to(map_osm)
		printfeatures(route.points, allfeatures, map_osm) #Print the route text output 
		map_osm.save('SiloamRoutes.html') #Create an html file with the route on the map
		webbrowser.get().open("file://" + dir_path + "/SiloamRoutes.html?",new=0) #Open html file		


#Function to analyze each feature and define if it's inside the range of the desired route
def printfeatures (route, bb_amenities, map_osm): #Input extracted gpx route, features data frame and map
	lenroute= len(route)
	scale = (.02/69)
	i = 1

	#Get the walking direction for every segment of the route by extracting this information from the gpx file
	#and then print the features inside this segment in order of appareance(the walking directions 
	#defines the parameters to sort the features) 
	for point in range(0, lenroute):
		if (point < lenroute-1):
			walk_direction = str(route[point].extensions['direction']) #Get this point walking direction
			nxt = point +1
			if (point == 0):
				print str(i) + ': ' + string.capwords(str(route[point].description)) #Print first instruction
				i = i +1
			elif (point < lenroute+1):	
				if (point > 0):
					#If there is no predefined instruction in the gpx define the walking direction by 
					#comparing the current walking direction with the previous one
					if (str(route[point].description)=='None'): 
						walk_direction1 = str(route[point-1].extensions['direction'])
						walk_direction2 = str(route[point].extensions['direction'])
						turn_direction = source.getTurnDirection(walk_direction1, walk_direction2)
						print str(i) + ': ' + turn_direction
						i = i + 1
		
					#Print predefined gpx file instruction
					else:
						walk_direction1 = str(route[point-1].extensions['direction'])
						walk_direction2 = str(route[point].extensions['direction'])
						print str(i) + ': ' + string.capwords(str(route[point].description)) 
						i = i + 1
		else:
			print 'You arrived at destination'

		#Every walking direction has different conditions to find out if a point is inside its boundaries
		if (walk_direction[:1]=='S'):
			#Defines the limit distance from the central segment line to the sides (this project takes as 
			#a reference the standard English street width plus 3 meters in order to detect the centroids 
			#of the amenities next to the stret)
			lat1=route[point].latitude  
			lat2=route[nxt].latitude 
			long1=route[point].longitude - (scale)
			long2=route[nxt].longitude + (scale)
			bb=[lat1, lat2, long1, long2]
			#Sort features in order of appareance. Depends on the walking direction
			bb_amenities = bb_amenities.sort_values(['lat'], ascending = False) 
			#Verifies if the feature is inside the limits of the segment 
			#and defines if its on the right or left side of the street
			for j in range(0, len(bb_amenities)):
				if (bb[1] <= bb_amenities['lat'].iloc[j] and bb_amenities['lat'].iloc[j] <= bb[0] and bb[2] <= bb_amenities['lng'].iloc[j] and bb_amenities['lng'].iloc[j] <= bb[3]): 
					#Obstacle case
					if (bb_amenities['geometry'].iloc[j]=='obstacle'):
						if (bb_amenities['lng'].iloc[j]>=route[point].longitude or bb_amenities['lng'].iloc[j]>=route[nxt].longitude):
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " left"
						else:
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " right "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], #Add marker to the map
							icon = folium.Icon(color ='red'), popup = popup).add_to(map_osm)				
					#Amenity case
					else:
						if (bb_amenities['lng'].iloc[j]>=route[point].longitude or bb_amenities['lng'].iloc[j]>=route[nxt].longitude):
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your left "
						else:
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your right "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], #Add marker to the map
							icon = folium.Icon(color ='green'), popup = popup).add_to(map_osm)

		#Applies same process for every walking direction
		elif (walk_direction[:1]=='N'): 
			lat1=route[nxt].latitude 
			lat2=route[point].latitude 
			long1=route[nxt].longitude - (scale)
			long2=route[point].longitude + (scale)
			bb_amenities = bb_amenities.sort_values(['lat'], ascending = True)
			bb=[lat1, lat2, long1, long2]
			for j in range(0, len(bb_amenities)):
				if (bb[1] <= bb_amenities['lat'].iloc[j] and bb_amenities['lat'].iloc[j] <= bb[0] and bb[2] <= bb_amenities['lng'].iloc[j] and bb_amenities['lng'].iloc[j] <= bb[3]):
					if (bb_amenities['geometry'].iloc[j]=='obstacle'):
						if (bb_amenities['lng'].iloc[j]>=route[point].longitude or bb_amenities['lng'].iloc[j]>=route[nxt].longitude):
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " right "
						else:
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='red'), popup = popup).add_to(map_osm)
					else:	
						if (bb_amenities['lng'].iloc[j]>=route[point].longitude or bb_amenities['lng'].iloc[j]>=route[nxt].longitude):
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your right "
						else:
							print '-' +  str(bb_amenities['Name'].iloc[j]) + " is at your left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='green'), popup = popup).add_to(map_osm)
		elif (walk_direction[:1]=='W'):
			lat1=route[nxt].latitude + (scale) 
			lat2=route[point].latitude - (scale)
			long1=route[nxt].longitude 
			long2=route[point].longitude
			bb_amenities = bb_amenities.sort_values(['lng'], ascending = False) 
			bb=[lat1, lat2, long1, long2]
			for j in range(0, len(bb_amenities)):
				if (bb[1] <= bb_amenities['lat'].iloc[j] and bb_amenities['lat'].iloc[j] <= bb[0] and bb[2] <= bb_amenities['lng'].iloc[j] and bb_amenities['lng'].iloc[j] <= bb[3]):
					if (bb_amenities['geometry'].iloc[j]=='obstacle'):
						if (bb_amenities['lat'].iloc[j]>=route[point].longitude or bb_amenities['lat'].iloc[j]>=route[nxt].longitude):
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " right "
						else:
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='red'), popup = popup).add_to(map_osm)

					else:
						if (bb_amenities['lat'].iloc[j]>=route[point].latitude or bb_amenities['lat'].iloc[j]>=route[nxt].latitude):
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your right "
						else:
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='green'), popup = popup).add_to(map_osm)

		else: 
			lat1=route[point].latitude + (scale) 
			lat2=route[nxt].latitude - (scale)
			long1=route[point].longitude 
			long2=route[nxt].longitude
			bb=[lat1, lat2, long1, long2]
			bb_amenities = bb_amenities.sort_values(['lng'], ascending = True)
			for j in range(0, len(bb_amenities)):
				if (bb[1] <= bb_amenities['lat'].iloc[j] and bb_amenities['lat'].iloc[j] <= bb[0] and bb[2] <= bb_amenities['lng'].iloc[j] and bb_amenities['lng'].iloc[j] <= bb[3]):
					if (bb_amenities['geometry'].iloc[j]=='obstacle'):
						if (bb_amenities['lat'].iloc[j]>=route[point].longitude or bb_amenities['lat'].iloc[j]>=route[nxt].longitude):
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " right "
						else:
							text = source.function(bb_amenities['Name'].iloc[j])
							print "*" + text + " left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='red'), popup = popup).add_to(map_osm)
					else:	
						if (bb_amenities['lat'].iloc[j]>=route[point].latitude or bb_amenities['lat'].iloc[j]>=route[nxt].latitude):
							print '-'  + str(bb_amenities['Name'].iloc[j]) + " is at your right "
						else:
							print '-' + str(bb_amenities['Name'].iloc[j]) + " is at your left "
						popup = str(bb_amenities['Name'].iloc[j]) 
						folium.Marker([bb_amenities['lat'].iloc[j], bb_amenities['lng'].iloc[j]], 
							icon = folium.Icon(color ='green'), popup = popup).add_to(map_osm)
	map_osm.save('SiloamRoutes.html') #Create an html file with the route on the map
	webbrowser.get().open("file://" + dir_path + "/SiloamRoutes.html?",new=0) #Open html file		

		

#This function finds all the amenities close to a specific point whitin a specific radius, ask destination
#point get directions to it  
def getplacesnear (lat, lng, start): #Input current lat, lng and address (string)
	radius = -1
	#Ask a searching radius to user 
	while radius < 0:
		try:
			radius = float(input('Enter your searching radius in meters:'))
			if radius < 0:
				print 'Error: Enter a positive value'
			else:
				radius = radius/1000
		except:
			print 'Error enter a valid input'
	margindistance = 0.001
	#Creat map and mark the current location
	map_osm= folium.Map(location=[lat, lng], zoom_start=16)
	map_osm.save('SiloamRoutesNear.html')
	folium.Marker([lat,lng]).add_to(map_osm)
	bb_amenities = source.getAmenities()

	#Set markers for amenities inside the searching radius	
	j = 0
	places = []
	for i in range(0, len(bb_amenities)-1):
		distance = source.getDistanceToLocation(lng, lat, bb_amenities['lng'].iloc[i], bb_amenities['lat'].iloc[i])
		if (distance <= radius):
			if distance > margindistance:
				print str(j+1) + ':' + str(bb_amenities['Name'].iloc[i]) + ' is at ' +  str(format((distance*1000), '.2f')) + ' meters.'
				pair = [j+1, i]
				j = j + 1
				places.append(pair)
				popup = str(bb_amenities['Name'].iloc[i]) 
				folium.Marker([bb_amenities['lat'].iloc[i], bb_amenities['lng'].iloc[i]], 
					icon = folium.Icon(color ='black'), popup = popup ).add_to(map_osm)
	#Save near places into an html file 			
	map_osm.save('SiloamRoutesNear.html') #Create an html file with the route on the map
	webbrowser.get().open("file://" + dir_path + "/SiloamRoutesNear.html?",new=0) #Open html file		
	#Ask destination point from near places
	if ( j != 0):
		option = 0
		while (option <=0 or option > j): 
			option = input('Choose your destination:') 
			if (option <=0 or option > j):
				print 'Invalid option'
			#Get route and save it into map
			else:
				for i in range(0 , j):
					if (places[i][0]==option):
						option_i=places[i][1]

				lat2= str(bb_amenities['lat'].iloc[option_i])
				lng2=str(bb_amenities['lng'].iloc[option_i])
				destination= source.getaddress (lat2, lng2)

				print "You are going from " + start + " to " + destination

				gpx, testfile = source.getgpxfile(lat, lng, lat2, lng2)
				allfeatures = source.concatFeatures()

				#Create map
				route_data = []
				route = gpx.routes[0]
				for point in route.points:
					route_data = route_data + [[point.latitude, point.longitude]]

				map_osm= folium.Map(location= [lat, lng], zoom_start=16)
				folium.Marker(route_data[0],
							 popup= str(start)).add_to(map_osm)
				folium.Marker(route_data[-1],
							popup = str(destination)).add_to(map_osm)
				df_waypointsline = folium.PolyLine(
				    route_data,
				    weight=10,
				    color='#08306b'
				).add_to(map_osm)
			printfeatures(route.points, allfeatures, map_osm) #Print features 
			map_osm.save('SiloamRoutes.html')
	
	else:
		print 'There is nothing to explore around you'



	