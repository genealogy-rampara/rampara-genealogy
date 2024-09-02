import csv, requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from .forms import PersonForm

# Path to your CSV file
def render_tree_view(request):
    return render(request, 'tree.html')

def mobile_template(request):
    return render(request, 'mobile_template.html')

def tree_with_female(request):
    return render(request, 'v2.html')

def v2_mobile_template(request):
    return render(request, 'v2_mobile_template.html')

def login(request):
    email = 'ramparagenealogy@gmail.com'
    password = 'Rampara@2024'
    return render(request, 'login.html', {'email': email, 'password': password})
csv_file_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTBaOy39XofhZwSWj6RDKkt4QUE69raL98PEVnZD70wtaZ4Es4Gp7BnQyBsWg21hAxY2zNL58tPMPrW/pub?output=csv'    

# Function to fetch CSV data from Google Drive
def fetch_csv_data_from_drive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:     # The HTTP 200 OK success status response code indicates that the request has succeeded.
            csv_data = response.content.decode('utf-8-sig').splitlines()  # Decode the content and split into lines
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
        reader = csv.DictReader(csv_data)  # Create a CSV reader object
        for row in reader:  # Iterate over each row in the CSV data
            imported_data.append({
                'ID': row.get('ID', '').strip(),
                'child_id': row.get('child_id', '').strip(),
                'Name': row.get('Name', ''),
                'DOB': row.get('DOB', '').strip(),
                'Gender': row.get('Gender', '').strip(),
                'father': row.get('father', ''),
                'mother': row.get('mother', ''),
                'spouse_name': row.get('spouse_name', ''),
                'spouse_fathername': row.get('spouse_fathername', ''),
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
        csv_data = fetch_csv_data_from_drive(csv_file_url)  # Fetch CSV data from Google Drive
        if csv_data:
            imported_data = import_data_from_csv(csv_data)  # Import data from the fetched CSV data
            if imported_data:
                return redirect('tree_view')
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to import data from CSV'}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch CSV data from Google Drive'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# View to search for a person in the genealogy data
def search_person(request):
    query = request.GET.get('q')
    print('\n\n=========================================================================================================================================')
    print('=================================================================  QUERY  ===============================================================\n')
    print(query)
    print('=========================================================================================================================================\n\n')

    genealogy_data = import_data_from_csv(fetch_csv_data_from_drive(csv_file_url))
    if query:
        # Find all persons where the Name or spouse_village contains the query string
        matching_persons = [item for item in genealogy_data if query.lower() in item.get("Name","") or query.lower() in item.get("spouse_village", "").lower() or query.lower() in item.get("spouse_name","") or query.lower() in item.get("spouse_fathername","")]
        if matching_persons:
            if len(matching_persons) == 1:
                # If exactly one match is found, redirect to the person's detail page
                return redirect('person_detail', person_id=matching_persons[0]["ID"])
            else:
                # If multiple matches are found, display a list of possible matches
                return render(request, 'multiple_matches.html', {'persons': matching_persons})
        else:
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
    # Find all children where the father is the current person
    children = [child for child in data if child['father'] == person['Name']]
    for child in children:
        person_tree['children'].append(build_tree(child, data))  # Recursively build the tree for each child
    # Find all children where the mother is the current person
    female_children_with_children = [child for child in data if child['mother'] == person['Name']]
    for female_child in female_children_with_children:
        person_tree['children'].append(build_tree(female_child, data))  # Recursively build the tree for each child
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
                    # for idx, spouse_name in enumerate(spouse_names):
                    #     spouse_details = {
                    #         'spouse_name': spouse_name.strip(),
                    #         'spouse_fathername': entry['spouse_fathername'].split(';')[idx].strip(),
                    #         'spouse_village': entry['spouse_village'].split(';')[idx].strip()
                    #     }
                    #     spouses.append(spouse_details)
                    for idx, spouse_name in enumerate(spouse_names):
                        spouse_details = {
                        'spouse_name': spouse_name,
                        'spouse_fathername': entry['spouse_fathername'].split(';')[idx],
                        'spouse_village': entry['spouse_village'].split(';')[idx].strip(),
                        'spouse_village_map': f"https://www.google.com/maps/search/?api=1&query={entry['spouse_village'].split(';')[idx].strip()}"
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
        
        # root_person_name = "Raj Jaswantsinhji - 2"
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

def save_person_data(request):
    if request.method == 'POST':
        num_children = int(request.POST.get('num_children', 0))
        num_spouse = int(request.POST.get('num_spouse', 0))

        form = PersonForm(request.POST, num_children=num_children, num_spouse=num_spouse)
        if form.is_valid():
            person_data = [
                form.cleaned_data.get('your_name', ''),
                form.cleaned_data.get('your_email', ''),
                form.cleaned_data.get('person_name', ''),
                form.cleaned_data.get('dob', ''),
                form.cleaned_data.get('gender', ''),
                form.cleaned_data.get('father_name', ''),
                form.cleaned_data.get('mother_name', ''),
                form.cleaned_data.get('marital_status', ''),
                num_spouse,
                num_children
            ]

            # Collect spouse details
            spouse_data = []
            for i in range(1, num_spouse + 1):
                spouse_name = form.cleaned_data.get(f'spouse_name_{i}', '')
                spouse_father_name = form.cleaned_data.get(f'spouse_father_name_{i}', '')
                spouse_village = form.cleaned_data.get(f'spouse_village_{i}', '')
                spouse_data.extend([spouse_name, spouse_father_name, spouse_village])

            # Collect children details
            children_data = []
            for i in range(1, num_children + 1):
                child_name = form.cleaned_data.get(f'child_name_{i}', '')
                child_gender = form.cleaned_data.get(f'child_gender_{i}', '')
                child_marital_status = form.cleaned_data.get(f'child_marital_status_{i}', '')
                children_data.extend([child_name, child_gender, child_marital_status])

            # Define the path for the temporary CSV file
            temp_csv_path = '/tmp/rampara-genealogy.csv'

            # Build the header based on current data
            header = [
                'Your Name', 'Your Email', 'Person Name', 'DOB', 'Gender', 
                'Father Name', 'Mother Name', 'Marital Status', 'Number of Spouse',
                'Number of Children'
            ]
            for i in range(1, num_spouse + 1):
                header.extend([f'Spouse Name {i}', f'Spouse Father Name {i}', f'Spouse Village {i}'])
            for i in range(1, num_children + 1):
                header.extend([f'Child Name {i}', f'Child Gender {i}', f'Child Marital Status {i}'])

            try:
                with open(temp_csv_path, 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Write the header if the file is new
                    if csvfile.tell() == 0:
                        writer.writerow(header)
                    
                    # Write the data
                    final_data = person_data + spouse_data + [''] * (num_spouse * 3 - len(spouse_data))
                    final_data += children_data + [''] * (num_children * 3 - len(children_data))
                    writer.writerow(final_data)

                # Send the CSV file via email to yourself (for record-keeping)
                email = EmailMessage(
                    subject='Genealogy CSV File',
                    body='Please find the attached file.',
                    to=['ramparagenealogy@gmail.com']
                )
                email.attach_file(temp_csv_path)
                email.send()

                # Send a confirmation email to the user
                user_email = form.cleaned_data.get('your_email')
                confirmation_email = EmailMessage(
                    subject='Submission Received - Rampara Genealogy',
                    body='Your data has been successfully submitted. It will be added to our records within 3-5 working days.',
                    to=[user_email]
                )
                confirmation_email.send()

                print(f"Data successfully written to CSV at: {temp_csv_path} and emailed.")

            except IOError as e:
                print(f"Error writing to file: {e}")

            return redirect('save_person_data')
        
        else:
            return render(request, 'save_person_data.html', {'form': form, 'error': 'Please correct the errors below.'})
    else:
        num_children = int(request.GET.get('num_children', 0))
        num_spouse = int(request.GET.get('num_spouse', 0))
        form = PersonForm(num_children=num_children, num_spouse=num_spouse)
    
    return render(request, 'save_person_data.html', {'form': form})
