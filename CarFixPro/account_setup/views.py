from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomerRegistrationForm, CustomerLoginForm, AddVehicleForm, BookAppointment, ManagerLoginForm, AppointmentApprovalForm, TechnicianRegistrationForm, AddTechnicianSkillsForm, AddTechnicianSkillsChoicesForm, TechnicianLoginForm, TechnicianCompletionForm, ManagerAppointmentFinishApprovalForm, DeleteTechnicianSkillsForm, DeleteTechnicianSkillsChoicesForm
from django.http import HttpResponseRedirect
from .models import CustomerInfo, Vehicle, Appointment, Location, Service, ManagerInfo, TechnicianInfo, TechnicianSkills, AppointmentStatus
from passlib.hash import pbkdf2_sha256

def index(request):
    if request.method == 'POST':
        customer_registration_form = CustomerRegistrationForm(request.POST)

        if customer_registration_form.is_valid():
            cinfo = CustomerInfo(fname=customer_registration_form.cleaned_data['first_name'],
                                 lname=customer_registration_form.cleaned_data['last_name'],
                                 address=customer_registration_form.cleaned_data['address'],
                                 phone=customer_registration_form.cleaned_data['phone'],
                                 email_id=customer_registration_form.cleaned_data['email'],
                                 c_number=customer_registration_form.cleaned_data['credit_card_number'],
                                 passwd=pbkdf2_sha256.encrypt(customer_registration_form.cleaned_data['password'], rounds=12000, salt_size=32))
            cinfo.save()

            return HttpResponseRedirect("/thank-you")

    else:
        customer_registration_form = CustomerRegistrationForm()

    return render(request, "account_setup/customer_registration.html", {
        "form": customer_registration_form
    })

def thank_you(request):
    return render(request, 'account_setup/thank_you.html')

def customer_login(request):
    if request.method == 'POST':
        customer_login_form = CustomerLoginForm(request.POST)

        if customer_login_form.is_valid():
            uname=customer_login_form.cleaned_data['username']
            passwd=customer_login_form.cleaned_data['password']
            stored_password = CustomerInfo.objects.filter(email_id=uname)[0].passwd
            is_verified = pbkdf2_sha256.verify(passwd, stored_password)

            request.session['user_email'] = customer_login_form.cleaned_data['username']
            
            if is_verified:
                return HttpResponseRedirect("/customer_dashboard")
            return HttpResponseRedirect("/customer_login")

    else:
        customer_login_form = CustomerLoginForm()

    return render(request, "account_setup/customer_login.html", {
        "form": customer_login_form
    })

def customer_dashboard(request):
    return render(request, 'account_setup/home_page.html')

def manager_dashboard(request):
    return render(request, 'account_setup/manager_dashboard.html')

def technician_dashboard(request):
    return render(request, 'account_setup/technician_dashboard.html')

def book_appointment(request):

    user_email = request.session.get('user_email', None)
    customer_vehicle_objects = Vehicle.objects.all()
    location_objects = Location.objects.all()
    service_objects = Service.objects.all()
    vehicle_details, location_details, serivces_details = [], [], []

    for i in customer_vehicle_objects:
        if i.customer_email.email_id == user_email:
            vdetails = str(i.vin) + ", " + str(i.mfg_company) + ", " + str(i.model) + ", " + str(i.color) + ", " + str(i.vtype)
            vehicle_details.append(vdetails)
    
    for i in location_objects:
        location_details.append(str(i.address) + " " + str(i.state) + " " + str(i.pincode))

    vehicle_details_dropdown = [(i, i) for i in vehicle_details]
    location_details_dropdown = [(location_details[i], location_details[i]) for i in range(len(location_details))]
    selected_services = []
    total_cost = 0
    if request.method == 'POST':

        book_appointment_form = BookAppointment(request.POST, vehicle_choices=vehicle_details_dropdown, location_choices=location_details_dropdown)

        if book_appointment_form.is_valid():
            date = book_appointment_form.cleaned_data['date']
            selected_services = [", ".join(str(i) for i in book_appointment_form.cleaned_data['services_details'])]
            vid = book_appointment_form.cleaned_data['vehicle_details'][:17]
            vtype = book_appointment_form.cleaned_data['vehicle_details'].split(", ")[-1]
            loc_address = book_appointment_form.cleaned_data['location_details']

            for service in selected_services[0].split(", "):
                total_cost += Service.objects.get(service_type=service, vehicle_type=vtype).price

            ainfo = Appointment(date=date,
                            location=loc_address,
                            vehicle_id=vid,
                            vehicletype=vtype,
                            service_details = selected_services[0],
                            total_price = total_cost,
                            customer_email = CustomerInfo.objects.get(email_id=user_email))
            ainfo.save()

            return HttpResponseRedirect("/thank-you")

    else:
        book_appointment_form = BookAppointment(vehicle_choices=vehicle_details_dropdown, location_choices=location_details_dropdown)

    return render(request, "account_setup/book_appointment.html", {
        "form": book_appointment_form
    })

