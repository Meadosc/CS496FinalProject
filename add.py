#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Add Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from workout import Workout
from exercise import Exercise

class AddHandler(webapp2.RequestHandler):
	def get(self, id=None):
		w = ndb.Key(urlsafe=id).get()  #get the workout object from the database
		###use this to send a json string of all the exercise IDs in that workout. Like View from the slip.
	
	def post(self, id=None):
		w = ndb.Key(urlsafe=id).get()  #get the workout object from the database
		exercise_data = json.loads(self.request.body) 
		#Needs to be sent JSON body with format {"URL_ID":"exercise URL safe id here"}
		self.response.write(exercise_data["URL_ID"]) ###debug
		w.exerciseIDs.append(str(exercise_data["URL_ID"])) ###curently putting u' in front of string. May or may not be a problem. We'll see.
		w.put()