# from re import M
# from django.forms import JSONField
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse,HttpResponse


# This view renders the tree.html template
def render_tree_view(request):
    return render(request, 'tree.html')

# This view displays details of a person
# This view displays details of a person
from django.shortcuts import render, Http404
import csv

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

# This view displays details of a child
# file_path = '/Users/neel2004/Desktop/family/family/main/genealogy.csv'

def child_detail(request, child_id):
    # Load CSV data
    genealogy_data = load_csv_data(file_path)
    # Find the child in CSV data
    child = find_person(genealogy_data, child_id)
    print('CHILD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>++++++++++++++++++++++++++++++',child)
    if child:
        families = []
        families.append(child)
        # Convert children IDs to a list of person dictionaries
        for family in families:
            children = []
            # Check if 'children' key exists in the family dictionary
            if 'children' in family:
                children_ids = family['children'].split(";")
                
                # Append each child to the children list
                for c in children_ids:
                    children.append(c.strip())
                
                # Initialize a list to store child details dictionaries
                child2 = []
                
                # Check if 'child_id' key exists in the family dictionary
                if 'child_id' in family:
                    child_ids = family['child_id'].split(';')
                    
                    # Iterate through each child_id and create child_details dictionary
                    for c_id in child_ids:
                        child_details = {
                            'child_id': c_id.strip(),
                        }
                        child2.append(child_details)
                
                # Iterate through children IDs and construct family_details for each children_name
                for children_name in children:
                    family_details = {
                        'children_name': children_name.strip(),
                        # 'child_ids': child2,  # Use the correct child_id list for each children_name
                    }
                    families.append(family_details)
        print('FAMILIES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',families)
        # Continue with spouse processing and rendering as per your existing logic
        spouses = []
        
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
            'id': request.POST.get('id'),
            'name': request.POST.get('name'),
            'gender': request.POST.get('gender'),
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
                new_person_data['id'],
                new_person_data['name'],
                new_person_data['gender'],
                new_person_data['father'],
                new_person_data['mother'],
                new_person_data['children'],
                new_person_data['spouse_name'],
                new_person_data['spouse_fathername'],
                new_person_data['spouse_village']
            ])
        
        # Redirect to create spouse view or any other relevant view
        return redirect('create_spouse')
    
    # Render a template for creating a new person (if needed)
    return render(request, 'person_form.html')

# 
# def create_spouse(request):
#     if request.method == 'POST':
#         spouse_form = SpouseInfoForm(request.POST)
#         if spouse_form.is_valid():
#             spouse_form.save()
#             return redirect('create_family')
#     else:
#         spouse_form = SpouseInfoForm()
#     return render(request, 'spouse_form.html',{'spouse_form':spouse_form})


# def create_spouse(request):
#     if request.method == 'POST':
#         spouse_form = SpouseInfoForm(request.POST)
#         if spouse_form.is_valid():
#             spouse = spouse_form.save(commit=False)  # Don't save to database yet
#             spouse.save()

#             # Add spouse details to CSV
#             update_csv_with_spouse(spouse)

#             return redirect('create_family')
#     else:
#         spouse_form = SpouseInfoForm()
#     return render(request, 'spouse_form.html', {'spouse_form': spouse_form})


# # 
# # def create_family(request):
# #     if request.method == 'POST':
# #         family_form = FamilyForm(request.POST)
# #         if family_form.is_valid():
# #             family = family_form.save()
# #             children_ids = request.POST.getlist('children')
# #             for child_id in children_ids:
# #                 child = Person.objects.get(id=child_id)
# #                 family.children.add(child)
# #             return redirect('tree_view')
# #     else:
# #         family_form = FamilyForm()
# #         # Filter the queryset for father and mother fields based on gender
# #         family_form.fields['father'].queryset = Person.objects.filter(gender='M')
# #         family_form.fields['mother'].queryset = Person.objects.filter(gender='F')
# #     return render(request, 'family_form.html', {'family_form': family_form})




# def create_family(request):
#     if request.method == 'POST':
#         family_form = FamilyForm(request.POST)
#         if family_form.is_valid():
#             family = family_form.save()

#             # Update CSV with family details and children
#             update_csv_with_family(family, request.POST.getlist('children'))

#             return redirect('tree_view')
#     else:
#         family_form = FamilyForm()
#         # Filter the queryset for father and mother fields based on gender
#         family_form.fields['father'].queryset = Person.objects.filter(gender='M')
#         family_form.fields['mother'].queryset = Person.objects.filter(gender='F')

#     return render(request, 'family_form.html', {'family_form': family_form})

# def update_csv_with_family(family, children_ids):
#     file_path = '/Users/neel2004/Desktop/family/genealogy.csv'

