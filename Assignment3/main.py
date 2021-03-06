# resources: class lectures

import webapp2
# import os
# import jinja2

# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + "/templates"))

# class MainHandler(webapp2.RequestHandler):
#     def get(self):
#         template = JINJA_ENVIRONMENT.get_template('index.html')
#         self.response.out.write(template.render())
        
app = webapp2.WSGIApplication([
    ('/insurance', 'insurance.Insurance'),
    ], debug=True)
app.router.add(webapp2.Route(r'/insurance/<iid:[0-9]+>', 'insurance.Insurance'))
app.router.add(webapp2.Route(r'/updateInsurance', 'insurance.UpdateInsurance'))
app.router.add(webapp2.Route(r'/deleteInsurance', 'insurance.DeleteInsurance'))
app.router.add(webapp2.Route(r'/updatePatient', 'patient.UpdatePatient'))
app.router.add(webapp2.Route(r'/deletePatient', 'patient.DeletePatient'))
app.router.add(webapp2.Route(r'/patient', 'patient.Patient'))
app.router.add(webapp2.Route(r'/patient/<pid:[0-9]+>', 'patient.Patient'))
app.router.add(webapp2.Route(r'/patient/<pid:[0-9]+>/insurance/<iid:[0-9]+>', 'patient.PatientInsurance'))
app.router.add(webapp2.Route(r'/delete/patient/<pid:[0-9]+>/insurance/<iid:[0-9]+>', 'patient.PatientInsuranceDelete'))
app.router.add(webapp2.Route(r'/patient/<pid:[0-9]+>/deleteInsurance/<iid:[0-9]+>', 'patient.PatientDelInsurance'))