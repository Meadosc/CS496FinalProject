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
		w = ndb.Key(urlsafe=id).get()  #get the workout object from the database
		##########################
		###add in removal functionality
		##########################
		