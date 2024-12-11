import datetime as dt

class Booking:
    def __init__(self):
        self.user_id = ''
        self.name =''
        self.phone_number = ''
        self.time_slot = 0
        self.id = ''
        self.datetime = None


    #convert from object to dict to upload to db
    def to_dict(self):
        return {
            'name' : self.name,
            'phonenumber' : self.phone_number,
            'timeslot' : self.time_slot,
            'userid' : self.user_id   
        }

    #convert data from db to object
    def from_dict(self,dict,id):
        self.name = dict['name']
        self.phone_number = dict['phonenumber']  
        self.time_slot = int(dict['timeslot'])    
        self.user_id = dict['userid']  
        self.id = id
        self.datetime = dt.datetime.fromtimestamp(self.time_slot)
        return self

    def __str__(self):
        return f"{self.id} - {self.datetime.strftime('%d-%m-%Y %H:%M')}"  
        # return self.id + " - " + str(self.time_slot)