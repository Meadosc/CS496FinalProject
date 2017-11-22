#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Relationship Class and handler for main.py
###currently not used. Had more problems than it solved.
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json

#Relationship
class Relationship(ndb.Model):
	workoutID = ndb.StringProperty(required=True)
	exerciseIDs = ndb.StringProperty(repeated=True) #list of relationship ids in the workout

	
	

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
			

	def post(self):
		#Create parent key so we can have a relationship tree
		parent_key = ndb.Key(Relationship, "parent_relationship")
		#get json data from post, then use "loads" to turn json into object. assign to relationship_data.
		relationship_data = json.loads(self.request.body)
		
		#check if required data is good. If not throw bad data error
		if isinstance(relationship_data['workoutID'], basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'workoutID', and 'exerciseID'")
		if isinstance(relationship_data.get('exerciseID', None), basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'workoutID', and 'exerciseID'")
			

		# Need to check if a relationship for the workout already exists. If so, append exercise.
		# If not, create relationship then add workout and exercise.	
		doesExist = 0 #flag for if the workout already exists.
		for r in Relationship.query().fetch():
			if relationship_data['workoutID'] == r.workoutID:
				doesExist = 1
				r.exerciseIDs.append(relationship_data['exerciseID']) #add exercise ID to already existing relationship 
				r.put() #add info to database

		if doesExist == 0: #if the workout did not already have a relationship, add relationship and exercise ID
			new_relationship = Relationship(workoutID=relationship_data['workoutID'], parent=parent_key) #add required data
			new_relationship.exerciseIDs.append(relationship_data['exerciseID']) #add exercise id to list
			new_relationship.put() #add info to database
			
		
		###provide link to new relationship object and return data for error testing
		#exercise_dict = new_relationship.to_dict()
		#exercise_dict['self'] = '/relationship/' + new_relationship.key.urlsafe()
		#self.response.write(json.dumps(exercise_dict))	