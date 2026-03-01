# Example Python Code to Insert a Document
from datetime import date
from pymongo import MongoClient 
from bson.objectid import ObjectId 

#UPDATE--removed Entry class, TypedDict
    

class AnimalShelter(object): 
    """ CRUD operations for Animal collection in MongoDB """   
    

    def __init__(self,username,password):
        # Initializing the MongoClient. This helps to access the MongoDB 
        # databases and collections. This is hard-wired to use the aac 
        # database, the animals collection, and the aac user. 
        # 
        # You must edit the password below for your environment. 
        # 
        # Connection Variables 
        #
        HOST = 'localhost'
        PORT = 27017
        USER = username
        PASS = password
        DB = 'aac'
        COL = 'animals'       
        self.client = MongoClient(f'mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT)) 
        self.database = self.client['%s' % (DB)] 
        self.collection = self.database['%s' % (COL)]
        
        # helper method to get next available object id for document insertion returns a new ID
    def get_New_Id(self)->ObjectId:
        new_id = ObjectId()
        return new_id
    
    # Insertion method to the collection, data is dict
    # data follows the form {'key':'value'}
    def create(self,data)->None:
        #check if data is populated
        if data is None:
            return False
        id = data['_id'] if data.get('_id') is not None else self.get_New_Id()
        already_exists = self.database.animals.find_one(id) is not None
        if data is not None and not already_exists:
            data['_id'] = id
            try:
                self.database.animals.insert_one(data)
            except:
                return False
            return True
        else:
            return False

    # Create method to implement the R in CRUD.\
    def read(self, query_data)->list:
        # create the cursor object
        cursor = self.database.animals.find(query_data)
        result = list(cursor)
        return result
    
    #queries are dicts, many default is false
    def update(self, query_data, update_action,many=False)->int:
        if many:
            result = self.database.animals.update_many(query_data,update_action)
        else:
            result = self.database.animals.update_one(query_data,update_action)
        return result.modified_count
        
    #queries are dicts, many default is false
    def delete(self, query,many=False)->int:
        if many:
            result = self.database.animals.delete_many(query)
        else:
            result = self.database.animals.delete_one(query)
        return result.deleted_count
        
        
        