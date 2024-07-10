from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import csv
import os
import json
import tempfile

# Path to your CSV file
csv_file_path = 'main/genealogy.csv'
json_file_path = os.path.join(tempfile.gettempdir(), 'genealogy_data.json')

# Save data to JSON
def save_data_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)

# Load data from JSON
def load_data_from_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    return []

# This view renders the tree.html template
def render_tree_view(request):
    imported_data = load_data_from_json(json_file_path)
    print("Imported Data:", imported_data)
    return render(request, 'tree.html', {'imported_data': imported_data})

def note(request):
    return render(request, 'note.html')

def search_person(request):
    query = request.GET.get('q')
    print("QUERY : ", query)
    genealogy_data = load_csv_data(csv_file_path)
    if query:
        try:
            person = next(item for item in genealogy_data if item["Name"].lower() == query.lower())
            return redirect('person_detail', person_id=person["ID"])
        except StopIteration:
            return HttpResponse('<center><h1>PERSON NOT FOUND</h1></center><br><center><a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">HOME</a></center>')
    return redirect('home')

def person_detail(request, person_id):
    genealogy_data = load_csv_data(csv_file_path)
    person = find_person(genealogy_data, person_id)
    if person:
        total_count_ids, total_ids = count_unique_ids(genealogy_data)
        total_ids = sorted(map(int, total_ids))
        person_id = int(person_id)
        current_index = total_ids.index(person_id)
        previous_person_id = total_ids[current_index - 1] if current_index > 0 else None
        next_person_id = total_ids[current_index + 1] if current_index < len(total_ids) - 1 else None

        families = []
        if 'children' in person:
            children = person['children'].split(';')
            child_ids = person['child_id'].split(';') if 'child_id' in person else []
            for idx, child_name in enumerate(children):
                child_id = child_ids[idx].strip() if idx < len(child_ids) else None
                family_details = {
                    'children_name': child_name.strip(),
                    'child_ids2': child_id,
                    'family_type': 'father' if person['Gender'] == 'M' else 'mother'
                }
                families.append(family_details)

        spouses = []
        if person.get('spouse_name'):
            for entry in genealogy_data:
                if person['spouse_name'] in entry['spouse_name']:
                    spouse_names = entry['spouse_name'].split(';')
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
    data = []
    with open(file_path, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def find_person(data, person_id):
    for person in data:
        if person['ID'] == str(person_id):
            return person

def create_person(request):
    if request.method == 'POST':
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

        genealogy_data = load_data_from_json(json_file_path)
        genealogy_data.append(new_person_data)
        save_data_to_json(genealogy_data, json_file_path)

        return redirect('tree_view')
    return render(request, 'person_form.html')

def import_data_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file or not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'message': 'Please upload a valid CSV file'}, status=400)
        try:
            csv_data = csv_file.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(csv_data)
            imported_data = []
            for row in reader:
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
                    'children': []
                })
            save_data_to_json(imported_data, json_file_path)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f"Error reading or processing CSV file: {e}"}, status=500)
        return redirect('tree_view')
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def build_tree(person, data):
    person_tree = {
        'name': person['Name'],
        'id': person['ID'],
        'child_id': person['child_id'],
        'gender': person['Gender'],
        'children': []
    }
    children = [child for child in data if child['Father'] == person['Name']]
    for child in children:
        person_tree['children'].append(build_tree(child, data))
    female_children_with_children = [child for child in data if child['Mother'] == person['Name']]
    for female_child in female_children_with_children:
        person_tree['children'].append(build_tree(female_child, data))
    return person_tree

def generate_tree_data(request):
    imported_data = load_data_from_json(json_file_path)
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
    imported_data = load_data_from_json(json_file_path)
    if not imported_data:
        return JsonResponse({'status': 'error', 'message': 'No data available'}, status=400)
    try:
        root_person = next((person for person in imported_data if person['Name'] == 'Anandsinhji'), None)
        if root_person:
            return JsonResponse({'name': root_person['Name']}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Root person not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def d3_collapsible_tree(request):
    try:
        imported_data = load_data_from_json(json_file_path)
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