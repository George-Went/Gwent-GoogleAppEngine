import datetime
import jinja2
import os 
import webapp2
import models

from google.appengine.api import users

template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
#This gloabal variable allows the template to be read across the 
#application, it tells the filesystemloader that the template are in the 
#current directory

class MainPage(webapp2.RequestHandler):
    def get(self):
        current_time = datetime.datetime.now()
        user = users.get_current_user()
        login_url = users.create_login_url(self.request.path)
        logout_url = users.create_logout_url(self.request.path)
        userPreferances = models.get_userPreferances()

        if userPreferances: 
            current_time += datetime.timedelta(
                0, 0, 0, 0, 0, userPreferances.tz_offset)

        template = template_env.get_template('home.html')
        context = {
            'current_time': current_time,
            'user': user,
            'login_url': login_url,
            'logout_url': logout_url,
            'userPreferances': userPreferances,
        } 
        self.response.out.write(template.render(context))

application = webapp2.WSGIApplication([('/', MainPage)],
                                        debug=True)
#The Web Server Gateway Interface is part of the webapp2 framework 
#It is similar to the Django framework1`