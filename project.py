#Flask imports
from flask import Flask, render_template

#Database imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)

    html = render_template('menu.html', restaurant=restaurant, items = items)
    return html

@app.route('/restaurants/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item."

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a new menu item."

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a new menu item."

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
