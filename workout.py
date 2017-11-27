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
	workoutURLID = ndb.StringProperty()
	exerciseIDs = ndb.StringProperty(repeated=True) #list of relationship ids in the workout
	
	



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
		

		
		#put workout object on database. Save key.
		wURLID = new_workout.put()
		
		#add key as property so front end can easily reference and recieve key/ID via json.
		w = wURLID.get()
		w.workoutURLID = wURLID.urlsafe()
		w.put()
		
		#provide link to new workout object and return data for error testing
		workout_dict = new_workout.to_dict()
		workout_dict['self'] = '/workout/' + new_workout.key.urlsafe()
		self.response.write(json.dumps(workout_dict))	
			

	def patch(self, id=None):
		if id:
			w = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 404
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#replace data if it is there.
			if isinstance(new_data.get('name', None), basestring): 
				w.name = new_data['name']
			if isinstance(new_data.get('date', None), basestring):
				w.date = new_data['date']
			if isinstance(new_data.get('type', None), basestring):
				w.type = new_data['type']
			if isinstance(new_data.get('notes', None), basestring):
				w.notes = new_data['notes']
			
			w.put() #put new info on database
			
			w_d = w.to_dict() ###debugging
			self.response.write(json.dumps(w_d)) ###debugging
		else:
			self.response.write("patch to WorkoutHandler") #debugging
			
			
			
	def delete(self, id=None):
		#if there is an id, delete it
		if id:
			ndb.Key(urlsafe=id).delete() #delete workout
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
