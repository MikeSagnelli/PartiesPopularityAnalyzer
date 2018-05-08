# PartiesPopularityAnalyzer

Parties Popularity Analyzer is an app web that will allow the user to analyze the popularity of politician candidates per state. Using the TwitterAPI we are able to determine this popularity based on user tweets, and each state geocode. Today this web app is analyzing the Mexican presidential elections of 2018; however, it is possible to adapt this app to analyze any elections from all over the world. The Mexican candidates are: Andrés Manuel López Obrador, Ricardo Anaya Cortés, José Antonio Meade Kuribreña, Margarita Ester Zavala Gómez del Campo, and Jaime Rodríguez Calderón.

## How to run project

This project comes with a Makefile that makes life easier. Therefore, to run the project using the Makefile use the following commands:

``make install``

This will install all dependencies for the project. Furthermore, there are some needed environment variables, but these will be provided upon request to ing.sagnelli@gmail.com

Finally, use the following command:

``make serve``

If all was correct, then the console will keep running, and if localhost:5000 is accessed, the project shall be seen.

Without using the Makefile you have to ``sudo pip install`` all the dependencies in the requirements.txt file, export the environment variables, and run ``python routes.py``.

That's it for running the project. Otherwise, simply go to [heroku link](https://parties-popularity-analyzer.herokuapp.com/)

## Technologies

![MongoDB](http://solucionesit.ldtsynergy.com/-/Srvs015/MongoDB/file/view/mongodb.png/547250106/315x368/mongodb.png)
![Flask](https://cdn-images-1.medium.com/max/1600/1*Ou6FFJJD3zhcIUU8wBZqIw.png =100x)
![Jinja2](https://quintagroup.com/cms/python/images/jinja2.png/image_preview)
![Heroku](http://kennmyers.github.io/assets/heroku_guide/heroku_logo.png)
![MLab](https://mlab.com/company/brand/img/downloads/mLab-logo-onlight.png)
![PyMongo](https://jarroba.com/wp-content/uploads/2015/03/MongoPython.png)