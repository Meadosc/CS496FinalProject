#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

#-----------------------------------
#Exercise Class and handler for main.py
#-----------------------------------

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json


#Exercise
class Exercise(ndb.Model):
	name = ndb.StringProperty(required=True)
	weight = ndb.IntegerProperty(required=True)
	sets = ndb.IntegerProperty(required=True)
	reps = ndb.IntegerProperty(required=True)
	exerciseURLID = ndb.StringProperty()

	
	

class ExerciseHandler(webapp2.RequestHandler):
	def get(self, id=None):
		#if there is an id, respond with exercise info corresponding to that id.
		#else, give a body response saying your're at the ExerciseHandler page
		if id:
			e = ndb.Key(urlsafe=id).get() #get the object from the database
			e_d = e.to_dict() #turn e object (exercise) into a dictionary
			e_d['self'] = "/exercise/" + id
			self.response.write(json.dumps(e_d))
		else: 
			exercise_dict = [] #dictionary to store exercise in
			for e in Exercise.query().fetch(): #fetch all exercise from the database
				e_d = e.to_dict() #turn each exercise instance into a dictionary
				###e_d['self'] = '/exercise/' + e.key.urlsafe() #add a "self" link to each exercise dictionary
				exercise_dict.append(e_d) #save exercise dictionary in larger dictionary
			self.response.write(json.dumps(exercise_dict)) #return exercise with links to themselves.
		
	def post(self):
		#Create parent key so we can have a exercise tree
		parent_key = ndb.Key(Exercise, "parent_exercise")
		#get json data from post, then use "loads" to turn json into object. assign to exercise_data.
		exercise_data = json.loads(self.request.body)
		
		#check if required data is good. If not throw bad data error or don't input data.
		#if good add data to new_exercise
		if isinstance(exercise_data['name'], basestring) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'weight', 'sets', and 'reps'")
		new_exercise = Exercise(name=exercise_data['name'], parent=parent_key) #add required data
		if isinstance(exercise_data.get('weight', None), int) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'weight', 'sets', and 'reps'")
		new_exercise.weight = exercise_data['weight']
		if isinstance(exercise_data.get('sets', None), int) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'weight', 'sets', and 'reps'")
		new_exercise.sets = exercise_data['sets']
		if isinstance(exercise_data.get('reps', None), int) == False:
			webapp2.abort(400,"Bad user input. Give json string with 'name', 'weight', 'sets', and 'reps'")
		new_exercise.reps = exercise_data['reps']
		
		
		#put exercise object on database
		eURLID = new_exercise.put()
		
		#add key as property so front end can easily reference and recieve key/ID via json.
		e = eURLID.get()
		e.exerciseURLID = eURLID.urlsafe()
		e.put()
		
		#provide link to new exercise object and return data for error testing
		exercise_dict = new_exercise.to_dict()
		exercise_dict['self'] = '/exercise/' + new_exercise.key.urlsafe()
		self.response.write(json.dumps(exercise_dict))	
			
			
	def patch(self, id=None):
		if id:
			e = ndb.Key(urlsafe=id).get() #get the object instance from the database
			if self.request.body: #check if user sent data. If not, abort error 404
				new_data = json.loads(self.request.body)
			else:
				webapp2.abort(400,"Bad user input")
			
			#replace data if it is there.
			if isinstance(new_data.get('name', None), basestring): 
				e.name = new_data['name']
			if isinstance(new_data.get('weight', None), int):
				e.weight = new_data['weight']
			if isinstance(new_data.get('sets', None), int):
				e.sets = new_data['sets']
			if isinstance(new_data.get('reps', None), int):
				e.reps = new_data['reps']
			
			e.put() #put new info on database
			
			e_d = e.to_dict() ###debugging
			self.response.write(json.dumps(e_d)) ###debugging
		else:
			self.response.write("patch to ExerciseHandler") #debugging
			
	################################
	### needs delete handler
	###############################
			