def add_vehicle(request):
    user_email = request.session.get('user_email', None)
    

    if request.method == 'POST':
        vehicle_registration_form = AddVehicleForm(request.POST)

        if vehicle_registration_form.is_valid():
            vinfo = Vehicle(vin=vehicle_registration_form.cleaned_data['vin'],
                            model=vehicle_registration_form.cleaned_data['model'],
                            year=vehicle_registration_form.cleaned_data['year'],
                            color=vehicle_registration_form.cleaned_data['color'],
                            mfg_company=vehicle_registration_form.cleaned_data['mfg_company'],
                            vtype=vehicle_registration_form.cleaned_data['vtype'],
                            customer_email = CustomerInfo.objects.get(email_id=user_email))
            vinfo.save()

            return HttpResponseRedirect("/thank-you")

    else:
        vehicle_registration_form = AddVehicleForm()

    return render(request, "account_setup/add_vehicle.html", {
        "form": vehicle_registration_form
    })

def manager_login(request):
    if request.method == 'POST':
        manager_login_form = ManagerLoginForm(request.POST)

        if manager_login_form.is_valid():
            uname=manager_login_form.cleaned_data['username']
            passwd=manager_login_form.cleaned_data['password']
            stored_password = ManagerInfo.objects.filter(email_id=uname)[0].passwd
            is_verified = pbkdf2_sha256.verify(passwd, stored_password)

            request.session['user_email'] = manager_login_form.cleaned_data['username']
            
            if is_verified:
                return HttpResponseRedirect("/manager_dashboard")
            return HttpResponseRedirect("/manager_login")

    else:
        manager_login_form = ManagerLoginForm()

    return render(request, "account_setup/manager_login.html", {
        "form": manager_login_form
    })


def manager_pending_approvals(request):
    pending_appointments = Appointment.objects.filter(manager_start_approval=False)
    
    if request.method == 'POST':
        form = AppointmentApprovalForm(request.POST)
        if form.is_valid():
            appointment_id = request.POST.get('appointment_id')
            
            # Use appointment_id to retrieve and update the corresponding appointment
            appointment_instance = Appointment.objects.get(appointment_id=appointment_id)
            
            appointment_instance.manager_start_approval = True  # Set manager_start_approval to True
            appointment_instance.save()
            # You can add a success message or redirect to a different page after submission
            return redirect('/manager_pending_approvals')
    else:
        form = AppointmentApprovalForm()

    return render(request, 'account_setup/manager_pending_approvals.html', {'pending_appointments': pending_appointments, 'form': form})


