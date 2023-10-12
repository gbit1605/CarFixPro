from django.shortcuts import render
from django.http import HttpResponse
from .forms import CustomerRegistrationForm
from django.http import HttpResponseRedirect

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
            print(customer_registration_form.cleaned_data)
            return HttpResponseRedirect("/thank-you")

    else:
        customer_registration_form = CustomerRegistrationForm()

    return render(request, "account_setup/customer_registration.html", {
        "form": customer_registration_form
    })

def thank_you(request):
    return render(request, 'account_setup/thank_you.html')
