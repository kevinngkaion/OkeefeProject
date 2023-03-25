from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import ModelForm, widgets, ValidationError
from .models import Task, Department, UserDepartment
from django import forms
from django.contrib.auth.models import User


class TaskForm(ModelForm):
    # This is for the styling of the form fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {
            'name': {'class': 'form-control', 'id': 'id_create_name'},
            'user': {'class': 'form-select', 'id': 'id_create_assignedTo'},
            'category': {'class': 'form-select', 'id': 'id_create_category'},
            'priority': {'class': 'form-select', 'id': 'id_create_priority'},
            'date_due': {'class': 'form-control', 'id': 'id_create_due', 'type': 'date'},
            'repeat': {'class': 'form-select', 'id': 'id_create_repeat', },
            'desc': {'class': 'form-control', 'id': 'id_create_desc', 'rows': '5'},
            'interval': {'class': 'form-select', 'id': 'id_create_interval', 'disabled': True},
            'intervalLength': {'class': 'form-control', 'id': 'id_create_intervalLength', 'disabled': True,
                               'placeholder': 'Frequency'},
        }
        self.fields['name'].widget.attrs.update(attrs['name'])
        self.fields['user'].widget.attrs.update(attrs['user'])
        self.fields['category'].widget.attrs.update(attrs['category'])
        self.fields['priority'].widget.attrs.update(attrs['priority'])
        self.fields['date_due'].widget = widgets.DateInput(attrs=attrs['date_due'])
        self.fields['repeat'].widget.attrs.update(attrs['repeat'])
        self.fields['desc'].widget = widgets.Textarea(attrs=attrs['desc'])
        self.fields['interval'].widget.attrs.update(attrs['interval'])
        self.fields['intervalLength'].widget.attrs.update(attrs['intervalLength'])

    class Meta:
        model = Task
        labels = {
            'name': 'Task Name',
            'user': 'Assign To',
            'desc': 'Description',
            'date_due': 'Date Due',
            'repeat': 'Is this a recurring task?',
            'intervalLength': 'Length',
            'repeat': 'Is this a recurring task?'
        }
        fields = [
            'name',
            'user',
            'category',
            'priority',
            'date_due',
            'repeat',
            'intervalLength',
            'interval',
            'desc',
        ]


