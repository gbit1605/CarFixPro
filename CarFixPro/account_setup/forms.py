from django import forms

class CustomerRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="First name", error_messages={
        "required" : "Please enter your first name!",
        "max_length" : "Your first name should not exceed 30 characters!"
    })
    last_name = forms.CharField(max_length=30, label="Last name")
    address = forms.CharField(max_length=100, label="Address")
    phone = forms.CharField(max_length=10, label="Phone number")
    email = forms.EmailField(label="Email ID")
    credit_card_number = forms.CharField(max_length=16, label="Credit card number")
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)

class CustomerLoginForm(forms.Form):
    username = forms.EmailField(label="Your email is your username")
    password = forms.CharField(max_length=32, required=True, widget=forms.PasswordInput)

class AddVehicleForm(forms.Form):

    CHOICES  = [('Sedan', 'Sedan'), ('SUV', 'SUV'), ('Hatchback', 'Hatchback'), ('Crossover', 'Crossover')]

    vin = forms.CharField(max_length=17, label="VIN")
    model = forms.CharField(max_length=50, label="Model")
    year = forms.CharField(max_length=4, label="Year")
    color = forms.CharField(max_length=10, label="Color")
    mfg_company = forms.CharField(max_length=20, label="Brand")
    vtype = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class':'form-control'}), label="Type")
