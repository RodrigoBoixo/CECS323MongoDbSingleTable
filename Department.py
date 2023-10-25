from pymongo import MongoClient

class Department:

  def __init__(self, database):
    self.database = database
    self.collection = database["departments"]

  def validate_department(self,department):
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

  def cursor_to_list(self,cursor):
    """Converts a Cursor object to a list."""

    list = []
    for document in cursor:
      list.append(document)
    return list

  def existing_abbreviation(self,department):
    existing_departments = self.database.departments.find({"abbreviation": department["abbreviation"]})
    if existing_departments.count_documents() > 0:
      return 1

  def existing_chair(self,department):
    existing_departments = self.database.departments.find({"chair_name": department["chair_name"]})
    if existing_departments.count_documents() > 0:
      return 1

  def existing_building_and_office(self,department):
    existing_departments = self.database.departments.find({
      "building": department["building"],
      "office": department["office"],
    })
    if existing_departments.count_documents() > 0:
      return 1

  def exists(self,department):
    existing_departments = self.database.departments.find({
      "$or": [
        {"abbreviation": department["abbreviation"]},
        {"chair_name": department["chair_name"]},
        {"building": department["building"], "office": department["office"]},
      ]
    })

    # Convert the Cursor object to a list.
    existing_departments_list = self.cursor_to_list(existing_departments)

    # Count the number of existing departments.
    num_existing_departments = len(existing_departments_list)

    if num_existing_departments > 0:
      return 1

  def add_department(self):

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

    # Get the departments collection from the database
    departments_collection = self.database.get_collection("departments")


    # Check for existing departments with the same abbreviation
    if self.exists(department):
      print("There is already a department with the same abbreviation, chair, or building+ office.")
      return

    # Insert the department document into the collection
    departments_collection.insert_one(department)

  def delete_department(self):
    """Deletes a department from the database, using only the abbreviation as a search criterion.

    Args:
      abbreviation: The abbreviation of the department to delete.
    """

    # Get the departments collection from the database
    departments_collection = self.database.get_collection("departments")
    abb = input("Enter the abbreviation of the department you want to delete: ")

    existing_departments = self.database.departments.find({
      "$or": [
        {"abbreviation": (abb)}]

    })

    # Convert the Cursor object to a list.
    existing_departments_list = self.cursor_to_list(existing_departments)

    # Count the number of existing departments.
    num_existing_departments = len(existing_departments_list)

    if num_existing_departments > 0:
      departments_collection.delete_one({
        "abbreviation": abb,
      })
    else:
      print("No department exists with that abbreviation")




