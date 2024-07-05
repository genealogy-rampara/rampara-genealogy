# from re import M
# from django.forms import JSONField
from django.shortcuts import render, Http404, redirect
from django.http import Http404, JsonResponse
import csv
from django.db import transaction
from django.http import JsonResponse

# This view renders the tree.html template
def render_tree_view(request):
    return render(request, 'tree.html')

# This view displays details of a person

# Path to your CSV file

file_path = 'main/genealogy.csv'

def person_detail(request, person_id):
    # Load CSV data
    genealogy_data = load_csv_data(file_path)
    # Find the person in CSV data
    person = find_person(genealogy_data, person_id)
    print('\n\n=========================================================================================================================================')
    print('==========================================================  PERSON  =====================================================================\n')
    print(person)
    print('=========================================================================================================================================\n\n')

    if person:
        families = []
        families.append(person)
        print('\n\n=========================================================================================================================================')
        print('==========================================================  FAMILIES  ===================================================================\n')
        print(families)
        print('=========================================================================================================================================\n\n')

        # Convert children IDs to list of person dictionaries
        for family in families:
            children = []
            # Check if 'children' key exists in the family dictionary
            if 'children' in family:
                child = family['children']
                print('\n\n=========================================================================================================================================')
                print('==========================================================  CHILD  ======================================================================\n')
                print(child)
                print('=========================================================================================================================================\n\n')

                # Split the children string into individual children
                children_ids = child.split(";")
                print('\n\n=========================================================================================================================================')
                print('========================================================  CHILDREN IDS  =================================================================\n')
                print(children_ids)
                print('=========================================================================================================================================\n\n')

                # Append each child to the children list
                for c in children_ids:
                    children.append(c.strip())

                print('\n\n=========================================================================================================================================')
                print('=======================================================  LIST OF CHILDREN  ==============================================================\n')
                print(children)
                print('=========================================================================================================================================\n\n')

                my_str = ';'.join(children)
                print('\n\n=========================================================================================================================================')
                print('=======================================================  LIST OF CHILDREN CONVERTED INTO STRING  ========================================\n')
                print(my_str)
                print('=========================================================================================================================================\n\n')

                # Split the string back into a list
                childrens_ids = my_str.split(';')
                print('\n\n=========================================================================================================================================')
                print('=======================================================  CHILDRENS IDS SPLIT THE STRING BACK INTO LIST  =================================\n')
                print(childrens_ids)
                print('=========================================================================================================================================\n\n')

                # Initialize a list to store child details dictionaries
                child2 = []

                # Check if 'child_id' key exists in the family dictionary
                if 'child_id' in family:
                    print('======================================== CHI<DDDDDDDDDDDDD >>>>>>>>>>>>>>>>>>>>>>>>>',family['child_id'])
                    child_ids = family['child_id'].split(';')

                    # Iterate through each child_id and create child_details dictionary
                    for c_id in child_ids:
                        child_details = {
                            'child_id': c_id.strip(),
                        }
                        child2.append(child_details)

                    print('\n\n=========================================================================================================================================')
                    print('=====================================================  CHILD 2 ===========================================================\n')
                    print(child2)
                    print('=========================================================================================================================================\n\n')

                # Iterate through childrens_ids and construct family_details for each children_name
                for children_name in childrens_ids:
                    family_details = {
                        'children_name': children_name.strip(),
                        'child_ids2': child2,  # Use the correct child_id list for each children_name
                    }
                    families.append(family_details)

                    print('\n\n=========================================================================================================================================')
                    print('=====================================================  FAMILY DETAILS CHILDREN NAME AND CHILD ID =====================================\n')
                    print(families)
                    print('=========================================================================================================================================\n\n')

        # Continue with spouse processing and rendering as per your existing logic

                # Append family details to the families list
        spouses = []
        # Check if the person has a spouse_name
        if person.get('spouse_name'):
            # Iterate through genealogy_data to find spouses where spouse_name matches person's name
            for entry in genealogy_data:
                if person['spouse_name'] in entry['spouse_name']:
                    spouse_names = entry['spouse_name'].split(';')
                    
                    for idx, spouse_name in enumerate(spouse_names):
                        spouse_details = {
                            'spouse_name': spouse_name.strip(),
                            'spouse_fathername': entry['spouse_fathername'].split(';')[idx].strip(),
                            'spouse_village': entry['spouse_village'].split(';')[idx].strip()
                        }
                        
                        # Append spouse details to the spouses list
                        spouses.append(spouse_details)
        
        # Print debug messages
        if not spouses:
            print('\n\n=========================================================================================================================================')
            print('==========================================================  NO SPOUSE FOUND!  ====================================================================\n')
            print('=========================================================================================================================================\n\n')
        
        print('\n\n=========================================================================================================================================')
        print('==========================================================  SPOUSES  ====================================================================\n')
        print(spouses)
        print('=========================================================================================================================================\n\n')
        
        return render(request, 'person_detail.html', {
            'person': person,
            'families': families,
            'spouses': spouses
        })
        
    else:
        raise Http404("Person does not exist")


