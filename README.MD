# Grocery App
## Create virtual enviroment (This is for Mac / Linux Environment)
```
command: python3 -m venv env
```
- Create the virtualenv inside the directory
```
command: source env/bin/activate
```
- Use requirements.txt to install compatible packages
```
command: pip install -r requirements.txt
```
- To run flask server
```
command: python app.py
```

## Description
Grocery App is a simple E-Commerce application like BigBasket, Blinkit, etc. It is a multi user app with
Admin and User Interface used for buying and selling groceries.<br><br> For Admin the functionalities are <br> Login, create, edit, delete categories & products and ability to view summary.<br><br> 
For Users the functionalities are <br> Login, View Products category-wise, Add to cart,Edit quantity, Buy from cart, ability to view Profile Page.<br><br>
- ## Technologies used
1. Python (Programming Language)
2. Flask (Web Framework)
3. HTML (HTML Doc.)
4. Bootstrap (Frontend)
5. Jinja2 (HTML injection)
6. SQLAlchemy (SQLite connection)


# celery -A app.celery worker -l info
