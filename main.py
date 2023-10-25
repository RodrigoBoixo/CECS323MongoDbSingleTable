from pymongo import MongoClient

cluster = input("Input your connection link") or "mongodb+srv://rboixo:Carm3n1ta@atlascluster.wxir5tb.mongodb.net/?retryWrites=true&w=majority"



client = MongoClient(cluster)

db = client.CECS323Database
collection = db.Deparments

#collection.insert_one({"Name":"Mike"})

#collection.insert_one({"name":"CECS"})

def validate_department(department):
  """Validates a department document."""

  # Check if the required fields are present.
  if not department.get("abbreviation"):
    raise ValueError("The department abbreviation is required.")
  if not department.get("chair_name"):
    raise ValueError("The department chair name is required.")
  if not department.get("building"):
    raise ValueError("The department building is required.")
  if not department.get("office"):
    raise ValueError("The department office is required.")
  if not department.get("description"):
    raise ValueError("The department description is required.")

  # Check the maximum lengths of the fields.
  if len(department["name"]) > 50:
    raise ValueError("The department name must be no longer than 50 characters.")
  if len(department["abbreviation"]) > 6:
    raise ValueError("The department abbreviation must be no longer than 6 characters.")
  if len(department["chair_name"]) > 80:
    raise ValueError("The department chair name must be no longer than 80 characters.")
  if len(department["building"]) > 10:
    raise ValueError("The department building must be no longer than 10 characters.")
  if len(department["description"]) > 80:
    raise ValueError("The department description must be no longer than 80 characters.")

  # Return the validated department document.
  return department

def cursor_to_list(cursor):
  """Converts a Cursor object to a list."""

  list = []
  for document in cursor:
    list.append(document)
  return list


def insert_department(department):
  """Inserts a department document into the collection."""

  # Validate the department document.
  validate_department(department)

  # Check for existing departments with the same abbreviation, chair name, building, and office.
  existing_departments = db.departments.find({
    "$or": [
      {"abbreviation": department["abbreviation"]},
      {"chair_name": department["chair_name"]},
      {"building": department["building"], "office": department["office"]},
    ]
  })

  # Convert the Cursor object to a list.
  existing_departments_list = cursor_to_list(existing_departments)

  # Count the number of existing departments.
  num_existing_departments = len(existing_departments_list)

  if num_existing_departments > 0:
    raise ValueError("There is already a department with the same abbreviation, chair name, building, or office.")

  # Insert the department document into the collection.
  db.departments.insert_one(department)


department = {
  "name": "Electrical Engineering",
  "abbreviation": "EE",
  "chair_name": "David Brown",
  "building": "SciTEch",
  "office": 111,
  "description": "The Electrical Engineering department ."
}

try:
  insert_department(department)
except ValueError as e:
  print(e)

# Get all of the departments in the collection.
departments = db.departments.find()

# Print the departments.
for department in departments:
  print(department)




