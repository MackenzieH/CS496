#resources: lecture code
from google.appengine.ext import ndb
import webapp2
import db_models
import json

#to add insurance AND to view insurance(s)
class Insurance(webapp2.RequestHandler):
    def post(self):
        #create a new insurance to be added to database
        new_insurance = db_models.Insurance()
        name = self.request.get('name', default_value=None)
        effec = self.request.get('effec', default_value=None)

        #check to make sure required fields are entered correctly
        #if not, errors will be displayed
        if name:
            new_insurance.name = name
        else:
            self.response.status = 400
            self.response.status_message = "Error: Insurance Name Required."  
        if effec:        
            new_insurance.effec = effec
        else:
            self.response.status = 400
            self.response.status_message = "Error: Insurance Effective Date Required."

        #add insurance to database, get key.
        key = new_insurance.put()
        out = new_insurance.to_dict()
        self.response.write(out)
        return

    def get(self, **kwargs):
        #when specific insuranceID (key) is entered, just display one insurance information
        if 'iid' in kwargs:
            out = ndb.Key(db_models.Insurance, int(kwargs['iid'])).get().to_dict()
            self.response.write(json.dumps(out))

        #when no specific key is entered then display out all keys in database
        #will display key, name, effec
        else:
            q = db_models.Insurance.query()
            results = [{'key':x.key.id(), 'name':x.name, 'effec':x.effec} for x in q.fetch()]
            self.response.write(json.dumps(results))

#to update current insurance in database
class UpdateInsurance(webapp2.RequestHandler):
    def post(self):
        # verify the application/json request
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API service requires application/json"
            return
        
        #get insurance key(ID) 
        insuranceID = int(self.request.get('key'))
        insurance = db_models.Insurance().get_by_id(int(insuranceID))

        name = self.request.get('name', default_value=None)
        effec = self.request.get('effec', default_value=None)
                
        #if nothing is entered in fields, then nothing is altered
        if name:
            insurance.name = name
        if effec:
            insurance.effec = effec
                    
        key = insurance.put()
        out = insurance.to_dict()
        self.response.write(json.dumps(out))
        return

class DeleteInsurance(webapp2.RequestHandler):
    def post(self):
        # verify the application/json request
        if 'application/json' not in self.request.accept:
            self.response.status = 406
            self.response.status_message = "API service requires application/json"
            return
        
        #get insurance key(ID) 
        insuranceID = int(self.request.get('key'))
        insurance = db_models.Insurance().get_by_id(int(insuranceID))
        insurance.key.delete()