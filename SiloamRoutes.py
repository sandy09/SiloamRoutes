"""
DEVELOPED BY SANDRA GARCIA LAMADRID
LAST UPDATED SEPTEMBER 25 2017
UNIVERSITY OF LIVERPOOL MSC PROJECT

SiloamRoutes allows users to get a route from one point to another one, shows the optimal route 
based on the GraphHopper API and announce the amenities and obstacles found in that route. 
It also offers you the option to explore around yo and get a route from your location to this 
destination including the amenities and obstacles ahead of you
This file holds the option menu structure of the programm and calls specific functions to provide 
a text output in the terminal and an html file holding the close places and the route
"""

import folium
import source
import webbrowser
import options
import sys
import os 



def main():
	dir_path = os.path.dirname(os.path.abspath(__file__))
	webbrowser.get()
	print "Welcome to SiloamRoutes\n"
	option1 = 0
	#Ask user first option
	while option1 != 1 and option1!= 2:
		print 'MENU'
		print '1: Select starting and destination points'
		print '2: Explore around me'
		print '3: Exit'
		option1 = input('Choose an option:')
		if (option1 == 1):
			option2 = 0 
			#Ask user second option
			while option2 != 1 and option2 != 2 and option2 != 3:	
				print '1:Enter starting and destination point coordinates'
				print '2:Search a starting and destination location'
				print '3:Return to main menu'
				print '4:Exit'
				option2 = input('Choose option:')
				if (option2 == 1):
					#Call  function to ask coordinates and draw route
					options.askBothCoordinates()
					option3 = 0
					while (option3 != 1 and option3 != 2 and option3 != 3):
						print "1: Go back"
						print "2: Go to main menu"
						print "3: Exit"
						option3 = input('Choose option:')
						if (option3 ==1):
							#Go back to previous menu
							option2 = 0
						elif (option3 == 2):
							#GO back to main menu
							main() 
						elif option3 == 3:
							#Exit
							sys.exit('Goodbye thank you for using SiloamRoutes')
						else: 
							print 'Invalid option'
				elif (option2 == 2):
					#Call function to search specific address or place
					options.getSearchedRoute()
					option3 = 0
					while (option3 != 1 and option3 != 2 and option3 != 3):
						print "1: Go back"
						print "2: Go to main menu"
						print "3: Exit"
						option3 = input('Choose option:')
						if (option3 ==1):
							#Go back to previous menu
							option2 = 0
						elif (option3 == 2):
							#GO back to main menu
							main() 
						elif option3 == 3:
							#Exit
							sys.exit('Goodbye thank you for using SiloamRoutes')
						else: 
							print 'Invalid option'
				elif (option2==3):
					#Go back to main menu
					main()
				elif (option2 == 4):
					#Exit
					sys.exit('Goodbye thank you for using SiloamRoutes')
				else:
					print 'Invalid option'
		
				option3 = 0 
				option4 = 0
				#Sub menu

			option4 = 0

			#Sub menu
			while (option4 != 1 and option4 != 2):
				print "1: Go to main menu"
				print "2: Exit"
				option4 = input('Choose option:')
				if (option4 ==1):
					#Go back to main menu
					main()
				elif option4 == 2:
					#Exit
					sys.exit('Goodbye thank you for using SiloamRoutes')
				else: 
					print 'Invalid option'
		elif (option1==2):

			option2 = 0 
			#Ask exploration option
			while option2 != 1 or option2 != 2 or option2 != 3 and option2 !=4:
				print '1:Enter starting point coordinates'
				print '2:Search a starting location'
				print '3:Return to main menu'
				print '4:Exit'
				option2 = input('Choose option:')
				if (option2 == 1):
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
					#lat=str(53.40094200948914)  #HARD DATA
					#lng=str(-2.964162826538086) #HARD DATA
					#Convert coordinates to string
					start = source.getaddress(str(lat),str(lng))
					print 'Your starting point is ' + str (start)
					#Find close places to the starting point
					options.getplacesnear(float(lat), float(lng), start)
					option4 = 0 		

				elif (option2==2):
					#Search starting point by address or name
					lat, lng, name = options.searchLocation('starting')
					#Find close places to the starting point
					options.getplacesnear(lat, lng, name)
				elif (option2 == 3):
					#Go back to main menu
					main()
				elif (option2 ==4):
					#Exit
					sys.exit('Goodbye thank you for using SiloamRoutes')
				else: 
					'Invalid option'

				option3 = 0 
				#Submenu
				while (option3 != 1 and option3 != 2 and option3 != 3):
					print "1: Go back"
					print "2: Go to main menu"
					print "3: Exit"
					option3 = input('Choose option:')
					if (option3 ==1):
						#Go back to previous menu
						option2 = 0
					elif (option3 == 2):
						#Go back to main menu
						main()
					elif option3 == 3:
						#Exit
						sys.exit('Goodbye thank you for using SiloamRoutes')
					else: 
						print 'Invalid option'	

			#Submenu
			option4 = 0
			while (option4 != 1 and option4 != 2 and option4 != 3):
				print "1: Go back"
				print "2: Go to main menu"
				print "3: Exit"
				option4 = input('Choose option:')
				if (option4 ==1):
					#Go bakc to previous menu
					option2 = 0
				elif (option4 == 2):
					#Go back to main menu 
					main()
				elif option4 == 3:
					#Exit
					sys.exit('Goodbye thank you for using SiloamRoutes')
				else: 
					print 'Invalid option'

		elif (option1 == 3):
			sys.exit('Goodbye thank you for using SiloamRoutes')
		else:
			print 'Invalid option'

	webbrowser.get().open("file://" + dir_path + "/SiloamRoutes?.html",new=0)	

		
main ()





