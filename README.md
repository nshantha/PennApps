# SafeMaps
  SafeMaps is a platform that allows for people to make conscious decisions before leaving their homes. Using cameras running a person detection algorithm, data can be collected on how well social distancing is being practiced in the area. These cameras would be installed in public places like large couryards, parks, and other open spaces. The data is then sent back to a database in real time and rendered as a heat map for the end user, allowing them to plan an evening out, morning jog, or commute to work before even leaving home. 

## Technology Used
OpenCV and pythong was used to process the video data. 
The front end for the website was created made with ReactJS. All of the data produced by the videos is stored on a postgres server and accessed via POST/GET requests served by a cherrypy server

## Installation/Running

To launch the website, go to `/web/ui` and run the following:
```
npm i
npm start
```
Doing so will launch the website on http://localhost:8080
If you'd like to run your own instance of the postgres db to connect to, go to `/web/server/ ` and copy `conf.default.json` into a file called `conf.json` After filling out the necessary fields run:

```
python3 postgres.py
python3 server.py
```
You will need a running postgres instance in order for this to work.
