from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# read data from db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import db class we designed
from database_setup import Restaurant, Base, MenuItem
#from sqlalchemy import Column, ForeignKey, Integer, String
# import comman gateway interface
import cgi


# create a global session to connect with db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""
# to deploy server to vagrant. it needs to import sqlalchemy to /user/lib/python2.7/dis...

Inorder to install the sqlalchemy to new ubuntu OS, it needs to install the pip or easy_install first.
1. install pip by using:
	sudo apt-get install python3-setuptools  -> easy_install3
	sudo easy_install3 pip 
2. install SQLAlchemy to current tools folder
	pip install SQLAlchemy   -> install to the current python lib in your user path.
3. copy SQLAlchemy to the correct version of python we using
	sudo sp -avr sqlalchemy/ ../../python2.7/dist-packages/
	sudo sp -avr "another sqlalchemy folder"/ ../../python2.7/dist-packages/	
"""


class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self): 
		try:
			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += "<html><body>Hello!</body></html>"
				self.wfile.write(message)
				print message
				return 
			 
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				message = ""
				message += '''<html><body><h1>Make a New Restaurant</h1><form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>'''
				message += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' >"
				message += '''<input type="submit" value="Add">'''
				message += '''</form></body></html>'''
				self.wfile.write(message)
				print message
				return 
			
			if self.path.endswith("/edit"):
				rest_id = self.path.split("/")[2] 
				curr_rest = session.query(Restaurant).filter_by(id = rest_id).one()
				if curr_rest != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					curr_menus = session.query(MenuItem).join(MenuItem.restaurant).filter(Restaurant.id == rest_id)
					output = ""
					output = "<html><body>"
					output +="<h1> Restaurant - %s</h1>" % curr_rest.name
					output += "<h2>Edit</h2><h3>"
					output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" %rest_id
					output += "<label for='Name'>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;Restaurant Name:</label> <input type='text' name='NewName' id='Name'>"
					output += "<input type='submit' value='Submit'></input>"
					output += "</form>"
					output += "</h3> <br />"
					output +="<table><tr><th>Menu Name</th><th>Description</th><th>Courses</th><th>Price</th></tr>"
					for menu in curr_menus:
						output += "<tr>" 
						output += "<td>" + str(menu.name) + "</td>" + "<td>" + str(menu.description) + "</td>" + "<td>" + str(menu.course) + "</td>" + "<td>" + str(menu.price) + "</td>"
						output += "</tr>"
					output += "</table>"
					output += "<div>"
					output += "</div>"
					output += "<a href='/restaurants' > <button>Back</button></a>"
					output += "</body></html>"
					self.wfile.write(output)
					print output 
				return 
				
			if self.path.endswith("/restaurants"):
				restaurant_list = session.query(Restaurant).all()
				# print restaurant_list 
				
				# the way to write query with a foreign key
				"""
				items = session.query(MenuItem).all()
				print items
				for item in items:
					print str(item.restaurant_id)
				spec = session.query(MenuItem).join(MenuItem.restaurant).filter(Restaurant.id == 9)
				print spec.count()
				"""
				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers() 
				
				message = ""
				message += "<html>"
				# add extra link and scripts
				message += "<head>"
				message += "</head>"
				message += "<body><title> Restaurant List </title>"
				# add new restaurant
				message += '''<label> Add Restaurant </label>'''
				message += '''<a href = '/restaurants/new'><button type="submit">Add</button></a>''' 
				
				# show the current restaurants
				message += "<table><tr><th>Restaurant Name</th><th>Menu numbers</th><th colspan = '2'>Operation</th></tr>"
				for rest in restaurant_list:
					print str(rest.id)
					#m_menu = session.query(MenuItem).filter_by(restaurant_id  = rest.id)
					#print m_menu
					message += "<tr>" + "<td>" + rest.name + "</td>"
					message += "<td>" + str(session.query(MenuItem).join(MenuItem.restaurant).filter(Restaurant.id == rest.id).count()) + "</td>"
					# add operation for this entry
					message += "<td>"
					message += "<a href='/restaurants/%s/edit'><button>Edit</button> </a>" % rest.id
					message += "</td>"
					
					# delete a restaurant
					message += "<td>"
					message += "<a href='/restaurants/%s/delete'><button>Delete</button> </a>" % rest.id
					message += "</td>"
					message += "</tr>"
					
				message += "</table>" 
				message += "</body></html>"
				
				
				# message += "<html><body>TEST222 Works!</body></html>"
				self.wfile.write(message)
				print message
				return   
				
			if self.path.endswith("/delete"): 
				rest_id = self.path.split("/")[2] 
				curr_rest = session.query(Restaurant).filter_by(id = rest_id).one()
				
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				
				output = ""
				output = "<html><body>"
				output +="<h1> Restaurant - %s</h1>" % curr_rest.name
				output += "<a href='/restaurants/%s/edit' > <button>Edit</button></a>" %rest_id
				output += "<a href='/restaurants' > <button>Back</button></a>"
				output += "<div>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" %rest_id
				output += "<h2>Do you really want to delete this restaurant ???</h2>"
				output += "<input type='submit' value= 'Yes'>  </input>"
				output += "</form>"
				output += "</div>"
				self.wfile.write(output)
				print output
			 
		except: 
			print "except happend: when get data of restaurant" 
			session.close() 
			#session.rollback() 
		finally:
			session.close()  
	
	def do_POST(self):
		try:
			if self.path.endswith("/restaurants/new"):
				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					# return the dictionary of options
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')
					
				newRest = Restaurant(name = messagecontent[0])
				session.add(newRest)
				session.commit()
				
				self.send_response(301)
				self.send_header('Content-type', 'text/html')
				self.send_header('Location','/restaurants')
				self.end_headers()
			
			if self.path.endswith("/edit"):
				rest_id = self.path.split("/")[2] 
				curr_entry = session.query(Restaurant).filter_by(id = rest_id)
				curr_rest = curr_entry.one()
				print curr_rest.name
				
				ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
				if ctype == 'multipart/form-data':
					# return the dictionary of options
					fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('NewName')
				
				newName = messagecontent[0]
				print newName
				
				if curr_rest != []:
					curr_rest.name = newName 
					session.add(curr_rest)
					session.commit()
				
				self.send_response(301)
				self.send_header('Content-type','text/html')
				dest = '/restaurants/%s/edit' %rest_id  
				self.send_header('Location', dest)
				self.end_headers() 
				
			if self.path.endswith("/delete"):
				rest_id = self.path.split("/")[2] 
				curr_entry = session.query(Restaurant).filter_by(id = rest_id)
				curr_rest = curr_entry.one()
				
				if curr_rest != []:
					session.delete(curr_rest)
					session.commit()
					self.send_response(301)
					self.send_header('Content-type', 'text/html')
					dest = '/restaurants'
					self.send_header('Location', dest)
					self.end_headers()
					
		except: 
			print "except happend: when create data of restaurant" 
			session.close() 
			#session.rollback() 
		finally:
			session.close()
		
def main():
	try:
		port = 8090
		server = HTTPServer(('', port), WebServerHandler) 
		print "Restaurant server is running... Port : %s" % port
		server.serve_forever()
	except KeyboardInterrupt:
		print " ^C entered, stopping web server...."
		server.socket.close()


if __name__ == '__main__':
	main()