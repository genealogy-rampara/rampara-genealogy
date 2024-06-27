from re import M
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse,HttpResponse
from .models import Person,SpouseInfo, Family, UserRegistration, ContactMessage
from .forms import FamilyForm, PersonForm, SpouseInfoForm
from django.contrib.auth.decorators import login_required
import random, smtplib, ssl, certifi, logging
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth import logout
# from django.http import HttpResponseRedirect
# import email


# This view renders the tree.html template
def render_tree_view(request):
    # user_id = request.session.get('user_id')
    # user_registration = None
    # if user_id:
        # user_registration = UserRegistration.objects.get(id=user_id)
    return render(request, 'tree.html')


# Generate tree data starting from a person
# def generate_tree_data(person):
#     data = {
#         "name": person.name,
#         "id": person.id,
#         "gender": person.gender,
#         "children": []
#     }
#     # Find families where the person is the father
#     families_as_father = Family.objects.filter(father=person)
#     for family in families_as_father:
#         children = family.children.filter(gender='M')
#         for child in children:
#             data["children_names"].append(generate_tree_data(child))
#     # Find families where the person is the mother
#     families_as_mother = Family.objects.filter(mother=person)
#     for family in families_as_father & families_as_mother:
#         # Get children who are sons (assuming male children)
#         sons = family.children.filter(gender='M')
#         for son in sons:
#             # Recursively generate data for each child
#             data["children"].append(generate_tree_data(son))
#     return data

def generate_tree_data(person):
    data = {
        "name": person.name,
        "id": person.id,
        "gender": person.gender,
        "children": []
    }

    # Find families where the person is the father
    families_as_father = Family.objects.filter(father=person)
    for family in families_as_father:
        children = family.children.filter(gender='M')
        print('---------------------CHILDREN----------------->>>>>>>>>>>',children)
        for child in children:
            data["children"].append(generate_tree_data(child))

    # Find families where the person is the mother
    families_as_mother = Family.objects.filter(mother=person)
    for family in families_as_mother:
        children = family.children.filter(gender='M')
        for child in children:
            data["children"].append(generate_tree_data(child))

    return data

# This view generates data for D3.js collapsible tree
def get_tree_data(request):
    try:
        root_person = Person.objects.get(name="Anandsinhji")
    except Person.DoesNotExist:
        return JsonResponse({"error": "Root person not found"}, status=404)
    tree_data = generate_tree_data(root_person)
    return JsonResponse(tree_data)

def d3_collapsible_tree(request):
    email = request.session.get('email')
    if email:
        try:
            root_person = Person.objects.get(name="Anandsinhji")
        except Person.DoesNotExist:
            return JsonResponse({"error": "Root person not found"}, status=404)
        tree_data = generate_tree_data(root_person)
        return JsonResponse(tree_data)
    else:
        return redirect('login')

# This view displays details of a person

def person_detail(request, person_id):
    email = request.session.get('email')
    if email:
        person = get_object_or_404(Person, pk=person_id)
        families = Family.objects.filter(father=person).prefetch_related('children')
        spouses = SpouseInfo.objects.filter(person=person)
        children_count = sum(family.children.count() for family in families)
        family_as_child = Family.objects.filter(children=person).first()
        father = family_as_child.father if family_as_child else None
        mother = family_as_child.mother if family_as_child else None

        return render(request, 'person_detail.html', {
            'person': person,
            'families': families,
            'children_count': children_count,
            'spouses': spouses,
            'father': father,
            'mother': mother
        })
    else:
        return redirect('login')

# This view displays details of a child
# @login_required(login_url='/')
def child_detail(request, child_id):
    email = request.session.get('email')
    if email :
        child = get_object_or_404(Person, pk=child_id)
        family = Family.objects.filter(children=child).first()
        father = family.father if family else None
        mother = family.mother if family else None
        spouses = SpouseInfo.objects.filter(person=child_id)
        families = Family.objects.filter(father=child).prefetch_related('children')
        families_as_mother = Family.objects.filter(mother=child).prefetch_related('children')
        # families = families_as_father | families_as_mother
        children_count_father = sum(family.children.count() for family in families)
        children_count_mother = sum(family.children.count() for family in families_as_mother)
        return render(request, 'child_detail.html', {
            'child': child,
            'father': father,
            'mother': mother,
            'spouses': spouses,
            'families': families,
            'families_as_mother': families_as_mother,
            'children_count_father': children_count_father,
            'children_count_mother': children_count_mother,
        })
    else:
        return redirect('login')

