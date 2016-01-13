from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from app import app
import os
from glob import glob

db = SQLAlchemy(app) #global db object - we assume we'll be dealing with one database at a time

class Test(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    
    def __init__(self,data):
        self.data = data
        self.timestamp = datetime.now()
    def __repr__(self):
        return "<Data %r>" % self.data

class Node:
    def __init__(self,name,next=None,prev=None):
        self.name = name
        self.next = next
        self.prev = prev
        self.created_at = datetime.now()
        self.create_db()

    def create_db(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databases/"+self.name+".db"
        db.create_all()
        
    def __str__(self):
        return repr(self.name)
    
class LinkedList:
    def __init__(self):
        self.head = Node("0")
        self.tail = Node("1")
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 3 

    def append(self):
        cur = self.tail
        cur_name = int(self.tail.name)
        new_node = Node(str(cur_name+1),next=None,prev=self.tail)
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1

    def db_renames(self):
        os.chdir("databases")
        dbs = glob("*.db")
        db_numbers = [int(elem.split(".db")[0]) for elem in dbs]
        db_numbers.sort()
        total_range = range(self.size)
        
        missing = [elem for elem in total_range if not elem in db_numbers][0]  
        missing -= 1
        start = False
        for db in dbs:
            name = int(db.strip(".")[0])
            if name == missing:
                start = True
            if start:
                name -= 1
                os.rename(db,str(name)+".db")
        os.chdir("..")
            
    def fill_holes(self):
        self.db_renames()
        cur = self.head
        counter = 0
        while cur:
            cur.name = str(counter)
            counter += 1
            cur = cur.next
            
    def delete(self,name):
        cur = self.head
        node_found = False
        while cur.next:
            if cur.name == name:
                node_found = True
                break
            cur = cur.next
        if node_found:
            new_next = cur.next
            prev_node = cur.prev
            prev_node.next = new_next
            new_next.prev = prev_node
            self.size -= 1
        os.chdir("databases")
        os.remove(name+".db")
        os.chdir("..")
            
    def pprint(self):
        cur = self.head
        while cur:
            print cur
            cur = cur.next
    def delete_from(self,name):
        #delete everything after the current node
        pass
    def delete_to(self,name):
        #delete everything up to the current node
        pass
    #detach head
