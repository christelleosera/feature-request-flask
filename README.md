#Feature Request App

A web application built on Flask that takes user input to add feature requests to the database.

##Tech Used
1. [Python Flask](http://flask.pocoo.org/)
2. MySQL
3. HTML/CSS
4. [Bootstrap](http://getbootstrap.com/)
5. [Bootstrap Validator](http://1000hz.github.io/bootstrap-validator/)
6. [Bootstrap Datepicker](https://github.com/eternicode/bootstrap-datepicker/)
7. [Flask BasicAuth](https://github.com/jpvanhal/flask-basicauth)
8. [KnockoutJS](https://github.com/knockout/knockout)

##Setup
To use on your local machine:
1. Install Python2.7 and pip

2. Install Flask `pip install Flask`
3. Install MySQL
4. Run SQL script for database creation `mysql < db_creation`
5. Install flask-mysql `pip install flask-mysql`
6. Install Flask-BasicAuth `pip install Flask-BasicAuth`
7. Run the app `python app.py`
8. App requires authentication. Username and password can be viewed and changed at the app.py file.

##Hosted
To demo, this web app is also hosted [here](http://ec2-52-24-193-7.us-west-2.compute.amazonaws.com/).