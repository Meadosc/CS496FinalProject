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
		#return workout ids with list of exercise ids in JSON format
		relationship_dict = [] #dictionary to store relationships in
		if id:
			for r in Workout.query().fetch(): #fetch all workout from the database
				r_d = "{\"workoutURLID\":  " + r.workoutURLID + "\""
				
				y=0
				for x in r.exerciseIDs:
					r_d = r_d + ", \"exerciseURLID" + str(y) + "\": \"" + r.exerciseIDs[y] + "\""
					y = y+1
					#self.response.write(r_d)
				
				r_d = r_d + "}"
				relationship_dict.append(r_d)
		self.response.write(relationship_dict)
			

	
	def post(self, id=None):
		w = ndb.Key(urlsafe=id).get()  #get the workout object from the database
		exercise_data = json.loads(self.request.body) 
		#Needs to be sent JSON body with format {"URL_ID":"exercise URL safe id here"}
		self.response.write(exercise_data["URL_ID"]) ###debug
		w.exerciseIDs.append(str(exercise_data["URL_ID"])) ###curently putting u' in front of string. May or may not be a problem. We'll see.
		w.put()