class EditTaskForm(ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'd-none', 'id': 'id_edit_id', 'hidden': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {
            'user': {'class': 'form-select', 'id': 'id_edit_assignedTo', 'disabled': True},
            'category': {'class': 'form-select', 'id': 'id_edit_category', 'disabled': True},
            'priority': {'class': 'form-select', 'id': 'id_edit_priority', 'disabled': True},
            'date_due': {'class': 'form-control', 'id': 'id_edit_due', 'type': 'date', 'disabled': True},
            'repeat': {'class': 'form-select', 'id': 'id_edit_repeat', 'disabled': True},
            'desc': {'class': 'form-control', 'id': 'id_edit_desc', 'rows': '5', 'readonly': True},
            'interval': {'class': 'form-select', 'id': 'id_edit_interval', 'disabled': True},
            'intervalLength': {
                'class': 'form-control',
                'id': 'id_edit_intervalLength',
                'disabled': True,
                'placeholder': 'Frequency',
            },
            'status': {'class': 'form-select', 'id': 'id_edit_status', 'disabled': True},
            'note': {'class': 'form-control', 'id': 'id_edit_note', 'rows': '2', 'readonly': True},
        }

        self.fields['user'].widget.attrs.update(attrs['user'])
        self.fields['category'].widget.attrs.update(attrs['category'])
        self.fields['priority'].widget.attrs.update(attrs['priority'])
        self.fields['date_due'].widget = widgets.DateInput(attrs=attrs['date_due'])
        self.fields['repeat'].widget.attrs.update(attrs['repeat'])
        self.fields['desc'].widget = widgets.Textarea(attrs=attrs['desc'])
        self.fields['interval'].widget.attrs.update(attrs['interval'])
        self.fields['intervalLength'].widget.attrs.update(attrs['intervalLength'])
        self.fields['status'].widget.attrs.update(attrs['status'])
        self.fields['note'].widget = widgets.Textarea(attrs=attrs['note'])

    class Meta:
        model = Task
        labels = {
            'status': 'Status',
            'user': 'Assign To',
            'desc': 'Description',
            'date_due': 'Date Due',
            'repeat': 'Is this a recurring task?',
            'note': 'Notes'
        }
        fields = [
            'id',
            'status',
            'user',
            'category',
            'priority',
            'date_due',
            'repeat',
            'intervalLength',
            'interval',
            'desc',
            'note',
        ]


class CreateUserForm(UserCreationForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {
            'username': {'class': 'form-control', 'id': 'id_create_username', },
            'first_name': {'class': 'form-control', 'id': 'id_create_first_name', },
            'last_name': {'class': 'form-control', 'id': 'id_create_last_name', },
            'email': {'class': 'form-control', 'id': 'id_create_email', },
            'department': {'class': 'form-select', 'id': 'id_create_department', },
            'password1': {'class': 'form-control', 'id': 'id_create_password1', },
            'password2': {'class': 'form-control', 'id': 'id_create_password2', },
        }

        self.fields['username'].widget.attrs.update(attrs['username'])
        self.fields['first_name'].widget.attrs.update(attrs['first_name'])
        self.fields['last_name'].widget.attrs.update(attrs['last_name'])
        self.fields['email'].widget.attrs.update(attrs['email'])
        self.fields['department'].widget.attrs.update(attrs['department'])
        self.fields['password1'].widget.attrs.update(attrs['password1'])
        self.fields['password2'].widget.attrs.update(attrs['password2'])

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'department')


# A user creation form that includes the fields of the built-in UserCreationForm, also including department in the
# Department table. Enter password twice to ensure it is entered correctly.
class MyCreateUserForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Password, 8 characters minimum')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        attrs = {
            'username': {'class': 'form-control', 'id': 'id_create_username', },
            'first_name': {'class': 'form-control', 'id': 'id_create_first_name', },
            'last_name': {'class': 'form-control', 'id': 'id_create_last_name', },
            'email': {'class': 'form-control', 'id': 'id_create_email', },
            'department': {'class': 'form-select', 'id': 'id_create_department', },
            'password1': {'class': 'form-control', 'id': 'id_create_password1', },
            'password2': {'class': 'form-control', 'id': 'id_create_password2', },
        }

        self.fields['username'].widget.attrs.update(attrs['username'])
        self.fields['first_name'].widget.attrs.update(attrs['first_name'])
        self.fields['last_name'].widget.attrs.update(attrs['last_name'])
        self.fields['email'].widget.attrs.update(attrs['email'])
        self.fields['department'].widget.attrs.update(attrs['department'])
        self.fields['password1'].widget.attrs.update(attrs['password1'])
        self.fields['password2'].widget.attrs.update(attrs['password2'])

    class Meta:
        model = User
        labels = {'username': 'Username',
                  'first_name': 'First Name',
                  'last_name': 'Last Name',
                  'email': 'Email',
                  'department': 'Department',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  }

        fields = ['username', 'first_name', 'last_name', 'email', 'department', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
            self.add_error('password2', "Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.department = self.cleaned_data['department']
        if commit:
            user.save()
        return user


class EditUserForm(ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['department'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['first_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['last_name'].widget = widgets.TextInput(attrs={'class': 'form-control', 'disabled': True})
        self.fields['email'].widget = widgets.EmailInput(attrs={'class': 'form-control', 'disabled': True})

    class Meta:
        model = User
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'department': 'Department',
        }
        fields = [
            'username',
            'department',
            'first_name',
            'last_name',
            'email',
        ]


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="email",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if user is None:
                raise ValidationError(
                    "Invalid email or password. Please try again."
                )

        return self.cleaned_data


class MyUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class MyResetPasswordForm(forms.ModelForm):
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two passwords do not match")
        return cleaned_data
