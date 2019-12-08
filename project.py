#Flask imports
from flask import Flask, render_template, request, redirect, url_for

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

@app.route('/restaurants/<int:restaurant_id>/new', methods=["GET", "POST"])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    return "page to create a new menu item."

@app.route('/restaurants/<int:restaurant_id>/edit/<int:menu_id>/', methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
    if request.method == "POST":
        item = session.query(MenuItem).filter(Restaurant.id == restaurant_id, MenuItem.id == menu_id).one()
        item.name = request.form['name']
        
        session.add(item)
        session.commit()
        return redirect(url_for("restaurantMenu", restaurant_id = restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
        item = session.query(MenuItem).filter(Restaurant.id == restaurant_id, MenuItem.id == menu_id).one()
        return render_template('editmenuitem.html', restaurant = restaurant, item = item)
    return "page to edit a new menu item."

@app.route('/restaurants/<int:restaurant_id>/delete/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a new menu item."

if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)