#     # Open CSV file in append mode to add new family details
#     with open(file_path, 'a', newline='') as file:
#         writer = csv.writer(file)

#         # Write family details to CSV
#         writer.writerow([
#             family.id,  # Assuming family has a unique identifier
#             family.father.id if family.father else '',  # Assuming ForeignKey to Person
#             family.mother.id if family.mother else '',  # Assuming ForeignKey to Person
#             ';'.join(children_ids) if children_ids else '',  # Assuming multiple children are separated by ';'
#         ])

# # Update an existing person
# # 
# # def update_person(request, person_id):
# #     person = get_object_or_404(Person, pk=person_id)
# #     if request.method == 'POST':
# #         person_form = PersonForm(request.POST, instance=person)
# #         if person_form.is_valid():
# #             person_form.save()
# #             # Redirect to the update_spouse view with the spouse's ID
# #             return redirect('person_detail', person_id=person.id)
# #     else:
# #         person_form = PersonForm(instance=person)
# #     return render(request, 'person_edit_form.html', {'person_form': person_form})


# def update_person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
    
#     if request.method == 'POST':
#         person_form = PersonForm(request.POST, instance=person)
#         if person_form.is_valid():
#             person_form.save()
            
#             # Update CSV file with new person data
#             update_csv_with_person(person)
            
#             # Redirect to the person detail view
#             return redirect('person_detail', person_id=person.id)
#     else:
#         person_form = PersonForm(instance=person)
    
#     return render(request, 'person_edit_form.html', {'person_form': person_form})


# def update_person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
    
#     if request.method == 'POST':
#         person_form = PersonForm(request.POST, instance=person)
#         if person_form.is_valid():
#             person_form.save()
            
#             # Update CSV file with new person data
#             update_csv_with_person(person)
            
#             # Redirect to the person detail view
#             return redirect('person_detail', person_id=person.id)
#     else:
#         person_form = PersonForm(instance=person)
    
#     return render(request, 'person_edit_form.html', {'person_form': person_form})

# def update_csv_with_person(person):
#     file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
#     # Open CSV file and update person's information
#     with open(file_path, 'r', newline='') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
        
#     with open(file_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         for row in rows:
#             if row[0] == str(person.id):  # Assuming ID is the first column
#                 row[1] = person.name      # Update name (assuming name is the second column)
#                 row[2] = person.gender    # Update gender (assuming gender is the third column)
#             writer.writerow(row)

# # 
# # def update_spouse(request, spouse_id):
# #     spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
# #     if request.method == 'POST':
# #         spouse_form = SpouseInfoForm(request.POST, instance=spouse)
# #         if spouse_form.is_valid():
# #             spouse_form.save()
# #             # Redirect to the update_family view with the spouse's ID
# #             return redirect('tree_view')
# #     else:
# #         spouse_form = SpouseInfoForm(instance=spouse)
# #     return render(request, 'spouse_edit_form.html', {'spouse_form': spouse_form})


# def update_spouse(request, spouse_id):
#     spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
    
#     if request.method == 'POST':
#         spouse_form = SpouseInfoForm(request.POST, instance=spouse)
#         if spouse_form.is_valid():
#             spouse_form.save()
            
#             # Update CSV file with new spouse data
#             update_csv_with_spouse(spouse)
            
#             # Redirect to the tree view or any appropriate view
#             return redirect('tree_view')  # Adjust the redirect as per your application's flow
#     else:
#         spouse_form = SpouseInfoForm(instance=spouse)
    
#     return render(request, 'spouse_edit_form.html', {'spouse_form': spouse_form})

# def update_csv_with_spouse(spouse):
#     file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
#     # Open CSV file and update spouse's information
#     with open(file_path, 'r', newline='') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
        
#     with open(file_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         for row in rows:
#             if row[0] == str(spouse.person.id):  # Assuming ID is the first column
#                 row[6] = spouse.spouse_name          # Update spouse_name (assuming it's the 7th column)
#                 row[7] = spouse.spouse_fathername    # Update spouse_fathername (assuming it's the 8th column)
#                 row[8] = spouse.spouse_village       # Update spouse_village (assuming it's the 9th column)
#             writer.writerow(row)

# # 
# # def update_family(request, family_id):
# #     family = get_object_or_404(Family, pk=family_id)
# #     if request.method == 'POST':
# #         family_form = FamilyForm(request.POST, instance=family)
# #         if family_form.is_valid():
# #             family_form.save()
# #             # Redirect to the family_detail view with the family's ID
# #             return redirect('tree_view')
# #     else:
# #         family_form = FamilyForm(instance=family)
# #     return render(request, 'family_edit_form.html', {'family_form': family_form})

