from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import csv
from django.db import transaction
from django.http import JsonResponse
from django.core.cache import cache
# This view renders the tree.html template
def render_tree_view(request):
    imported_data = cache.get('imported_data')
    if not imported_data:
        imported_data = []
    print("Imported Data:", imported_data)
    return render(request, 'tree.html', {'imported_data': imported_data})

def note(request):
    return render(request, 'note.html')

def search_person(request):
    query = request.GET.get('q')
    print("QUERY : ",query)
    genealogy_data = load_csv_data(file_path)
    if query:
        try:
            person = next(item for item in genealogy_data if item["Name"].lower() == query.lower()) 
            return redirect('person_detail', person_id=person["ID"])
        except StopIteration:
            return HttpResponse('<center><h1>PERSON NOT FOUND</h1></center><br><center><a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">HOME</a></center>')
    return redirect('home')  
# This view displays details of a person

# Path to your CSV file

file_path = 'main/genealogy.csv'

def person_detail(request, person_id):
    # Load CSV data
    genealogy_data = load_csv_data(file_path)
    # Find the person in CSV data
    person = find_person(genealogy_data, person_id)
    if person:
        print('\n\n=========================================================================================================================================')
        print('==========================================================  PERSON  =====================================================================\n')
        print(person)
        print('=========================================================================================================================================\n\n')
        # Get all person IDs
        total_count_ids, total_ids = count_unique_ids(genealogy_data)
        total_ids = sorted(map(int, total_ids))
        print('\n\n=========================================================================================================================================')
        print('=========================================================  Total SORTED IDS  ============================================================\n')
        print(total_ids)
        print('=========================================================================================================================================\n\n')
        person_id = int(person_id)
        print('\n\n=========================================================================================================================================')
        print('=========================================================  PERSON ID  ===================================================================\n')
        print(person_id)
        print('=========================================================================================================================================\n\n')
        current_index = total_ids.index(person_id)
        print('\n\n=========================================================================================================================================')
        print('===========================================  CURRENT INDEX (PERSON ID INDEX IN THE LIST) ================================================\n')
        print(current_index)
        print('=========================================================================================================================================\n\n')
        previous_person_id = total_ids[current_index - 1] if current_index > 0 else None
        print('\n\n=========================================================================================================================================')
        print('======================================================  PREVIOUS PERSON ID  =============================================================\n')
        print(previous_person_id)
        print('=========================================================================================================================================\n\n')
        next_person_id = total_ids[current_index + 1] if current_index < len(total_ids) - 1 else None
        print('\n\n=========================================================================================================================================')
        print('======================================================  NEXT PERSON ID  =================================================================\n')
        print(next_person_id)
        print('=========================================================================================================================================\n\n')
        
        families = []

        # Check if 'children' key exists in the person dictionary
        if 'children' in person:
            children = person['children'].split(';')
            print('\n\n=========================================================================================================================================')
            print('=======================================================  CHILDREN NAMES  ================================================================\n')
            print(children)
            print('=========================================================================================================================================\n\n')
            child_ids = person['child_id'].split(';') if 'child_id' in person else []
            print('\n\n=========================================================================================================================================')
            print('========================================================  CHILD IDS  ====================================================================\n')
            print(child_ids)
            print('=========================================================================================================================================\n\n')
            for idx, child_name in enumerate(children):
                child_id = child_ids[idx].strip() if idx < len(child_ids) else None
                print('\n\n=========================================================================================================================================')
                print('========================================================  CHILD ID AFTER SEPARATING  ====================================================\n')
                print(child_id)
                print('=========================================================================================================================================\n\n')
                family_details = {
                    'children_name': child_name.strip(),
                    'child_ids2': child_id,
                    'family_type': 'father' if person['Gender'] == 'M' else 'mother'
                }
                families.append(family_details)
                print('\n\n=========================================================================================================================================')
                print('====================================================  FAMILIES DETAILS  =================================================================\n')
                print(families)
                print('=========================================================================================================================================\n\n')
        spouses = []
        if person.get('spouse_name'):
            for entry in genealogy_data:
                if person['spouse_name'] in entry['spouse_name']:
                    spouse_names = entry['spouse_name'].split(';')
                    print('\n\n=========================================================================================================================================')
                    print('====================================================  SPOUSE NAME OR NAMES  =============================================================\n')
                    print(spouse_names)
                    print('=========================================================================================================================================\n\n')
                    for idx, spouse_name in enumerate(spouse_names):
                        spouse_details = {
                            'spouse_name': spouse_name.strip(),
                            'spouse_fathername': entry['spouse_fathername'].split(';')[idx].strip(),
                            'spouse_village': entry['spouse_village'].split(';')[idx].strip()
                        }
                        spouses.append(spouse_details)
        
        return render(request, 'person_detail.html', {
            'person': person,
            'families': families,
            'spouses': spouses,
            'previous_person_id': previous_person_id,
            'next_person_id': next_person_id
        })
    else:
        return HttpResponse('<center><h1>PERSON DOES NOT EXIST</h1></center><br><center><a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">HOME</a></center>')

    
def count_unique_ids(genealogy_data):
    ids = set()
    for entry in genealogy_data:
        ids.add(entry['ID'])
    return len(ids), sorted(ids)


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
        
        # Save the person details to CSV 
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


def import_data_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid CSV file'}, status=400)
        try:
            # Ensure proper decoding and handle potential BOM
            csv_data = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(csv_data)
            imported_data = []
            # Clear existing data to ensure fresh import
            # imported_data.clear()
            for row in reader:
                # Append each row from CSV to imported_data list
                imported_data.append({
                    'ID': row.get('ID', '').strip(),
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
                cache.set('imported_data', imported_data, timeout=None)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error reading or processing CSV file: {e}"}, status=500)
        # Store imported_data in session for future access
        # request.session['imported_data'] = imported_data
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
            root_person = imported_data[0]
            tree_data = build_tree(root_person, imported_data)
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
    try:
        imported_data = cache.get('imported_data')
        if not imported_data:
            return JsonResponse({"error": "No data available"}, status=400)
        
        root_person_name = "Anandsinhji"
        root_person = next((item for item in imported_data if item['Name'] == root_person_name), None)
        if not root_person:
            return JsonResponse({"error": "Root person not found"}, status=404)
        
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
        
        tree_data = build_tree_with_male(root_person)
        return JsonResponse(tree_data)
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