def RegisterUserView(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        
        # Create and save the user registration
        user_registration = UserRegistration(
            first_name=first_name,
            last_name=last_name,
            email_id=email_id,
            password=password
        )
        try:
            user_registration.save()
        except IntegrityError:
            error_message = "Email already registered. Please use a different email."
            return render(request, 'signup.html', {'error_message': error_message})

        # Send registration email
        email = user_registration.email_id
        subject = "Registered Successfully"
        body = f"Hello {first_name} {last_name}, Thank you for registration.\n\nHave a nice day."
        message = f"Subject: {subject}\n\n{body}"
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
                server.sendmail("ramparagenealogy@gmail.com", email, message)
        except Exception as e:
            print("Error sending email:", e)
        
        return redirect('login')
    return render(request, 'signup.html')

def LoginUserView(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        passwordobj = request.POST.get('password')      
        user_registration = UserRegistration.objects.filter(email_id=email).last()
        print('-----------------------------------USER>>>>>>>>>>>>>>', user_registration)
        if user_registration is not None:
            print('--------------------------CHECK IF >>>>>>>>>>>>>>>>>>>>>', user_registration)
            if user_registration.password == passwordobj:
                print('---------------------------PASSWORD>>>>>>>>>>>>>>>>>', passwordobj)
                # Store user information in session
                request.session['user_id'] = user_registration.id
                request.session['email'] = email
                request.session['first_name'] = user_registration.first_name
                request.session['last_name'] = user_registration.last_name
                email = user_registration.email_id
                subject = "Login Successfully"
                body = f"Hello {user_registration.first_name} {user_registration.last_name},\nWelcome back! You have logged in successfully..."
                message = f"Subject: {subject}\n\n{body}"
                try:
                    context = ssl.create_default_context(cafile=certifi.where())
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                        server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
                        server.sendmail("ramparagenealogy@gmail.com", email, message)
                except Exception as e:
                    print("Error sending email:", e)
                return redirect('tree_view')
            else:
                return render(request, 'login.html', {'error_message': 'Invalid credentials'})
        else:
            return render(request, 'login.html', {'error_message': 'User not found or invalid password'})
    return render(request, 'login.html')


def logout_view(request):
    email = request.session.get('email')
    if email:
        del request.session['user_id']
        del request.session['email']
        del request.session['first_name']
        del request.session['last_name']
    else:    
        return redirect('login')    
    return redirect('login')


def contactus_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        ContactMessage.objects.create(name=name, email=email, phone=phone, message=message)
        return redirect('contactus')
    return render(request, 'contactus.html')


# Create a new person
# @login_required
# def create_person(request):
#     if request.method == 'POST':
#         person_form = PersonForm(request.POST)
#         if person_form.is_valid() :
#             person_form.save()
#         return redirect('create_spouse')
#     else:
#         person_form = PersonForm()
#     return render(request, 'person_form.html', {'person_form': person_form})

file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
@login_required
def create_person(request):
    if request.method == 'POST':
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            # Save the person object
            new_person = person_form.save()
            
            # Add new person details to CSV file
            with open(file_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    new_person.id,
                    new_person.name,
                    new_person.gender,
                    '',  # father (initially empty)
                    '',  # mother (initially empty)
                    '',  # children (initially empty)
                    '',  # spouse_name (initially empty)
                    '',  # spouse_fathername (initially empty)
                    ''   # spouse_village (initially empty)
                ])
            
            return redirect('create_spouse')
    else:
        person_form = PersonForm()
    return render(request, 'person_form.html', {'person_form': person_form})

# @login_required
# def create_spouse(request):
#     if request.method == 'POST':
#         spouse_form = SpouseInfoForm(request.POST)
#         if spouse_form.is_valid():
#             spouse_form.save()
#             return redirect('create_family')
#     else:
#         spouse_form = SpouseInfoForm()
#     return render(request, 'spouse_form.html',{'spouse_form':spouse_form})
@login_required
def create_spouse(request):
    if request.method == 'POST':
        spouse_form = SpouseInfoForm(request.POST)
        if spouse_form.is_valid():
            spouse = spouse_form.save(commit=False)  # Don't save to database yet
            spouse.save()

            # Add spouse details to CSV
            update_csv_with_spouse(spouse)

            return redirect('create_family')
    else:
        spouse_form = SpouseInfoForm()
    return render(request, 'spouse_form.html', {'spouse_form': spouse_form})


# @login_required
# def create_family(request):
#     if request.method == 'POST':
#         family_form = FamilyForm(request.POST)
#         if family_form.is_valid():
#             family = family_form.save()
#             children_ids = request.POST.getlist('children')
#             for child_id in children_ids:
#                 child = Person.objects.get(id=child_id)
#                 family.children.add(child)
#             return redirect('tree_view')
#     else:
#         family_form = FamilyForm()
#         # Filter the queryset for father and mother fields based on gender
#         family_form.fields['father'].queryset = Person.objects.filter(gender='M')
#         family_form.fields['mother'].queryset = Person.objects.filter(gender='F')
#     return render(request, 'family_form.html', {'family_form': family_form})


@login_required
def create_family(request):
    if request.method == 'POST':
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            family = family_form.save()

            # Update CSV with family details and children
            update_csv_with_family(family, request.POST.getlist('children'))

            return redirect('tree_view')
    else:
        family_form = FamilyForm()
        # Filter the queryset for father and mother fields based on gender
        family_form.fields['father'].queryset = Person.objects.filter(gender='M')
        family_form.fields['mother'].queryset = Person.objects.filter(gender='F')

    return render(request, 'family_form.html', {'family_form': family_form})

def update_csv_with_family(family, children_ids):
    file_path = '/Users/neel2004/Desktop/family/genealogy.csv'

    # Open CSV file in append mode to add new family details
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)

        # Write family details to CSV
        writer.writerow([
            family.id,  # Assuming family has a unique identifier
            family.father.id if family.father else '',  # Assuming ForeignKey to Person
            family.mother.id if family.mother else '',  # Assuming ForeignKey to Person
            ';'.join(children_ids) if children_ids else '',  # Assuming multiple children are separated by ';'
        ])

