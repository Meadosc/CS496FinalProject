#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Relationship Class and handler for main.py
###currently not used. Created more issues than it solved.
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json
from workout import Workout
from exercise import Exercise

#Relationship
class Relationship(ndb.Model):
	relationshipURLID = ndb.StringProperty()
	workoutID = ndb.StringProperty(required=True)
	exerciseID0 = ndb.StringProperty()
	exerciseID1 = ndb.StringProperty()
	exerciseID2 = ndb.StringProperty()
	exerciseID3 = ndb.StringProperty()
	exerciseID4 = ndb.StringProperty()
	

	
	

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
			webapp2.abort(400,"Bad user input. Give json string with 'workoutID', and 'exerciseID0', 'exerciseID1' 'exerciseID2' 'exerciseID3' 'exerciseID4'")

			

		# Need to check if a relationship for the workout already exists. If so, append exercise.
		# If not, create relationship then add workout and exercise.	
		doesExist = 0 #flag for if the workout already exists.
		for r in Relationship.query().fetch():
			if relationship_data['workoutID'] == r.workoutID:
				doesExist = 1
				### below code still assumes list.
				r.exerciseIDs.append(relationship_data['exerciseID']) #add exercise ID to already existing relationship 
				r.put() #add info to database

		if doesExist == 0: #if the workout did not already have a relationship, add relationship and exercise ID
			new_relationship = Relationship(workoutID=relationship_data['workoutID'], parent=parent_key) #add required data
			new_relationship.exerciseID0 = relationship_data['exerciseID0']
			new_relationship.exerciseID1 = relationship_data['exerciseID1']
			new_relationship.exerciseID2 = relationship_data['exerciseID2']
			new_relationship.exerciseID3 = relationship_data['exerciseID3']
			new_relationship.exerciseID4 = relationship_data['exerciseID4']
			rURLID = new_relationship.put() #add info to database
			
			robj = rURLID.get()
			robj.relationshipURLID = rURLID.urlsafe()
			robj.put()
			
		
		###provide link to new relationship object and return data for error testing
		#exercise_dict = new_relationship.to_dict()
		#exercise_dict['self'] = '/relationship/' + new_relationship.key.urlsafe()
		#self.response.write(json.dumps(exercise_dict))	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		