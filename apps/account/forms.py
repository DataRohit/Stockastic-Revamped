# Imports
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from apps.account.validators import UsernameValidator

# Get the user model
User = get_user_model()


# User login form
class UserLoginForm(forms.Form):
    """User login form

    Inherits:
        forms.Form

    Fields:
        email (forms.EmailField): Email input field
        password (forms.CharField): Password input field
    """

    # Fields
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        ),
    )


# User registration form
class UserRegisterForm(forms.ModelForm):
    """User registration form

    Inherits:
        forms.Form

    Fields:
        username (forms.CharField): Username input field
        email (forms.EmailField): Email input field
        first_name (forms.CharField): First name input field
        last_name (forms.CharField): Last name input field
        password (forms.CharField): Password input field
        confirm_password (forms.CharField): Password confirmation input field

    Meta:
        model (User): The user model
        fields (List[str]): The fields to include in the form

    Methods:
        clean -> Dict: Get the cleaned data
        save -> User: Save the form
    """

    # Fields
    username = forms.CharField(
        label="Username",
        max_length=60,
        validators=[UsernameValidator],
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your first name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your last name", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter your password", "class": "form-control"}
        ),
        validators=[validate_password],
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm your password", "class": "form-control"}
        ),
    )

    # Method to clean the form
    def clean(self):
        # Get the cleaned data
        cleaned_data = super().clean()

        # Get the password and confirm password
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # If the passwords do not match
        if password != confirm_password:
            # Add an error message
            raise forms.ValidationError("Passwords do not match.")

        # Return the cleaned data
        return cleaned_data

    # Method to save the form
    def save(self, commit=True):
        # Get the cleaned data
        cleaned_data = self.cleaned_data

        # Get the username, email, first name, and last name
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        password = cleaned_data.get("password")

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        # Return the user
        return user

    # Meta
    class Meta:
        # Attributes
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]


# User update form
class UserUpdateForm(forms.ModelForm):
    """User update form

    Inherits:
        forms.ModelForm

    Fields:
        username (forms.CharField): Username input field
        email (forms.EmailField): Email input field
        first_name (forms.CharField): First name input field
        last_name (forms.CharField): Last name input field
        avatar (forms.ImageField): Avatar input field

    Methods:
        clean_username -> str: Get the cleaned username
        clean_email -> str: Get the cleaned email

    Meta:
        model (User): The user model
        fields (List[str]): The fields to include in the form
    """

    # Fields
    username = forms.CharField(
        label="Username",
        max_length=60,
        validators=[UsernameValidator],
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your username", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={"placeholder": "Enter your email", "class": "form-control"}
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your first name", "class": "form-control"}
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=60,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter your last name", "class": "form-control"}
        ),
    )
    avatar = forms.ImageField(
        label="Avatar",
        widget=forms.FileInput(attrs={"class": "form-control", "type": "file"}),
        required=False,
    )

    # Method to get cleaned username
    def clean_username(self):
        # Get the cleaned data
        cleaned_data = self.cleaned_data

        # Get the username
        username = cleaned_data.get("username")

        # Get the user
        user = (
            User.objects.filter(username=username).exclude(pk=self.instance.pk).first()
        )

        # If the user exists
        if user:
            # Add an error message
            raise forms.ValidationError("Username is already taken.")

        # Return the username
        return username

    # Method to get cleaned email
    def clean_email(self):
        # Get the cleaned data
        cleaned_data = self.cleaned_data

        # Get the email
        email = cleaned_data.get("email")

        # Get the user
        user = User.objects.filter(email=email).exclude(pk=self.instance.pk).first()

        # If the user exists
        if user:
            # Add an error message
            raise forms.ValidationError("Email is already taken.")

        # Return the email
        return email

    # Meta
    class Meta:
        # Attributes
        model = User
        fields = ["username", "email", "first_name", "last_name", "avatar"]
