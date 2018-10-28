# Restaurants

## Description
Restaurants is a Django-based web application to manage a restaurant bookings system.
<br>
There are 3 types of user:
- The anonymous user who can search for restaurants available by day, time, place,
types of kitchen and services offered.
- The registered user who can make reservations, can modify and delete them and see the history.
- The restaurant owner who can, upon registration, insert information about the restaurant as
types of kitchen, services provided, address, menu, photos, number of seats and duration of the reservation.
<br>
The search results are sorted by proximity to the search site.
<br>
A registered user can put himself on the waiting list for the busy restaurant and will receive 
an e-mail when the seats are available.

![Restaurants - Home](https://imgur.com/TDvNizR.png)

## Requirements
To run Restaurants the system requires Python3.5, Django 1.11 and MySql.
If they aren't installed follow these steps:
- Set python3.5 as default python interpreter by typing in the shell:

`sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1`
<br>
`sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.5 2`
- Install Django1.11, MySql and other necessary packages:

`sudo apt install python3-setuptools python3-dev python-pip python3-pip mysql-server libmysqlclient-dev`
<br>
`pip install Django==1.11 django-mysql wheel mysqlclient`
- Download the .zip archive from GitHub.
- Extract the contents.
- Open a terminal in the directory.
- Run to load example db:

`sudo mysql -u root -p password < djangorestaurants.sql`.
- Run the server typing:

`python manage.py runserver`.
- Visit with a browser 'http://127.0.0.1:8000/' to use the application.
<br>

> Tested on *Linux Mint 18.2 Cinnamon 64-bit*.
> <br>
> Tested on *Google Chrome 68.0.3440.106*.

## Sample data
Example of user credentials:
- [SUPERUSER] - username: admin, password: rest2018
- [CLIENT] - username: giovannipascoli, password: rest2018
- [CLIENT] - username: ugofoscolo, password: rest2018
- [RESTAURANT] - username: giuseppegaribaldi, password: rest2018
- [RESTAURANT] - username: alessandromanzoni, password: rest2018
- [RESTAURANT] - username: giacomoleopardi, password: rest2018
- [RESTAURANT] - username: luigipirandello, password: rest2018
- [RESTAURANT] - username: giovanniverga, password: rest2018