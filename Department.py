from pymongo import MongoClient

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


def insert_department(department,database):
  """Inserts a department document into the collection."""

  # Validate the department document.
  validate_department(department)

  # Check for existing departments with the same abbreviation, chair name, building, and office.
  existing_departments = database.departments.find({
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
  database.departments.insert_one(department)


def add_department(database):

  name = input("Department name --> ")
  abbreviation = input("Department's abbreviation --> ")
  chairName = input("Department Chair name --> ")
  building = input("Building name --> ")
  office = int(input("Office number --> "))
  description = input("Description of department --> ")

  department = {
    "name": name,
    "abbreviation": abbreviation,
    "chair_name": chairName,
    "building": building,
    "office": office,
    "description": description
  }

  while not validate_department(department):
    name = input("Department name --> ")
    abbreviation = input("Department's abbreviation --> ")
    chairName = input("Department Chair name --> ")
    building = input("Building name --> ")
    office = int(input("Office number --> "))
    description = input("Description of department --> ")

    department = {
      "name": name,
      "abbreviation": abbreviation,
      "chair_name": chairName,
      "building": building,
      "office": office,
      "description": description
    }

  # Check for existing departments with the same abbreviation, chair name, building, and office.
  existing_departments = database.departments.find({
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
  database.departments.insert_one(department)


