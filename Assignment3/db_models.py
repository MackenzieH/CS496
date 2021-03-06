#resources: class lectures

from google.appengine.ext import ndb

class Model(ndb.Model):
    def to_dict(self):
        d = super(Model, self).to_dict()
        d['key'] = self.key.id()
        return d
    
#Patient and Insurance have a relationship
class Patient(Model):
    username = ndb.StringProperty()
    dob = ndb.DateProperty()
    insurance = ndb.KeyProperty(kind="Insurance", repeated=True)
    
    def to_dict(self):
        d = super(Patient, self).to_dict()
        d['key'] = self.key.id()
        d['insurance'] = [c.id() for c in d['insurance']]
        return d

class Insurance(Model):
    name = ndb.StringProperty(required=True)
    effec = ndb.DateProperty(required=True)
    
    def to_dict(self):
        d = super(Insurance, self).to_dict()
        d['key'] = self.key.id()
        return d