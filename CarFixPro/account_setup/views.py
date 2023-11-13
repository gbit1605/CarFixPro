from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomerRegistrationForm, CustomerLoginForm, AddVehicleForm, BookAppointment
from django.http import HttpResponseRedirect
from .models import CustomerInfo, Vehicle, Appointment, Location, Service
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