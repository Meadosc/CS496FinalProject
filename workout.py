#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Workout Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json


#workout
class Workout(ndb.Model):
	name = ndb.StringProperty(required=True)
	date = ndb.StringProperty(required=True)
	type = ndb.StringProperty(required=True)
	notes = ndb.StringProperty(required=True)
	
	



class WorkoutHandler(webapp2.RequestHandler):
	def get(self, id=None):
		#if there is an id, respond with workout info corresponding to that id.
		#else, give a body response saying your're at the workouthandler page
		if id:
			w = ndb.Key(urlsafe=id).get() #get the object from the database
			w_d = w.to_dict() #turn w object (workout) into a dictionary
			w_d['self'] = "/workout/" + id
			self.response.write(json.dumps(w_d))
		else: 
			workout_dict = [] #dictionary to store workout in
			for w in Workout.query().fetch(): #fetch all workout from the database
				w_d = w.to_dict() #turn each workout instance into a dictionary
				w_d['self'] = '/workout/' + w.key.urlsafe() #add a "self" link to each workout dictionary
				workout_dict.append(w_d) #save workout dictionary in larger dictionary
			self.response.write(json.dumps(workout_dict)) #return workout with links to themselves.
		
	def post(self):
		#Create parent key so we can have a workout tree
		parent_key = ndb.Key(Workout, "parent_workout")
		#get json data from post, then use "loads" to turn json into object. assign to workout_data.
		workout_data = json.loads(self.request.body)
		
		#check if required data is good. If not throw bad data error or don't input data.
		#if good add data to new_workout
		if isinstance(workout_data['name'], basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'date', 'type', and 'notes'")
		new_workout = Workout(name=workout_data['name'], parent=parent_key) #add required data
		if isinstance(workout_data.get('date', None), basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'date', 'type', and 'notes'")
		new_workout.date = workout_data['date']
		if isinstance(workout_data.get('type', None), basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'date', 'type', and 'notes'")
		new_workout.type = workout_data['type']
		if isinstance(workout_data.get('notes', None), basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'date', 'type', and 'notes'")
		new_workout.notes = workout_data['notes']
		
		#put workout object on database
		new_workout.put()
		
		#provide link to new workout object and return data for error testing
		workout_dict = new_workout.to_dict()
		workout_dict['self'] = '/workout/' + new_workout.key.urlsafe()
		self.response.write(json.dumps(workout_dict))	
			
			