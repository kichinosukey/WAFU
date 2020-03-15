# WAFU(Web Application Framework for us)

The WAFU is web application frame work design patter by Python(Flask).
WAFU's target is "To be template for the beginner of web app developper".

To achieve it, WAFU took in these frameworks below.

- Backend
  - API
    - [Flask](https://flask.palletsprojects.com/en/1.1.x/) (Python)
  - Database
    - [Sqlite](https://www.sqlite.org/index.html)
- Frontend
  - [Bokeh](https://docs.bokeh.org/en/latest/docs/user_guide/bokehjs.html) (Javascript) in sample app

The application architechture is below.


## index.py
- script for running flask server
- This has some interfaces to setup the server like ip address, port or debug
- Some apps what you want to add are registered in it as [Blueprint](https://flask.palletsprojects.com/en/1.1.x/blueprints/)

## apps
- The directory "apps" is root for each applications.  
- Main components are auth.py and db.py  

### auth.py
- script for user authentification.
- It has interface with user db
- Any requests for app must get connection with this. But this is choiceable.
- If you don't have any accounts in user db, your requests are redirected to login page

### db.py
- For database opereation
- Currently this only supports sqlite
- Basic CRUD operation can be used

## sample (app name can be decided as you like)
- Application folder you want to made
- This design pattern is inspired to [MVC model](https://ja.wikipedia.org/wiki/Model_View_Controller)
- Main four components are below

### body.py
- API (Application Programming Interface)
- This is called as "Model"

### view.py
- This is called as "Controller"

### static
- The directory contains css / js(javascripts)

### templates
- The directory contains sample's html file
- This is called as "View"