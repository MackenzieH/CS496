#resources: lecture code

import webapp2
import db_models
import json
from google.appengine.ext import ndb

class Patient(webapp2.RequestHandler):
    def post(self):
        """Creates a Patient entity
        
        POST Body Variables:
        username - Required. Patient name (First and Last)
        dob - Required. Patient ate of birth
        insurance - the Insurance carrier of the patient (can have multiple)
        """
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.message = "Not acceptable, API only supports application/json MIME type"
            return
        
        new_patient = db_models.Patient()
        username = self.request.get('username', default_value=None)
        dob = self.request.get('dob', default_value=None)
        insurance = self.request.get_all('insurance[]', default_value=None)
        
        if username:
            new_patient.username = username
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request - a patient username is required"
        if dob:
            new_patient.dob = dob
        else:
            self.response.status = 400
            self.response.status_message = "Invalid request - a patient date of birth is required"
        if insurance:
            for insurance in insurance:
                new_patient.insurance.append(ndb.Key(db_models.Insurance, int(insurance)))
        key = new_patient.put()
        out = new_patient.to_dict()
        self.response.write(json.dumps(out))
        return
    
    def get(self, **kwargs):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.message = "Not acceptable, API only supports application/json MIME type"
            return
        
        #when specific key is entered
        if 'id' in kwargs:
            out = ndb.Key(db_models.Patient, int(kwargs['id'])).get().to_dict()
            self.response.write(json.dumps(out))
            
        #if no id is entered, then display all keys
        else:
            q = db_models.Patient.query()
            results = [{'key':x.key.id(), 'username':x.username} for x in q.fetch()]
            self.response.write(json.dumps(results))
            
class UpdatePatient(webapp2.RequestHandler):
    def post(self):
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.message = "Not acceptable, API only supports application/json MIME type"
            return
        
        #get the patient key
        patientID = int(self.request.get('key'))
        patient = db_models.Patient().get_by_id(int(patientID))
        
        username = self.request.get('username', default_value=None)
        dob = self.request.get('dob', default_value=None)
        insurance = self.request.get('insurance[]', default_value=None)
        
        #no changes are made to additional fields
        if username:
            patient.username = username
        if dob:
            patient.dob = dob
        if insurance:
            for insurance in insurance:
                patient.insurance.append(ndb.Key(db_models.Insurance,int(insurance)))
                
        key = patient.put()
        out = patient.to_dict()
        self.response.write(json.dumps(out))
        return
    
class DeletePatient(webapp2.RequestHandler):
    def post(self):
        #get patientID
        patientID = int(self.request.get('key'))
        patient = db_models.Patient().get_by_id(int(patientID))
        patient.key.delete()

class PatientInsurance(webapp2.RequestHandler):
    def put(self, **kwargs):
        if 'id' in kwargs:
            patient = ndb.Key(db_models.Patient, int(kwargs['id'])).get()
            if not patient:
                self.response.status = 404
                self.response.status_message = "Patient Not Found, Please Add Patient."
                return
        if 'iid' in kwargs:
            insurance = ndb.Key(db_models.Insurance, int(kwargs['iid']))
            if not patient:
                self.response.status = 404
                self.response.status_message = "Insurance Not Found, Please Add Appropriate Insurance."
                return
        if insurance not in patient.insurance:
            patient.insurance.append(insurance)
            patient.put()
        self.response.write(json.dumps(patient.to_dict()))
        return

class PatientInsuranceDelete(webapp2.RequestHandler):
    def delete(self, **kwargs):
        if 'id' in kwargs:
            patient = ndb.Key(db_models.Patient, int(kwargs['id'])).get()
            if not patient:
                self.response.status = 404
                self.response.status_message = "Patient Not Found. Please enter correct PatientID."
                return
        if 'iid' in kwargs:
            insurance = ndb.Key(db_models.Insurance, int(kwargs['iid']))
            if not patient:
                self.response.status = 404
                self.response.status_message = "Insurance Not Found. Please enter correct InsuranceID."
                return
        for c in patient.insurance:
            patient.insurance.append(insurance)
            patient.put()
            patient.insurance.remove(c)
        self.response.write(patient.insurance[0])
        s = patient.query()
        self.response(s)
        for c in patient.insurance:
            self.response.write(json.dumps(patient.insurance))
        return