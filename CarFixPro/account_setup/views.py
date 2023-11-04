from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomerRegistrationForm, CustomerLoginForm
from django.http import HttpResponseRedirect
from .models import CustomerInfo
# from django.contrib.auth.hashers import make_password
from passlib.hash import pbkdf2_sha256

# Create your views here.

# def index(request):

#     customer_registration_form = CustomerRegistrationForm()

#     if request.method == "POST":
#         # entered_first_name = request.POST['first_name']
#         # print(entered_first_name)
#         print("Meowww")
#         return HttpResponseRedirect("/thank-you")

#     return render(request, "account_setup/customer_registration.html", {
#         "form" : customer_registration_form
#     })

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