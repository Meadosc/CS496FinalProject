#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Remove Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from workout import Workout
from exercise import Exercise

class RemoveHandler(webapp2.RequestHandler):
	def post(self, id=None):
		if id:
			w = ndb.Key(urlsafe=id).get()  #get the workout object from the database
			request_data = json.loads(self.request.body)
			exerciseID = request_data["URL_ID"] #request must be json of form {"URL_ID":"exercise id here"}
		
			delFlag = -1
			for i, exID in enumerate(w.exerciseIDs):			
				if exID == exerciseID:
					delFlag = i
					self.response.write("match found" + str(i)) ###debug
			if delFlag != -1:
				w.exerciseIDs.pop(delFlag)
				w.put()
	
	
		
		
		