def technician_registration(request):
    location_objects = Location.objects.all()
    location_details = []
    user_email = request.session.get('user_email', None)
    for i in location_objects:
        location_details.append(str(i.address) + " " + str(i.state) + " " + str(i.pincode))

    location_details_dropdown = [(location_details[i], location_details[i]) for i in range(len(location_details))]
    if request.method == 'POST':
        technician_registration_form = TechnicianRegistrationForm(request.POST, location_choices=location_details_dropdown)

        if technician_registration_form.is_valid():
            
            tinfo = TechnicianInfo(SSN=technician_registration_form.cleaned_data['ssn'],
                                 fname=technician_registration_form.cleaned_data['first_name'],
                                 lname=technician_registration_form.cleaned_data['last_name'],
                                 address=technician_registration_form.cleaned_data['address'],
                                 phone=technician_registration_form.cleaned_data['phone'],
                                 email_id=technician_registration_form.cleaned_data['email'],
                                 acc_number=technician_registration_form.cleaned_data['acc_number'],
                                 hourly_rate = technician_registration_form.cleaned_data['hourly_rate'],
                                 mngr = ManagerInfo.objects.get(email_id=user_email),
                                 hire_date = technician_registration_form.cleaned_data['hire_date'],
                                 location = technician_registration_form.cleaned_data['location'],
                                 passwd=pbkdf2_sha256.encrypt(technician_registration_form.cleaned_data['password'], rounds=12000, salt_size=32))
            tinfo.save()

            return HttpResponseRedirect("/thank-you")

    else:
        technician_registration_form = TechnicianRegistrationForm(location_choices=location_details_dropdown)

    return render(request, "account_setup/technician_registration.html", {
        "form": technician_registration_form
    })

def add_technician_skills(request):

    list_of_technicians = [(i.email_id, i.email_id) for i in TechnicianInfo.objects.all()]

    if request.method == 'POST':
        
        add_technician_skills_form = AddTechnicianSkillsForm(request.POST, technician_choices=list_of_technicians)

        if add_technician_skills_form.is_valid():
            request.session['technician_email'] = add_technician_skills_form.cleaned_data['technician']
            return redirect('/add_technician_skills/' + str(request.session.get('technician_email', None)))

    else:
        add_technician_skills_form = AddTechnicianSkillsForm(technician_choices=list_of_technicians)

    return render(request, "account_setup/add_technician_skills.html", {
        "form": add_technician_skills_form
    })

def add_technician_skills_choices(request, test_number):
    list_of_technicians = [(test_number, test_number)]

    CHOICES_SERVICES = [
    'Maintenance and Repairs',
    'Diagnostic Services',
    'Body and Paint Services',
    'Detailing Services',
    'Customization Services',
    'Towing and Recovery Services',
    'Pre-Purchase Inspection',
    'Rental and Leasing Services',
    'Consultation and Advice']

    technician_skills = [skill_obj.service_type for skill_obj in TechnicianSkills.objects.filter(email_id=test_number)]
    technician_skills_remaining = []
    for skill in technician_skills:
        CHOICES_SERVICES.remove(skill)
    CHOICES_SERVICES = [(s, s) for s in CHOICES_SERVICES]

    if request.method == 'POST':
        
        add_technician_skills_choices_form = AddTechnicianSkillsChoicesForm(request.POST, technician_choices=list_of_technicians, service_choices=CHOICES_SERVICES)

        if add_technician_skills_choices_form.is_valid():
            selected_services = add_technician_skills_choices_form.cleaned_data['services']
            for service in selected_services:
                service_instance = TechnicianSkills(email_id=test_number, service_type=service)
                service_instance.save()
            return HttpResponseRedirect("/thank-you")

    else:
        add_technician_skills_choices_form = AddTechnicianSkillsChoicesForm(technician_choices=list_of_technicians, service_choices=CHOICES_SERVICES)

    return render(request, "account_setup/add_technician_skills_choices.html", {
        "form": add_technician_skills_choices_form, 'test_number':test_number
    })

def delete_technician_skills(request):

    list_of_technicians = [(i.email_id, i.email_id) for i in TechnicianInfo.objects.all()]

    if request.method == 'POST':
        
        delete_technician_skills_form = DeleteTechnicianSkillsForm(request.POST, technician_choices=list_of_technicians)

        if delete_technician_skills_form.is_valid():
            request.session['technician_email'] = delete_technician_skills_form.cleaned_data['technician']
            return redirect('/delete_technician_skills/' + str(request.session.get('technician_email', None)))

    else:
        delete_technician_skills_form = DeleteTechnicianSkillsForm(technician_choices=list_of_technicians)

    return render(request, "account_setup/delete_technician_skills.html", {
        "form": delete_technician_skills_form
    })

