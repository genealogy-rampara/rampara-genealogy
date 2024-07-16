from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import csv
import requests

# Path to your CSV file
def render_tree_view(request):
    return render(request, 'tree.html')

def tree_with_female(request):
    return render(request, 'v2.html')

def login(request):
    email = 'ramparagenealogy@gmail.com'
    password = 'Rampara@2024'
    return render(request, 'login.html',{'email':email, 'password' : password})

csv_file_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTBaOy39XofhZwSWj6RDKkt4QUE69raL98PEVnZD70wtaZ4Es4Gp7BnQyBsWg21hAxY2zNL58tPMPrW/pub?output=csv'    
def fetch_csv_data_from_drive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            csv_data = response.content.decode('utf-8-sig').splitlines()
            return csv_data
        else:
            print(f"Failed to fetch data from Google Drive. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching data from Google Drive: {e}")
        return None

# Function to process and import CSV data
def import_data_from_csv(csv_data):
    imported_data = []
    try:
        reader = csv.DictReader(csv_data)
        for row in reader:
            imported_data.append({
                'ID': row.get('ID', '').strip(),
                'child_id': row.get('child_id', '').strip(),
                'Name': row.get('Name', ''),
                'DOB': row.get('DOB', '').strip(),
                'Gender': row.get('Gender', '').strip(),
                'father': row.get('father', ''),
                'mother': row.get('mother', ''),
                'spouse_name': row.get('spouse_name', '').strip(),
                'spouse_fathername': row.get('spouse_fathername', '').strip(),
                'spouse_village': row.get('spouse_village', '').strip(),
                'children': row.get('children', '') 
            })
        return imported_data
    except Exception as e:
        error_message = f"Error reading or processing CSV data: {e}"
        print(error_message)
        return None

# View to import data from CSV file
def import_data_from_drive(request):
    if request.method == 'POST':
        csv_data = fetch_csv_data_from_drive(csv_file_url)
        if csv_data:
            imported_data = import_data_from_csv(csv_data)
            if imported_data:
                return redirect('tree_view')
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to import data from CSV'}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch CSV data from Google Drive'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def search_person(request):
    query = request.GET.get('q')
    print('\n\n=========================================================================================================================================')
    print('=================================================================  QUERY  ===============================================================\n')
    print(query)
    print('=========================================================================================================================================\n\n')
    genealogy_data = import_data_from_csv(fetch_csv_data_from_drive(csv_file_url))
    if query:
        # query = query.strip()
        try:
            person = next(item for item in genealogy_data if item["Name"].lower() == query.lower())
            return redirect('person_detail', person_id=person["ID"])
        except StopIteration:
            return HttpResponse('<center><h1>PERSON NOT FOUND</h1></center><br><center><a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">HOME</a></center>')
    return redirect('tree_view')

# Function to build the family tree structure
def build_tree(person, data):
    person_tree = {
        'name': person['Name'],
        'id': person['ID'],
        'child_id': person['child_id'],
        'DOB': person['DOB'],
        'gender': person['Gender'],
        'children': []
    }
    children = [child for child in data if child['father'] == person['Name']]
    for child in children:
        person_tree['children'].append(build_tree(child, data))
    female_children_with_children = [child for child in data if child['mother'] == person['Name']]
    for female_child in female_children_with_children:
        person_tree['children'].append(build_tree(female_child, data))
    return person_tree

# View to render the note.html template
def note(request):
    return render(request, 'note.html')

