from pymongo import MongoClient

from Department import Department

cluster = input("Input your connection link: ") or "mongodb+srv://rboixo:Carm3n1ta@atlascluster.wxir5tb.mongodb.net/?retryWrites=true&w=majority"

database = input("Input the name of your database: ") or "CECS323Database"

client = MongoClient(cluster)

db = client[database]




Dp = Department(db)
go = True
while go:
  action = int(input("What do you want to do: \n 1:Add department \n 2:Delete department \n3: Quit"))
  if action == 1:
    Dp.add_department()
  elif action==2:
    Dp.delete_department()
  else:
    go = False


  departments = db.departments.find()

  # Print the departments.
  for department in departments:
    print(department)

# Get all of the departments in the collection.

departments = db.departments.find()

# Print the departments.
for department in departments:
  print(department)