def delete_technician_skills_choices(request, test_number):
    list_of_technicians = [(test_number, test_number)]

    technician_skills = [(skill_obj.service_type, skill_obj.service_type) for skill_obj in TechnicianSkills.objects.filter(email_id=test_number)]

    if request.method == 'POST':
        
        delete_technician_skills_choices_form = DeleteTechnicianSkillsChoicesForm(request.POST, technician_choices=list_of_technicians, service_choices=technician_skills)

        if delete_technician_skills_choices_form.is_valid():
            selected_services = delete_technician_skills_choices_form.cleaned_data['services']
            for service in selected_services:
                service_instance = TechnicianSkills.objects.get(email_id=test_number, service_type=service)
                service_instance.delete()
            return HttpResponseRedirect("/thank-you")

    else:
        delete_technician_skills_choices_form = DeleteTechnicianSkillsChoicesForm(technician_choices=list_of_technicians, service_choices=technician_skills)

    return render(request, "account_setup/add_technician_skills_choices.html", {
        "form": delete_technician_skills_choices_form, 'test_number':test_number
    })

def technician_login(request):
    if request.method == 'POST':
        technician_login_form = TechnicianLoginForm(request.POST)

        if technician_login_form.is_valid():
            uname=technician_login_form.cleaned_data['username']
            passwd=technician_login_form.cleaned_data['password']
            stored_password = TechnicianInfo.objects.filter(email_id=uname)[0].passwd
            is_verified = pbkdf2_sha256.verify(passwd, stored_password)

            request.session['technician_email'] = technician_login_form.cleaned_data['username']
            
            if is_verified:
                return HttpResponseRedirect("/technician_dashboard")
            return HttpResponseRedirect("/technician_login")

    else:
        technician_login_form = TechnicianLoginForm()

    return render(request, "account_setup/technician_login.html", {
        "form": technician_login_form
    })  

def technician_pending_appointments(request):
    all_appointments = AppointmentStatus.objects.filter(completed=False)
    technician_email = request.session.get('technician_email', None)
    technician_skills = [skill.service_type for skill in TechnicianSkills.objects.filter(email_id=technician_email)]
    appointments_for_technician = []
    for appointment in all_appointments:
        if appointment.service_detail in technician_skills:
            appointments_for_technician.append(appointment)
    
    if request.method == 'POST':
        form = TechnicianCompletionForm(request.POST)
        if form.is_valid():
            appointment_id = request.POST.get('appointment')
            print(appointment_id)
            service_detail = request.POST.get('service_detail')

            appointment_status_instance = AppointmentStatus.objects.get(appointment=appointment_id, service_detail=service_detail)
            
            appointment_status_instance.completed = True  
            appointment_status_instance.save()

            return redirect('/technician_pending_appointments')
    else:
        form = TechnicianCompletionForm()
    return render(request, 'account_setup/technician_pending_appointments.html', {'appointments_for_technician':appointments_for_technician, 'form': form})
    
def manager_appointment_finish_approval(request):
    appointment_objects = Appointment.objects.filter(manager_start_approval=True, manager_finish_approval=False)
    completed_appointments = []
    for appointment in appointment_objects:
        appointment_status = all([app.completed for app in AppointmentStatus.objects.filter(appointment=appointment.appointment_id)])
        if appointment_status:
            completed_appointments.append(appointment)
    print(completed_appointments)
    if request.method == 'POST':
        form = ManagerAppointmentFinishApprovalForm(request.POST)
        if form.is_valid():
            appointment_id = request.POST.get('appointment_id')

            appointment_instance = Appointment.objects.get(appointment_id=appointment_id)
            
            appointment_instance.manager_finish_approval = True  
            appointment_instance.save()

            return redirect('/manager_appointment_finish_approval')
    else:
        form = ManagerAppointmentFinishApprovalForm()
    return render(request, 'account_setup/manager_appointment_finish_approval.html', {'appointments_for_manager':completed_appointments, 'form': form})