# # login_required
# def update_family(request, family_id):
#     family = get_object_or_404(Family, pk=family_id)
    
#     if request.method == 'POST':
#         family_form = FamilyForm(request.POST, instance=family)
#         if family_form.is_valid():
#             family_form.save()
            
#             # Update CSV file with new family data
#             update_csv_with_family(family)
            
#             # Redirect to the tree view or any appropriate view
#             return redirect('tree_view')  # Adjust the redirect as per your application's flow
#     else:
#         family_form = FamilyForm(instance=family)
    
#     return render(request, 'family_edit_form.html', {'family_form': family_form})


# def update_csv_with_family(family):
#     file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
#     # Open CSV file and update family's information
#     with open(file_path, 'r', newline='') as file:
#         reader = csv.reader(file)
#         rows = list(reader)
        
#     with open(file_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         for row in rows:
#             if row and row[0] == str(family.father.id):  # Assuming father's ID is the first column
#                 children_names = ', '.join([child.name for child in family.children.all()])  # Update children (assuming it's the 4th column)
#                 row[5] = children_names.split(', ')  # Split children names by comma after updating
#             writer.writerow(row)

# # Delete a person

# def delete_person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
#     if request.method == 'POST':
#         person.delete()
#         return redirect('tree_view')
#     return render(request, 'person_confirm_delete.html', {'person': person})


# def delete_spouse(request, spouse_id):
#     spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
#     if request.method == 'POST':
#         spouse.delete()
#         return redirect('tree_view')
#     return render(request, 'spouse_confirm_delete.html', {'spouse': spouse})


# def delete_family(request, family_id):
#     family = get_object_or_404(Family, pk=family_id)
#     if request.method == 'POST':
#         family.delete()
#         return redirect('tree_view')
#     return render(request, 'family_confirm_delete.html', {'family': family})


# def forgotpass(request):
#     if request.method == 'POST':
#         email_id = request.POST.get('email_id')
#         if not UserRegistration.objects.filter(email_id=email_id).exists():
#             return render(request, 'getemail.html', {'error_message': "Email address not registered." "\n\n\n" "Please enter a valid email."})
#         otp = ''.join(random.choices('1234567890', k=4))
#         request.session['otp'] = otp
#         # Create email content
#         subject = "Your OTP Code"
#         body = f"Your OTP code is: {otp}"
#         message = f"Subject: {subject}\n\n{body}"
#         try:
#             # Use certifi's certificate bundle
#             context = ssl.create_default_context(cafile=certifi.where())
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                 server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
#                 server.sendmail("ramparagenealogy@gmail.com", email_id, message)
#         except Exception as e:
#             print("Error sending email:", e)
#             return HttpResponse("Failed to send OTP email. Please try again.")
#         request.session['email_id'] = email_id
#         return redirect('otp')    
#     return render(request, 'getemail.html')


# def otp(request):
#     if 'email_id' not in request.session:
#         return redirect('login')
#     if request.method == 'POST':
#         entered_otp = request.POST.get('otp')
#         if not entered_otp:
#             return render(request, 'otp.html')
#         stored_otp = request.session.get('otp')
#         if entered_otp == stored_otp:
#             return redirect('changepass')
#         else:
#             return render(request, 'otp.html',{'error_message':'Wrong OTP Entered.'})
#     return render(request, 'otp.html')


# def changepass(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('password')
#         if not new_password:
#             return render(request, 'changepass.html', {'error_message': "Password cannot be empty."})
#         if 'email_id' not in request.session:
#             return redirect('login')
#         try:
#             user = UserRegistration.objects.get(email_id=request.session['email_id'])
#             user.password = new_password
#             user.save()
#             # Send email notification
#             email = user.email_id
#             subject = "Password Changed Successfully..."
#             body = f"Hello,Your password has been successfully changed."
#             message = f"Subject: {subject}\n\n{body}"
#             try:
#                 # Use certifi's certificate bundle
#                 context = ssl.create_default_context(cafile=certifi.where())
#                 with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                     server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
#                     server.sendmail("ramparagenealogy@gmail.com", email, message)
#             except Exception as e:
#                 print("Error sending email:", e)
#             return redirect('login')
#         except UserRegistration.DoesNotExist:
#             return redirect('login')
#     return render(request, 'changepass.html')

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


import csv
from django.http import JsonResponse
from django.db import transaction

