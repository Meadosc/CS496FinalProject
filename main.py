#CS496 Mobile and Web development Final Project: Hybrid
# Cord Meados 2017

# [START imports]
from google.appengine.ext import ndb
import webapp2
import json

from workout import Workout, WorkoutHandler
from exercise import Exercise, ExerciseHandler
from add import AddHandler
from remove import RemoveHandler





# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
		self.response.write({"title":"Final Project main page"})		### debug
# [END main_page]


# [START app]

#allow patch() 
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
#end allow patch()

app = webapp2.WSGIApplication([
    ('/', MainPage),	
	('/workout', WorkoutHandler),
	('/workout/([\w-]+)', WorkoutHandler),
	('/exercise', ExerciseHandler),
	('/exercise/([\w-]+)', ExerciseHandler),
	('/workout/([\w-]+)/add', AddHandler),
	('/workout/([\w-]+)/remove', RemoveHandler),
], debug=True)
# [END app] 