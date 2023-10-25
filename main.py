from pymongo import MongoClient

import Department as Dp

cluster = input("Input your connection link") or "mongodb+srv://rboixo:Carm3n1ta@atlascluster.wxir5tb.mongodb.net/?retryWrites=true&w=majority"



client = MongoClient(cluster)

db = client.CECS323Database
collection = db.Deparments

#collection.insert_one({"Name":"Mike"})

#collection.insert_one({"name":"CECS"})



department = {
  "name": "Electrical Engineering",
  "abbreviation": "EE",
  "chair_name": "David Brown",
  "building": "SciTEch",
  "office": 111,
  "description": "The Electrical Engineering department ."
}

try:
  Dp.insert_department(department,db)
except ValueError as e:
  print(e)

# Get all of the departments in the collection.
departments = db.departments.find()

# Print the departments.
for department in departments:
  print(department)