# Global variable to store imported data
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
            csv_data = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(csv_data)
            
            imported_data.clear()  # Clear existing data to ensure fresh import
            
            for row in reader:
                # try:
                    if not row['ID'].isdigit():
                        continue
                    
                    person_id = int(row['ID'])
                    child_id = row.get('child_id', '')
                    father_name = row.get('father', '')
                    mother_name = row.get('mother', '')
                    spouse_name = row.get('spouse_name', '')
                    spouse_fathername = row.get('spouse_fathername', '')
                    spouse_village = row.get('spouse_village', '')
                    
                    # Append each person's data to imported_data with an empty children list
                    imported_data.append({
                        'ID': person_id,
                        'child_id': child_id,
                        'Name': row['Name'],
                        'Gender': row['Gender'],
                        'Father': father_name,
                        'Mother': mother_name,
                        'Spouse Name': spouse_name,
                        'Spouse Father Name': spouse_fathername,
                        'Spouse Village': spouse_village,
                        'children': []  # Initialize an empty list for children
                    })
                
                # except Exception as e:
                #     return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
        return redirect('tree_view')
        # return JsonResponse({'status': 'success', 'message': 'Data imported successfully'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

from django.http import JsonResponse

def build_tree(person, data):
    # Initialize the tree structure for the current person
    person_tree = {
        'name': person['Name'],
        'id': person['ID'],
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




# def RegisterUserView(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('firstName')
#         last_name = request.POST.get('lastName')
#         email_id = request.POST.get('email_id')
#         password = request.POST.get('password')
        
#         # Create and save the user registration
#         user_registration = UserRegistration(
#             first_name=first_name,
#             last_name=last_name,
#             email_id=email_id,
#             password=password
#         )
#         try:
#             user_registration.save()
#         except IntegrityError:
#             error_message = "Email already registered. Please use a different email."
#             return render(request, 'signup.html', {'error_message': error_message})

#         # Send registration email
#         email = user_registration.email_id
#         subject = "Registered Successfully"
#         body = f"Hello {first_name} {last_name}, Thank you for registration.\n\nHave a nice day."
#         message = f"Subject: {subject}\n\n{body}"
#         try:
#             context = ssl.create_default_context(cafile=certifi.where())
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                 server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
#                 server.sendmail("ramparagenealogy@gmail.com", email, message)
#         except Exception as e:
#             print("Error sending email:", e)
        
#         return redirect('login')
#     return render(request, 'signup.html')

# def LoginUserView(request):
#     if request.method == 'POST':
#         email = request.POST.get('email_id')
#         passwordobj = request.POST.get('password')      
#         user_registration = UserRegistration.objects.filter(email_id=email).last()
#         print('-----------------------------------USER>>>>>>>>>>>>>>', user_registration)
#         if user_registration is not None:
#             print('--------------------------CHECK IF >>>>>>>>>>>>>>>>>>>>>', user_registration)
#             if user_registration.password == passwordobj:
#                 print('---------------------------PASSWORD>>>>>>>>>>>>>>>>>', passwordobj)
#                 # Store user information in session
#                 request.session['user_id'] = user_registration.id
#                 request.session['email'] = email
#                 request.session['first_name'] = user_registration.first_name
#                 request.session['last_name'] = user_registration.last_name
#                 email = user_registration.email_id
#                 subject = "Login Successfully"
#                 body = f"Hello {user_registration.first_name} {user_registration.last_name},\nWelcome back! You have logged in successfully..."
#                 message = f"Subject: {subject}\n\n{body}"
#                 try:
#                     context = ssl.create_default_context(cafile=certifi.where())
#                     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                         server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
#                         server.sendmail("ramparagenealogy@gmail.com", email, message)
#                 except Exception as e:
#                     print("Error sending email:", e)
#                 return redirect('tree_view')
#             else:
#                 return render(request, 'login.html', {'error_message': 'Invalid credentials'})
#         else:
#             return render(request, 'login.html', {'error_message': 'User not found or invalid password'})
#     return render(request, 'login.html')


# def logout_view(request):
#     email = request.session.get('email')
#     if email:
#         del request.session['user_id']
#         del request.session['email']
#         del request.session['first_name']
#         del request.session['last_name']
#     else:    
#         return redirect('login')    
#     return redirect('login')


# def contactus_view(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         message = request.POST['message']
#         ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
#         return redirect('contactus')
#     return render(request, 'contactus.html')


# Create a new person
# 
# def create_person(request):
#     if request.method == 'POST':
#         person_form = PersonForm(request.POST)
#         if person_form.is_valid() :
#             person_form.save()
#         return redirect('create_spouse')
#     else:
#         person_form = PersonForm()
#     return render(request, 'person_form.html', {'person_form': person_form})

# file_path = '/Users/neel2004/Desktop/family/family/main/genealogy.csv'