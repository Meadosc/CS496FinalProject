#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Relationship Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json

#Relationship
class Relationship(ndb.Model):
	workoutID = ndb.StringProperty(required=True)
	exerciseIDs = ndb.StringProperty(repeated=True) #list of exercise ids in the workout

	
	

class RelationshipHandler(webapp2.RequestHandler):
	def get(self, id=None):
		#if there is an id, respond with info corresponding to that id.
		#else, give a body response saying your're at the RelationshipHandler page
		if id:
			r = ndb.Key(urlsafe=id).get() #get the object from the database
			r_d = r.to_dict() #turn r object (relationship) into a dictionary
			r_d['self'] = "/relationship/" + id
			self.response.write(json.dumps(r_d))
		else: 
			relationship_dict = [] #dictionary to store relationship in
			for r in Relationship.query().fetch(): #fetch all relationship from the database
				r_d = r.to_dict() #turn each relationship instance into a dictionary
				r_d['self'] = '/relationship/' + r.key.urlsafe() #add a "self" link to each relationship dictionary
				relationship_dict.append(r_d) #save relationship dictionary in larger dictionary
			self.response.write(json.dumps(relationship_dict)) #return relationship with links to themselves.