# Update an existing person
# @login_required
# def update_person(request, person_id):
#     person = get_object_or_404(Person, pk=person_id)
#     if request.method == 'POST':
#         person_form = PersonForm(request.POST, instance=person)
#         if person_form.is_valid():
#             person_form.save()
#             # Redirect to the update_spouse view with the spouse's ID
#             return redirect('person_detail', person_id=person.id)
#     else:
#         person_form = PersonForm(instance=person)
#     return render(request, 'person_edit_form.html', {'person_form': person_form})

@login_required
def update_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    
    if request.method == 'POST':
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            
            # Update CSV file with new person data
            update_csv_with_person(person)
            
            # Redirect to the person detail view
            return redirect('person_detail', person_id=person.id)
    else:
        person_form = PersonForm(instance=person)
    
    return render(request, 'person_edit_form.html', {'person_form': person_form})

@login_required
def update_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    
    if request.method == 'POST':
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            
            # Update CSV file with new person data
            update_csv_with_person(person)
            
            # Redirect to the person detail view
            return redirect('person_detail', person_id=person.id)
    else:
        person_form = PersonForm(instance=person)
    
    return render(request, 'person_edit_form.html', {'person_form': person_form})

def update_csv_with_person(person):
    file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
    # Open CSV file and update person's information
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == str(person.id):  # Assuming ID is the first column
                row[1] = person.name      # Update name (assuming name is the second column)
                row[2] = person.gender    # Update gender (assuming gender is the third column)
            writer.writerow(row)

# @login_required
# def update_spouse(request, spouse_id):
#     spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
#     if request.method == 'POST':
#         spouse_form = SpouseInfoForm(request.POST, instance=spouse)
#         if spouse_form.is_valid():
#             spouse_form.save()
#             # Redirect to the update_family view with the spouse's ID
#             return redirect('tree_view')
#     else:
#         spouse_form = SpouseInfoForm(instance=spouse)
#     return render(request, 'spouse_edit_form.html', {'spouse_form': spouse_form})

@login_required
def update_spouse(request, spouse_id):
    spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
    
    if request.method == 'POST':
        spouse_form = SpouseInfoForm(request.POST, instance=spouse)
        if spouse_form.is_valid():
            spouse_form.save()
            
            # Update CSV file with new spouse data
            update_csv_with_spouse(spouse)
            
            # Redirect to the tree view or any appropriate view
            return redirect('tree_view')  # Adjust the redirect as per your application's flow
    else:
        spouse_form = SpouseInfoForm(instance=spouse)
    
    return render(request, 'spouse_edit_form.html', {'spouse_form': spouse_form})