# file_path='main/genealogy.csv'
def load_csv_data(file_path):
    """
    Load genealogy data from CSV file into a list of dictionaries.
    Assumes the CSV file has headers: ID, Name, Gender, father, mother, children, spouse_name, spouse_fathername, spouse_village.
    """
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def find_person(data, person_id):
    """
    Find a person with the specified ID in the loaded genealogy data.
    """
    for person in data:
        if person['ID'] == str(person_id):
            return person
            # print('PERSON >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',person)
    # for child in data:
    #     if child['child_id'] == str(child_id):
    #         print('====================CHILD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',child)
# This view displays details of a child
# file_path = '/Users/neel2004/Desktop/family/family/main/genealogy.csv'

def find_child(data, child_id):
    """
    Find a child with the specified ID in the loaded genealogy data.
    """
    for child in data:
        if child['child_id'] == str(child_id):
            return child
            # print('CHILD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',child)

def child_detail(request, child_id):
    # Load CSV data
    genealogy_data = load_csv_data(file_path)
    # Find the child in CSV data
    child = find_child(genealogy_data, child_id)
    print('CHILD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>++++++++++++++++++++++++++++++', child)
    if child:
        # Initialize lists for families and spouses
        families = []
        spouses = []

        # Check if 'children' key exists in the child dictionary
        if 'children' in child:
            children_ids = child['children'].split(";")

            # Iterate through children IDs and construct family_details for each children_name
            for children_name in children_ids:
                family_details = {
                    'children_name': children_name.strip(),
                }
                families.append(family_details)

        # Check if the child has a spouse_name
        if child.get('spouse_name'):
            # Iterate through genealogy_data to find spouses where spouse_name matches child's spouse_name
            for entry in genealogy_data:
                if child['spouse_name'] in entry['spouse_name']:
                    spouse_names = entry['spouse_name'].split(';')

                    for idx, spouse_name in enumerate(spouse_names):
                        spouse_details = {
                            'spouse_name': spouse_name.strip(),
                            'spouse_fathername': entry['spouse_fathername'].split(';')[idx].strip(),
                            'spouse_village': entry['spouse_village'].split(';')[idx].strip()
                        }

                        # Append spouse details to the spouses list
                        spouses.append(spouse_details)

        return render(request, 'child_detail.html', {
            'child': child,
            'families': families,
            'spouses': spouses
        })

    else:
        raise Http404("Person does not exist")



def create_person(request):
    if request.method == 'POST':
        # Extract data from POST request
        new_person_data = {
            'ID': request.POST.get('ID'),
            'child_id': request.POST.get('child_id'),
            'Name': request.POST.get('Name'),
            'Gender': request.POST.get('Gender'),
            'father': '',
            'mother': '',
            'children': '',
            'spouse_name': '',
            'spouse_fathername': '',
            'spouse_village': ''
        }
        
        # Save the person details to CSV file
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                new_person_data['ID'],
                new_person_data['child_id'],
                new_person_data['Name'],
                new_person_data['Gender'],
                new_person_data['father'],
                new_person_data['mother'],
                new_person_data['children'],
                new_person_data['spouse_name'],
                new_person_data['spouse_fathername'],
                new_person_data['spouse_village']
            ])
        
        # Redirect to create spouse view or any other relevant view
        return redirect('tree_view')
    # return redirect('tree_view')
    return render(request, 'person_form.html')




# Global variable to store imported data
# global imported_data
# imported_data = []
# @transaction.atomic
# def import_data_from_csv(request):
#     global imported_data
#     if request.method == 'POST':
#         csv_file = request.FILES.get('csv_file')
#         if not csv_file or not csv_file.name.endswith('.csv'):
#             return JsonResponse({'status': 'error', 'message': 'Please upload a valid CSV file'}, status=400)
        
#         # try:
#         csv_data = csv_file.read().decode('utf-8').splitlines()
#         reader = csv.DictReader(csv_data)

#         imported_data.clear()  # Clear existing data to ensure fresh import
#         for row in reader:
#             try:
#                 if not row['ID']:
#                     continue
#                 person_id = row.get('ID')
#                 child_id = row.get('child_id', '')
#                 father_name = row.get('father', '')
#                 mother_name = row.get('mother', '')
#                 spouse_name = row.get('spouse_name', '')
#                 spouse_fathername = row.get('spouse_fathername', '')
#                 spouse_village = row.get('spouse_village', '')
                
