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