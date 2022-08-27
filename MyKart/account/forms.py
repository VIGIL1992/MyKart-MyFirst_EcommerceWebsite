from distutils.command.clean import clean
from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'Placeholder' : 'Enter pasword'                                                      
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'Placeholder' : 'Confirm pasword'                                                      
    }))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phonenumber', 'email', 'password'] 

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last name'
        self.fields['phonenumber'].widget.attrs['placeholder'] = 'Enter phonenumber'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )