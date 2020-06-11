from django.apps import apps
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

userInfo = apps.get_model('login' , 'user')


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        print(username+" "+password)
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError('This user does not exist')

            if not user.is_active:
                raise forms.ValidationError('User is not activated!')
#            user = authenticate(username=username, password=password)

            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            # if not user.is_active:
            #     raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class LoginForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': ' Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ' Password'}))

    class Meta:
        model = User
        fields = ['email', 'password']

    def authenticate_data(self, email, password):
        user = User.objects.filter(email=email)
        if not user:
            return False
        user = User.objects.get(email=email)
        if user.password != password:
            return False
        return True

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-10 '


class UserForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': ' Name'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': ' Email'}))
    contact = forms.RegexField(regex=r'^\+?1?\d{9,16}$', widget=forms.TextInput(
        attrs={'placeholder': ' Contact no. (+92xxxxxxxxxx)'}))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ' Password'}))
    confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ' Confirm Password'}))

    class Meta:
        model = userInfo
        fields = ['name', 'email', 'contact', 'password','confirm']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm = self.__getitem__('confirm')
        confirm= confirm.value()
        #confirm = self.cleaned_data.get('confirm')
        print(str(password))
        print(str(confirm))
        if len(password) < 6:
            raise forms.ValidationError("Password should be 6 or more characters long")
            return False
        elif str(password) != str(confirm):
            print(type(confirm))
            raise forms.ValidationError("Password not same")
            return False
        return True

    def authenticate_data(self, email):
        user = userInfo.objects.filter(email=email)
        if user:
            #raise forms.ValidationError("User Already Exists.")
            print("User Already Exists.")
            return False
        return True
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-12 col-sm-12  col-lg-12 '

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    contact = forms.RegexField(regex=r'^\+?1?\d{9,16}$', widget=forms.TextInput(
        attrs={'placeholder': ' Contact no. (+92xxxxxxxxxx)'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'contact', 'password1', 'password2')

    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Password must match")
        username = User.objects.filter(username=self.cleaned_data.get('username'))
        email_qs = User.objects.filter(email=self.cleaned_data.get('email'))
        if username.exists():
            raise forms.ValidationError(
                "Username already exists")
        if email_qs.exists():
            raise forms.ValidationError(
                "Email already exists")
        return super(SignupForm, self).clean(*args, **kwargs)