# import pandas as pd
# from main.models import Person, Family, SpouseInfo

# def run():
#     # Path to your CSV file
#     csv_file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
#     # Load the CSV file
#     try:
#         df = pd.read_csv(csv_file_path)
#     except FileNotFoundError:
#         print(f"Error: The file at path {csv_file_path} was not found.")
#         return
#     except pd.errors.ParserError:
#         print(f"Error: There was a parsing error while reading the CSV file at path {csv_file_path}.")
#         return
    
#     # Print column names for debugging
#     print("CSV Columns:", df.columns.tolist())
    
#     required_columns = ['ID','Name','Gender','father_name','mother_name','spouse_name','spouse_fathername','spouse_village','children_names']
    
#     # Check if all required columns are present in the CSV
#     for column in required_columns:
#         if column not in df.columns:
#             print(f"Error: Missing required column '{column}' in CSV file.")
#             return

#     for index, row in df.iterrows():
#         # Fetch or create Person
#         person, created = Person.objects.get_or_create(name=row['Name'], defaults={'gender': row['Gender']})
#         if not created:
#             # Update existing person details
#             person.gender = row['Gender']
#             person.save()

#         # Fetch or create Family for the father and mother
#         father, _ = Person.objects.get_or_create(name=row['father_name'], defaults={'gender': 'M'})
#         mother, _ = Person.objects.get_or_create(name=row['mother_name'], defaults={'gender': 'F'})
#         family, _ = Family.objects.get_or_create(father=father, mother=mother)
        
#         # Add person as a child to the family (if not already added)
#         if person not in family.children.all():
#             family.children.add(person)
        
#         # Handle children data
#         children_names = row['children_names'].split(',') if pd.notna(row['children_names']) else []
#         for child_name in children_names:
#             child_name = child_name.strip()
#             if child_name:
#                 child, child_created = Person.objects.get_or_create(name=child_name)
#                 if child not in family.children.all():
#                     family.children.add(child)

#         # Fetch or create SpouseInfo
#         if pd.notna(row['spouse_name']):
#             spouse_info, created = SpouseInfo.objects.get_or_create(person=person, defaults={
#                 'spouse_name': row['spouse_name'],
#                 'spouse_fathername': row['spouse_fathername'],
#                 'spouse_village': row['spouse_village']
#             })
#             if not created:
#                 # Update existing spouse info details
#                 spouse_info.spouse_name = row['spouse_name']
#                 spouse_info.spouse_fathername = row['spouse_fathername']
#                 spouse_info.spouse_village = row['spouse_village']
#                 spouse_info.save()

#         # Print success messages
#         print(f"Person {row['Name']} processed successfully")
#         print(f"Family of {father.name} and {mother.name} processed successfully")
#         print(f"Spouse Info for {row['Name']} processed successfully")
#         print(f"Children: {children_names} processed successfully")
#         print("------------------------------------------------")
# import pandas as pd
# from main.models import Person, Family, SpouseInfo

# def run():
#     # Path to your CSV file
#     csv_file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
#     # Load the CSV file
#     try:
#         df = pd.read_csv(csv_file_path)
#     except FileNotFoundError:
#         print(f"Error: The file at path {csv_file_path} was not found.")
#         return
#     except pd.errors.ParserError:
#         print(f"Error: There was a parsing error while reading the CSV file at path {csv_file_path}.")
#         return
    
#     # Print column names for debugging
#     print("CSV Columns:", df.columns.tolist())
    
#     required_columns = ['ID', 'Name', 'Gender', 'father', 'mother', 'children', 'spouse_name', 'spouse_fathername', 'spouse_village']
    
#     # Check if all required columns are present in the CSV
#     for column in required_columns:
#         if column not in df.columns:
#             print(f"Error: Missing required column '{column}' in CSV file.")
#             return

#     for index, row in df.iterrows():
#         # Fetch or create Person
#         person, created = Person.objects.get_or_create(name=row['Name'], defaults={'gender': row['Gender']})
#         if not created:
#             # Update existing person details
#             person.gender = row['Gender']
#             person.save()

#         # Fetch or create Family for the father and mother
#         father, _ = Person.objects.get_or_create(name=row['father'], defaults={'gender': 'M'})
#         mother, _ = Person.objects.get_or_create(name=row['mother'], defaults={'gender': 'F'})
#         family, _ = Family.objects.get_or_create(father=father, mother=mother)
        
#         # Add person as a child to the family (if not already added)
#         if person not in family.children.all():
#             family.children.add(person)
        
#         # Handle children data
#         children = row['children'].split(',') if pd.notna(row['children']) else []
#         for child in children:
#             child = child.strip()
#             if child:
#                 child, child_created = Person.objects.get_or_create(name=child)
#                 # Find or create family where this person is a parent
#                 if person.gender == 'M':
#                     child_family, _ = Family.objects.get_or_create(father=person)
#                 else:
#                     child_family, _ = Family.objects.get_or_create(mother=person)
#                 if child not in child_family.children.all():
#                     child_family.children.add(child)

#         # Fetch or create SpouseInfo
#         if pd.notna(row['spouse_name']):
#             spouse_info, created = SpouseInfo.objects.get_or_create(person=person, defaults={
#                 'spouse_name': row['spouse_name'],
#                 'spouse_fathername': row['spouse_fathername'],
#                 'spouse_village': row['spouse_village']
#             })
#             if not created:
#                 # Update existing spouse info details
#                 spouse_info.spouse_name = row['spouse_name']
#                 spouse_info.spouse_fathername = row['spouse_fathername']
#                 spouse_info.spouse_village = row['spouse_village']
#                 spouse_info.save()

#         # Print success messages
#         print(f"Person {row['Name']} processed successfully")
#         print(f"Family of {father.name} and {mother.name} processed successfully")
#         print(f"Spouse Info for {row['Name']} processed successfully")
#         print(f"Children: {children} processed successfully")
#         print("------------------------------------------------")