# View to display detailed information about a person
def person_detail(request, person_id):
    # Load CSV data
    genealogy_data = import_data_from_csv(fetch_csv_data_from_drive(csv_file_url))
    # Find the person in CSV data
    person = find_person(genealogy_data, person_id)
    if person:
        print('\n\n=========================================================================================================================================')
        print('==========================================================  PERSON  =====================================================================\n')
        print(person)
        print('=========================================================================================================================================\n\n')
        # Get all person IDs
        DOB = person['DOB']
        print(DOB)
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
            print('\n\n=========================================================================================================================================')
            print('====================================================  CHILDREN KEY EXISTS  ==============================================================\n')
            print(person['children'])
            print('=========================================================================================================================================\n\n')
            children = person['children'].split(';') if person['children'] else []
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
        else:
            print("No children key found in the person dictionary.")

        # Ensure children are correctly linked to their parent
        for family in families:
            child_id = family['child_ids2']
            if child_id:
                child_person = find_person(genealogy_data, child_id)
                print('\n\n=========================================================================================================================================')
                print('=================================================================  FINDING CHILD PERSON WITH ID  ===============================================================\n')
                print(f'Finding child person with ID - {child_id} : {child_person}')
                print('=========================================================================================================================================\n\n')
                if child_person:
                    family['children_name'] = child_person['Name']
                else:
                    family['children_name'] = "Unknown"

        spouses = []
        if person.get('spouse_name'):
            for entry in genealogy_data:
                if person['spouse_name'] in entry['spouse_name']:
                    print('GENDER : ',person['Gender'])
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
                    print('\n\n=========================================================================================================================================')
                    print('====================================================  SPOUSES DETAILS  =============================================================\n')
                    print(spouses)
                    print('=========================================================================================================================================\n\n')
        return render(request, 'person_detail.html', {
            'person': person,
            'DOB':DOB,
            'families': families,
            'spouses': spouses,
            'previous_person_id': previous_person_id,
            'next_person_id': next_person_id
        })
    else:
        return HttpResponse('<center><h1>PERSON DOES NOT EXIST</h1></center><br><center><a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">HOME</a></center>')

def find_person(data, person_id):
    """
    Find a person with the specified ID in the loaded genealogy data.
    """
    for person in data:
        if person['ID'] == str(person_id):
            return person

        
# Function to count unique IDs in the genealogy data
def count_unique_ids(genealogy_data):
    ids = set()
    for entry in genealogy_data:
        ids.add(entry['ID'])
    return len(ids), sorted(ids)

# View to generate family tree data
def generate_tree_data(request):
    genealogy_data = import_data_from_csv(fetch_csv_data_from_drive(csv_file_url))
    print('\n\n=========================================================================================================================================')
    print('=============================================================  GENEALOGY DATA  ==========================================================\n')
    print(genealogy_data)
    print('=========================================================================================================================================\n\n')
    if not genealogy_data:
        return JsonResponse({'status': 'error', 'message': 'Data not imported yet'}, status=404)
    try:
        if request.method == 'GET':
            root_person = genealogy_data[0]
            tree_data = build_tree(root_person, genealogy_data)
            return JsonResponse(tree_data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# View to get tree data for D3 collapsible tree visualization
def d3_collapsible_tree(request):
    try:
        genealogy_data = import_data_from_csv(fetch_csv_data_from_drive(csv_file_url))
        print('\n\n=========================================================================================================================================')
        print('=============================================================  GENEALOGY DATA  ==========================================================\n')
        print(genealogy_data)
        print('=========================================================================================================================================\n\n')
        if not genealogy_data:
            return JsonResponse({"error": "No data available"}, status=400)
        
        # root_person_name = "Vakhatsinhji"
        root_person = genealogy_data[0]
        # root_person = next((item for item in genealogy_data if item['Name'] == root_person_name), None)
        if root_person is None:
            return JsonResponse({"error": "Root person not found"}, status=404)
        
        def build_tree_with_male(person):
            return {
                'name': person['Name'],
                'id': person['ID'],
                'child_id': person['child_id'],
                'gender': person['Gender'],
                'children': [
                    build_tree_with_male(child)
                    for child in genealogy_data
                    if child['father'] == person['Name'] and child['Gender'] == 'M'
                ]
            }

        tree_data = build_tree_with_male(root_person)
        return JsonResponse(tree_data)  
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)