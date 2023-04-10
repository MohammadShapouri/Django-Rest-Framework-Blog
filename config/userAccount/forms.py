from django import forms
from .models import UserAccount
from django.contrib.auth.forms import UserCreationForm
from django.utils.html import format_html
from django.contrib.auth.validators import ASCIIUsernameValidator




class UserAccountForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(UserAccountForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "رمز"
        self.fields['password2'].label = "تکرار رمز"
        self.fields['password1'].help_text = format_html("<ul>  <li>{}</li> <li>{}</li> <li>{}</li>  <ul>".format(
                                                            "دست کم ۸ کاراکتر داشته باشد.",
                                                            "شامل حروف باشد.",
                                                            "مشابه داده های دیگر نباشد."
                                                            )
                                                        )
        self.fields['password2'].help_text = format_html("<ul>  <li>{}</li>  <ul>".format(
                                                            "رمز را تکرار کنید."
                                                            )
                                                        )
        

    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email']



    def clean_username(self):
        cleaned_data = super(UserAccountForm, self).clean()
        username = cleaned_data.get('username')

        try:
            ASCIIUsernameValidator()
        except forms.ValidationError:
            raise forms.ValidationError([{'username' : "نام کاربری ساختار نامعتبری دارد."}])

        try:
            user = UserAccount.objects.get(username = username)
        except UserAccount.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "نام کاربری در حال استفاده است."}])



    def clean_email(self):
        cleaned_data = super(UserAccountForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = UserAccount.objects.get(email = email)
        except UserAccount.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : " ایمیل در حال استفاده است."}])





class EditUserAccountForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.form_request = kwargs.pop('request', None)
        super(EditUserAccountForm, self).__init__(*args, **kwargs)


    class Meta:
        model = UserAccount
        fields = ['first_name', 'last_name', 'username', 'email', 'profile_picture']




    def clean_username(self):
        cleaned_data = super(UserAccountForm, self).clean()
        username = cleaned_data.get('username')

        try:
            ASCIIUsernameValidator()
        except forms.ValidationError:
            raise forms.ValidationError([{'username' : "نام کاربری ساختار نامعتبری دارد."}])

        try:
            user = UserAccount.objects.get(username = username)
        except UserAccount.DoesNotExist:
            return username
        else:
            if self.form_request.user.username == username:
                return username
            else:
                raise forms.ValidationError([{'username' : "نام کاربری در حال استفاده است."}])




    def clean_email(self):
        cleaned_data = super(UserAccountForm, self).clean()
        email = cleaned_data.get('email')

        try:
            user = UserAccount.objects.get(email = email)
        except UserAccount.DoesNotExist:
            return email
        else:
            if self.form_request.user.email == email:
                return email
            else:
                raise forms.ValidationError([{'email' : " ایمیل در حال استفاده است."}])




class LoginForm(forms.Form):

    email = forms.EmailField(required=True, label="ایمیل", error_messages={'email' : "ایمیل ساختار نادرستی دارد."})
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز", error_messages={'password' : "رمز ساختار نادرستی دارد."})