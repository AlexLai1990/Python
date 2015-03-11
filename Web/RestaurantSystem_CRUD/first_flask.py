from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
sys.path.append("C:\PyCharmFolder\Test1")
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@app.route('/')
@app.route('/restaurants', methods=['GET','POST'])
def getAllRestaurants():
	if request.method == 'GET':
		m_restaurants = session.query(Restaurant).all() 
		return render_template('restaurants.html', restaurants = m_restaurants)
	else: 
		new_rest = Restaurant(name = request.form['Name'])
		session.add(new_rest)
		session.commit()
		flash("Restaurant : " + request.form['Name'] + " has been added!")
		m_restaurants = session.query(Restaurant).all() 
		return render_template('restaurants.html', restaurants = m_restaurants)
	
@app.route('/restaurants/<int:restaurant_id>/edit', methods=['POST'])
def editRestaurant(restaurant_id):
	if request.method == 'POST':
		curr_rest = session.query(Restaurant).filter_by(id = restaurant_id).one()
		curr_rest.name = request.form['Name']
		session.add(curr_rest)
		session.commit()
		m_restaurants = session.query(Restaurant).all() 
		return render_template('restaurants.html', restaurants = m_restaurants)
		
@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET'])
def deleteRestaurant(restaurant_id):
	if request.method == 'GET':
		filter_res = session.query(Restaurant).filter_by(id = restaurant_id)
		print filter_res
		#curr_rest = session.query(Restaurant).filter_by(id = restaurant_id).one() 
		if filter_res != []:
			curr_rest = filter_res.one() 
			session.delete(curr_rest)
			session.commit()
			flash("Restaurant : " + curr_rest.name + " has been deleted!")
		m_restaurants = session.query(Restaurant).all() 
		return redirect(url_for('getAllRestaurants')) 
		#render_template('restaurants.html', restaurants = m_restaurants)		
		 
# Making an API for get all menus in one restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])
	
@app.route('/restaurants/<int:restaurant_id>/')
def getMenus(restaurant_id):
	curr_restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one() 
	menus = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = curr_restaurant, items = menus) 

# using html template to render.
# logic part: {% %}	content: {{}}
@app.route('/restaurants/<int:restaurant_id>/create/', methods=['GET','POST'])	
def newMenuItem(restaurant_id):
	if request.method == 'GET': 
		return render_template('createMenu.html', restaurant_id = restaurant_id)
	else: 
		newMenu = MenuItem(name = request.form['Name'], 
						   description = request.form['Description'],
						   course = request.form['Course'],
						   price = request.form['Price'],
						   restaurant_id = restaurant_id
		)  
		session.add(newMenu)
		session.commit()
		flash("Menu : " + request.form['Name'] + " has been added!")
		return redirect(url_for('getMenus', restaurant_id = restaurant_id)) 

# the function we defined can be reached by using url_for in template html file.
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])	
def editMenuItem(restaurant_id, menu_id):
	error = None
	curr_rest = session.query(Restaurant).filter_by(id = restaurant_id).one() 
	curr_menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
	#print curr_menu  
	if curr_menu == []:
		error = "not exist menu"
	
	if request.method == 'GET': 
		return render_template('editMenu.html', restaurant = curr_rest, menu = curr_menu, error = error)
	else :
		print "In post"
		if error == None : 
			curr_menu.name = request.form['Name']
			curr_menu.description = request.form['Description']
			curr_menu.course = request.form['Course']
			curr_menu.price = request.form['Price']
			session.add(curr_menu)
			session.commit()
		return redirect(url_for('getMenus', restaurant_id = restaurant_id)) 
 
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET'])	
def deleteMenuItem(restaurant_id, menu_id):
	error = None
	curr_rest = session.query(Restaurant).filter_by(id = restaurant_id).one() 
	curr_menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).filter_by(id = menu_id).one()
	#print curr_menu  
	if curr_menu == []:
		error = "not exist menu"
	if request.method == 'GET':
		session.delete(curr_menu)
		session.commit()
	return redirect(url_for('getMenus', restaurant_id = restaurant_id)) 
		
if __name__ == '__main__':
	app.secret_key = 'my_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)