#                 # Append each person's data to imported_data with an empty children list
#                 imported_data.append({
#                     'ID': person_id,
#                     'child_id': child_id,
#                     'Name': row['Name'],
#                     'Gender': row['Gender'],
#                     'Father': father_name,
#                     'Mother': mother_name,
#                     'Spouse Name': spouse_name,
#                     'Spouse Father Name': spouse_fathername,
#                     'Spouse Village': spouse_village,
#                     'children': []  # Initialize an empty list for children
#                 })
            
#             except Exception as e:
#                 return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
#         # except Exception as e:
#         #     return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
#         return redirect('tree_view')
#         # return JsonResponse({'status': 'success', 'message': 'Data imported successfully'})
    
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

global imported_data
imported_data = []
@transaction.atomic
def import_data_from_csv(request):
    global imported_data
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid CSV file'}, status=400)
        try:
            # Ensure proper decoding and handle potential BOM
            csv_data = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(csv_data)
            imported_data.clear()  # Clear existing data to ensure fresh import
            for row in reader:
                try:
                    person_id = row.get('ID', '').strip()
                    if not person_id:
                        continue
                    imported_data.append({
                        'ID': person_id,
                        'child_id': row.get('child_id', '').strip(),
                        'Name': row.get('Name', '').strip(),
                        'Gender': row.get('Gender', '').strip(),
                        'Father': row.get('father', '').strip(),
                        'Mother': row.get('mother', '').strip(),
                        'Spouse Name': row.get('spouse_name', '').strip(),
                        'Spouse Father Name': row.get('spouse_fathername', '').strip(),
                        'Spouse Village': row.get('spouse_village', '').strip(),
                        'children': []  # Initialize an empty list for children
                    })
                except Exception as e:
                    # Log the error for debugging purposes
                    print(f"Error processing row {row}: {e}")
                    return JsonResponse({'status': 'error', 'message': f"Error processing row: {e}"}, status=500)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error reading file: {e}"}, status=500)
        return redirect('tree_view')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



def build_tree(person, data):
    # Initialize the tree structure for the current person
    person_tree = {
        'name': person['Name'],
        'id': person['ID'],
        'child_id': person['child_id'],
        'gender': person['Gender'],
        'children': []
    }
    
    # Find children of the current person
    children = [child for child in data if child['Father'] == person['Name']]
    
    # Recursively build the tree for each child
    for child in children:
        person_tree['children'].append(build_tree(child, data))
    
    # Additionally, find female children who have children and add their children
    female_children_with_children = [child for child in data if child['Mother'] == person['Name']]
    
    for female_child in female_children_with_children:
        person_tree['children'].append(build_tree(female_child, data))
    return person_tree

def generate_tree_data(request):
    global imported_data
    
    # Ensure imported_data is populated before accessing it
    if not imported_data:
        return JsonResponse({'status': 'error', 'message': 'Data not imported yet'}, status=404)
    
    try:
        if request.method == 'GET':
            # Find the root person (assuming the first person is the root)
            root_person = imported_data[0]
            
            # Build the tree starting from the root person
            tree_data = build_tree(root_person, imported_data)
            
            # Return the tree data as JSON response
            return JsonResponse(tree_data, safe=False)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)  
    
def get_tree_data(request):
    global imported_data
    if not imported_data:
        return JsonResponse({'status': 'error', 'message': 'No data available'}, status=400)
    try:
        # Find the root person with the name "Anandsinhji"
        root_person = next((person for person in imported_data if person['Name'] == 'Anandsinhji'), None)
        if root_person:
            # Return only the name of the root person
            return JsonResponse({'name': root_person['Name']}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Root person not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def d3_collapsible_tree(request):
    global imported_data
    if not imported_data:
        return JsonResponse({"error": "No data available"}, status=400)
    root_person_name = "Anandsinhji"
    root_person = next((item for item in imported_data if item['Name'] == root_person_name), None)
    if not root_person:
        return JsonResponse({"error": "Root person not found"}, status=404)
    # Function to recursively filter and build the tree with male individuals
    def build_tree_with_male(person):
        return {
            'name': person['Name'],
            'id': person['ID'],
            'child_id': person['child_id'],
            'gender': person['Gender'],
            'children': [
                build_tree_with_male(child)
                for child in imported_data
                if child['Father'] == person['Name'] and child['Gender'] == 'M'
            ]
        }
    # Generate the tree data starting from the root person
    tree_data = build_tree_with_male(root_person)
    return JsonResponse(tree_data)


def save_person_details(request):
    if request.method == 'POST':
        imported_data = imported_data(request.POST)
        if imported_data.is_valid():
            imported_data = imported_data.save()
            # Redirect to import_data_from_csv view
            return redirect('tree_view')
        else:
            # Handle form errors if needed
            return JsonResponse({'status': 'error', 'message': 'Form data is not valid.'}, status=400)
    else:
        # Handle GET request if needed
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

