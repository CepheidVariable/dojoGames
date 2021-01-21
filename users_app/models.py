from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def cleanup_spaces(self, post_pattern1=None, post_pattern2=None, post_pattern3=None):
        '''
        Strips erroneous spacing around data, and inbetween based of several patterns
        PATTERN1: all spaces and newline characters
        PATTERN2: any double spaces, but allows newline characters

        Note: the parameter post_pattern3 is a special case of PATTERN1 for use with usernames where spaces are not desirable.
        '''
        PATTERN1 = re.compile(r'\s+')
        PATTERN2 = re.compile(r' {2,}')
        
        if post_pattern1 is not None:
            clean_post = re.sub(PATTERN1, ' ', post_pattern1).strip()
        elif post_pattern2 is not None:
            clean_post = re.sub(PATTERN2, ' ', post_pattern2).strip()
        else:
            clean_post = re.sub(PATTERN1, '', post_pattern3).strip()


        return clean_post

    def validate(self, post_data):
        errors = {}
        AGE_LIMIT = 13
        TODAY = date.today()

        PATTERN_NAME = re.compile(r"(?i)^[a-z ,.'-]+$")
        PATTERN_USERNAME = re.compile(r"^(?=.{8,25}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")
        PATTERN_EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        PATTERN_PWD = re.compile(r"^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$")

        test_username = User.objects.cleanup_spaces(post_pattern3=post_data['username'])
        test_first_name = User.objects.cleanup_spaces(post_pattern1=post_data['first_name'])
        test_last_name = User.objects.cleanup_spaces(post_pattern1=post_data['last_name'])
        test_email = User.objects.cleanup_spaces(post_pattern1=post_data['email'])
        test_password = User.objects.cleanup_spaces(post_pattern1=post_data['password'])
        print(test_username, test_first_name, test_last_name, test_email)
        
        # Validate username
        if User.objects.filter(username=test_username).exists():
            errors['duplicate'] = "User with that title already exists."
        if not PATTERN_USERNAME.match(test_username):
            errors['username'] = "Username must be between 8-25 characters in length. "\
            + "Contain alphanumeric characters, underscore or dot. "\
            + "Underscore or dot cannot be next to each other, occur multiple times, or be at the start/end."

        # Validate first and last name
        if not PATTERN_NAME.match(test_first_name):
            errors['first_name'] = "First name invalid"
        if not PATTERN_NAME.match(test_last_name):
            errors['last_name'] = "Last name invalid"

        #Validate date of birth
        if post_data['dob'] == '':
            errors['dob'] = "DOB is invalid"
        else:
            if (datetime.strptime(post_data['dob'], '%Y-%m-%d') > datetime.today()):
                errors['dob'] = "DOB is invalid"
            else:
                dob = datetime.strptime(post_data['dob'], '%Y-%m-%d').date()
                age = TODAY.year - dob.year - ((TODAY.month, TODAY.day) < (dob.month, dob.day))
                if age < AGE_LIMIT:
                    errors['age'] = "Must be 13 or older to register."

        # Validate email
        if not PATTERN_EMAIL.match(test_email):
            errors['email'] = "Email invalid"

        # If PATTERN_PWD matches, input is not valid
        if PATTERN_PWD.match(test_password):
            errors['password'] = "Password must be at least 8 characters in length, include one uppercase letter, one special character, and alphanumeric characters."

        
        return errors


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=35,)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=254, unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()