from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Person,SpouseInfo, Family, UserRegistration, ContactMessage
from .forms import FamilyForm, PersonForm, SpouseInfoForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from django.core.mail import EmailMessage
# from django.conf import settings
# import random, smtplib, ssl
# from django.template.loader import get_template
# This view renders the tree.html template
def render_tree_view(request):
    return render(request, 'tree.html')

# Generate tree data starting from a person
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
        for child in children:
            data["children"].append(generate_tree_data(child))

    # Find families where the person is the mother
    families_as_mother = Family.objects.filter(mother=person)
    for family in families_as_father & families_as_mother:
        # Get children who are sons (assuming male children)
        sons = family.children.filter(gender='M')
        for son in sons:
            # Recursively generate data for each child
            data["children"].append(generate_tree_data(son))
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
    try:
        root_person = Person.objects.get(name="Anandsinhji")
    except Person.DoesNotExist:
        return JsonResponse({"error": "Root person not found"}, status=404)
    tree_data = generate_tree_data(root_person)
    return JsonResponse(tree_data)

# This view displays details of a person
def person_detail(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    families = Family.objects.filter(father=person).prefetch_related('children')
    spouses = person.spouses.all()
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

# This view displays details of a child
def child_detail(request, child_id):
    child = get_object_or_404(Person, pk=child_id)
    family = Family.objects.filter(children=child).first()
    father = family.father if family else None
    mother = family.mother if family else None
    spouses = child.spouses.all()
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

def RegisterUserView(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')
        # user_data = UserRegistration.objects.get(id=user_registration.id)
        # subject = 'Registration Succesfully'
        # ctx = {
        #         'first_name': first_name,
        #         'last_name': last_name,
        #         }
        # message = get_template('email.html').render(ctx)
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [user_data.email_id]
        # msg=EmailMessage(subject,message,email_from,recipient_list)
        # msg.content_subtype= 'html'
        # msg.send()
        user_registration = UserRegistration(
            first_name=first_name,
            last_name=last_name,
            email_id=email_id,
            password=password
        )
        user_registration.save()
        return redirect('login')
    return render(request, 'signup.html')

def LoginUserView(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        password = request.POST.get('password')
        user_registration = UserRegistration.objects.filter(email_id=email).last()
        if user_registration and user_registration.password == password:
            request.session['email'] = email
            request.session['first_name'] = user_registration.first_name
            return redirect('tree_view')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('/'))

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
def create_person(request):
    if request.method == 'POST':
        person_form = PersonForm(request.POST)
        if person_form.is_valid() :
            person_form.save()
        return redirect('create_spouse')
    else:
        person_form = PersonForm()
    return render(request, 'person_form.html', {'person_form': person_form})


def create_spouse(request):
    if request.method == 'POST':
        spouse_form = SpouseInfoForm(request.POST)
        if spouse_form.is_valid():
            spouse_form.save()
            return redirect('create_family')
    else:
        spouse_form = SpouseInfoForm()
    return render(request, 'spouse_form.html',{'spouse_form':spouse_form})


def create_family(request):
    if request.method == 'POST':
        family_form = FamilyForm(request.POST)
        if family_form.is_valid():
            family = family_form.save()
            children_ids = request.POST.getlist('children')
            for child_id in children_ids:
                child = Person.objects.get(id=child_id)
                family.children.add(child)
            return redirect('tree_view')
    else:
        family_form = FamilyForm()
        # Filter the queryset for father and mother fields based on gender
        family_form.fields['father'].queryset = Person.objects.filter(gender='M')
        family_form.fields['mother'].queryset = Person.objects.filter(gender='F')
    return render(request, 'family_form.html', {'family_form': family_form})

# Update an existing person
def update_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        person_form = PersonForm(request.POST, instance=person)
        if person_form.is_valid():
            person_form.save()
            # Redirect to the update_spouse view with the spouse's ID
            return redirect('person_detail', person_id=person.id)
    else:
        person_form = PersonForm(instance=person)
    return render(request, 'person_edit_form.html', {'person_form': person_form})

def update_spouse(request, spouse_id):
    spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
    if request.method == 'POST':
        spouse_form = SpouseInfoForm(request.POST, instance=spouse)
        if spouse_form.is_valid():
            spouse_form.save()
            # Redirect to the update_family view with the spouse's ID
            return redirect('tree_view')
    else:
        spouse_form = SpouseInfoForm(instance=spouse)
    return render(request, 'spouse_edit_form.html', {'spouse_form': spouse_form})

def update_family(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    if request.method == 'POST':
        family_form = FamilyForm(request.POST, instance=family)
        if family_form.is_valid():
            family_form.save()
            # Redirect to the family_detail view with the family's ID
            return redirect('tree_view')
    else:
        family_form = FamilyForm(instance=family)
    return render(request, 'family_edit_form.html', {'family_form': family_form})

# Delete a person
def delete_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    if request.method == 'POST':
        person.delete()
        return redirect('tree_view')
    return render(request, 'person_confirm_delete.html', {'person': person})

def delete_spouse(request, spouse_id):
    spouse = get_object_or_404(SpouseInfo, pk=spouse_id)
    if request.method == 'POST':
        spouse.delete()
        return redirect('tree_view')
    return render(request, 'spouse_confirm_delete.html', {'spouse': spouse})

def delete_family(request, family_id):
    family = get_object_or_404(Family, pk=family_id)
    if request.method == 'POST':
        family.delete()
        return redirect('tree_view')
    return render(request, 'family_confirm_delete.html', {'family': family})

# def forgotpass(request):
#     if request.method == 'POST':
#         email = request.POST.get('email_id')
#         if not email:
#             return render(request, 'getemail.html',{'error_message':"Invalid email address. Please enter a valid email."})
#         otp = ''.join(random.choices('1234567890', k=4))  
#         request.session['otp'] = otp
#         try:
#             server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context())
#             server.login("neelrajsinhzala27@gmail.com", "syik suwx zkxf icga")
#             server.sendmail("neelrajsinhzala27@gmail.com", email, otp)
#             server.quit()
#         except Exception as e:
#             print("Error sending email:", e)
#             return HttpResponse("Failed to send OTP email. Please try again.")
#         request.session['email_id'] = email
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
#             return HttpResponse('<a href="">Wrong OTP entered.</a>')
#     return render(request, 'otp.html')

# def changepass(request):
#     if request.method == 'POST':
#         new_password = request.POST.get('password')
#         if not new_password:
#             return render(request, 'changepass.html')
#         if 'email_id' not in request.session:
#             return redirect('login')
#         user = UserRegistration.objects.get(email_id=request.session['email_id'])
#         user.password = new_password
#         user.save()
#         return redirect('login')
#     return render(request, 'changepass.html')