def update_csv_with_spouse(spouse):
    file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
    # Open CSV file and update spouse's information
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row[0] == str(spouse.person.id):  # Assuming ID is the first column
                row[6] = spouse.spouse_name          # Update spouse_name (assuming it's the 7th column)
                row[7] = spouse.spouse_fathername    # Update spouse_fathername (assuming it's the 8th column)
                row[8] = spouse.spouse_village       # Update spouse_village (assuming it's the 9th column)
            writer.writerow(row)

# @login_required
# def update_family(request, family_id):
#     family = get_object_or_404(Family, pk=family_id)
#     if request.method == 'POST':
#         family_form = FamilyForm(request.POST, instance=family)
#         if family_form.is_valid():
#             family_form.save()
#             # Redirect to the family_detail view with the family's ID
#             return redirect('tree_view')
#     else:
#         family_form = FamilyForm(instance=family)
#     return render(request, 'family_edit_form.html', {'family_form': family_form})

login_required
def update_family(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    
    if request.method == 'POST':
        family_form = FamilyForm(request.POST, instance=family)
        if family_form.is_valid():
            family_form.save()
            
            # Update CSV file with new family data
            update_csv_with_family(family)
            
            # Redirect to the tree view or any appropriate view
            return redirect('tree_view')  # Adjust the redirect as per your application's flow
    else:
        family_form = FamilyForm(instance=family)
    
    return render(request, 'family_edit_form.html', {'family_form': family_form})


def update_csv_with_family(family):
    file_path = '/Users/neel2004/Desktop/family/genealogy.csv'
    
    # Open CSV file and update family's information
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
        
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            if row and row[0] == str(family.father.id):  # Assuming father's ID is the first column
                children_names = ', '.join([child.name for child in family.children.all()])  # Update children (assuming it's the 4th column)
                row[5] = children_names.split(', ')  # Split children names by comma after updating
            writer.writerow(row)

# Delete a person
@login_required
def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        person.delete()
        return redirect('tree_view')
    return render(request, 'person_confirm_delete.html', {'person': person})

@login_required
def delete_spouse(request, spouse_id):
    spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
    if request.method == 'POST':
        spouse.delete()
        return redirect('tree_view')
    return render(request, 'spouse_confirm_delete.html', {'spouse': spouse})

@login_required
def delete_family(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    if request.method == 'POST':
        family.delete()
        return redirect('tree_view')
    return render(request, 'family_confirm_delete.html', {'family': family})


def forgotpass(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        if not UserRegistration.objects.filter(email_id=email_id).exists():
            return render(request, 'getemail.html', {'error_message': "Email address not registered." "\n\n\n" "Please enter a valid email."})
        otp = ''.join(random.choices('1234567890', k=4))
        request.session['otp'] = otp
        # Create email content
        subject = "Your OTP Code"
        body = f"Your OTP code is: {otp}"
        message = f"Subject: {subject}\n\n{body}"
        try:
            # Use certifi's certificate bundle
            context = ssl.create_default_context(cafile=certifi.where())
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
                server.sendmail("ramparagenealogy@gmail.com", email_id, message)
        except Exception as e:
            print("Error sending email:", e)
            return HttpResponse("Failed to send OTP email. Please try again.")
        request.session['email_id'] = email_id
        return redirect('otp')    
    return render(request, 'getemail.html')


def otp(request):
    if 'email_id' not in request.session:
        return redirect('login')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if not entered_otp:
            return render(request, 'otp.html')
        stored_otp = request.session.get('otp')
        if entered_otp == stored_otp:
            return redirect('changepass')
        else:
            return render(request, 'otp.html',{'error_message':'Wrong OTP Entered.'})
    return render(request, 'otp.html')


def changepass(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        if not new_password:
            return render(request, 'changepass.html', {'error_message': "Password cannot be empty."})
        if 'email_id' not in request.session:
            return redirect('login')
        try:
            user = UserRegistration.objects.get(email_id=request.session['email_id'])
            user.password = new_password
            user.save()
            # Send email notification
            email = user.email_id
            subject = "Password Changed Successfully..."
            body = f"Hello,Your password has been successfully changed."
            message = f"Subject: {subject}\n\n{body}"
            try:
                # Use certifi's certificate bundle
                context = ssl.create_default_context(cafile=certifi.where())
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login("ramparagenealogy@gmail.com", "pzkq adso icms rjed")
                    server.sendmail("ramparagenealogy@gmail.com", email, message)
            except Exception as e:
                print("Error sending email:", e)
            return redirect('login')
        except UserRegistration.DoesNotExist:
            return redirect('login')
    return render(request, 'changepass.html')




from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.db import transaction
import csv
from .models import Person, Family, SpouseInfo
import os

@transaction.atomic
def import_data_from_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'status': 'error', 'message': 'File is not a CSV'}, status=400)
    
    # Delete existing data before importing new data
    Person.objects.all().delete()
    Family.objects.all().delete()
    SpouseInfo.objects.all().delete()
    # Define the base directory and file name
    # Example using relative paths and environment variables
    # Define base directory relative to the script's location
    base_dir = os.path.join(os.path.dirname(__file__))
    # print('============================BASE_DIR>>>>>>>>>>>>>>>>>>>>>>>>>>',base_dir)
    # Example using environment variables (ensure it's set in your environment)
    # base_dir = os.getenv('GENEALOGY_DIR', '/path/to/default/family') /Users/neel2004/Desktop/family/genealogy.csv
    # Define the file name
    file_name = 'genealogy.csv'
    # Create the full file path using os.path
    file_path = os.path.join(base_dir, file_name)
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)        
        for row in reader:
            try:
                # Validate the ID
                if not row['ID'].isdigit():
                    continue  # Skip rows with invalid IDs
                
                # Convert ID to an integer
                person_id = int(row['ID'])
                
                # Create or update Person record
                person, created = Person.objects.get_or_create(
                    id=person_id,
                    defaults={
                        'name': row['Name'],
                        'gender': row['Gender'],
                    }
                )
                
                # Update person's name and gender if they differ
                if not created:
                    if person.name != row['Name']:
                        person.name = row['Name']
                    if person.gender != row['Gender']:
                        person.gender = row['Gender']
                    person.save()           
                
                # Find or create father
                father = None
                father_name = row.get('father')
                if father_name and father_name != 'Unknown':
                    fathers = Person.objects.filter(name=father_name, gender='M')
                    if fathers.exists():
                        father = fathers.first()
                    else:
                        father = Person.objects.create(name=father_name, gender='M')
                
                # Find or create mother
                mother = None
                mother_name = row.get('mother')
                if mother_name and mother_name != 'Unknown':
                    mothers = Person.objects.filter(name=mother_name, gender='F')
                    if mothers.exists():
                        mother = mothers.first()
                    else:
                        mother = Person.objects.create(name=mother_name, gender='F')
                
                # Create or get family
                family = None
                if father or mother:
                    # Check if family already exists
                    family_qs = Family.objects.filter(father=father, mother=mother)
                    if family_qs.exists():
                        family = family_qs.first()
                    else:
                        family = Family.objects.create(father=father, mother=mother)
                
                # Add person to family if family exists
                if family:
                    family.children.add(person)
                    family.save()

                # Handle SpouseInfo if applicable
                spouse_names = row.get('spouse_name')
                spouse_fathernames = row.get('spouse_fathername')
                spouse_villages = row.get('spouse_village')
                
                # Split spouse-related fields if they contain ';', otherwise treat as single entries
                if spouse_names and ';' in spouse_names:
                    spouse_names = spouse_names.split(';')
                    spouse_fathernames = spouse_fathernames.split(';') if spouse_fathernames else [''] * len(spouse_names)
                    spouse_villages = spouse_villages.split(';') if spouse_villages else [''] * len(spouse_names)
                else:
                    spouse_names = [spouse_names] if spouse_names else []
                    spouse_fathernames = [spouse_fathernames] if spouse_fathernames else []
                    spouse_villages = [spouse_villages] if spouse_villages else []

                for spouse_name, spouse_fathername, spouse_village in zip(spouse_names, spouse_fathernames, spouse_villages):
                    if spouse_name and spouse_name != 'Unknown':
                        # Create new SpouseInfo
                        SpouseInfo.objects.create(
                            spouse_name=spouse_name,
                            spouse_fathername=spouse_fathername,
                            spouse_village=spouse_village,
                            person=person
                        )
            
            except Exception as e:
                # Log or handle the exception as needed
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    # Redirect to tree_view after successful import
    return redirect('tree_view')

def save_person_details(request):
    if request.method == 'POST':
        person_form = PersonForm(request.POST)
        if person_form.is_valid():
            person = person_form.save()
            # Redirect to import_data_from_csv view
            return redirect('import_data_from_csv')
        else:
            # Handle form errors if needed
            return JsonResponse({'status': 'error', 'message': 'Form data is not valid.'}, status=400)
    else:
        # Handle GET request if needed
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)