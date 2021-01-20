from django.db import models
import re
from datetime import datetime

class UserManager(models.Manager):
    def cleanup_spaces(self, post_pattern1=None, post_pattern2=None, post_pattern3=None):
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

        user = User.objects.all()

        # PATTERN_TITLE = re.compile(r'^([\w.$!()\/"\']+ )+[\w.$!()\/"\']+$|^[\w.$!()"\']{2,}$')
        # PATTERN_NETWORK = re.compile(r'^([\w.$!()\/"\']+ )+[\w.$!()\/"\']+$|^[\w.$!()"\']{3,}$')
        # PATTERN_DESCRIPTION = re.compile(r'\s*(?:[\w\.]\s*){10,}$')
        PATTERN_NAME = re.compile(r"^[a-z ,.'-]+$\"i")
        PATTERN_USERNAME = re.compile(r"^(?=.{8,25}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$")
        PATTERN_EMAIL = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        PATTERN_PWD = re.compile(r"^(.{0,7}|[^0-9]*|[^A-Z]*|[^a-z]*|[a-zA-Z0-9]*)$")

        # test_first_name = User.objects.cleanup_spaces(post_pattern1=post_data['first_name'])
        # test_last_name = User.objects.cleanup_spaces(post_pattern1=post_data['last_name'])
        # test_description = User.objects.cleanup_spaces(post_pattern2=post_data['description'])
        test_username = User.objects.cleanup_spaces(post_pattern3=post_data['username'])
        test_password = User.objects.cleanup_spaces(post_pattern1=post_data['password'])

        if user.filter(username=test_username).exists():
            errors['duplicate'] = "User with that title already exists."

        if not PATTERN_USERNAME.match(test_username):
            errors['username'] = "User name must be between 8-25 characters in length."

        if PATTERN_PWD.match(test_password):
            errors['password'] = "Password must be at least 8 characters in length, include one uppercase letter, one special character, and alphanumeric characters."



        # if not PATTERN_TITLE.match(test_title):
        #     errors['title'] = "Title should be at least 2 characters in length.\nAccepted characters: A-Z, 0-9, ., $, !, ( ), /, \", ', "

        # if not PATTERN_NETWORK.match(test_network):
        #     errors['network'] = "Network should be at least 3 characters in length."

        # if len(test_description) > 0 and not PATTERN_DESCRIPTION.match(test_description):
        #     errors['description'] = "Description should be at least 10 characters in length, with no extra spaces between words."
            
        # if (datetime.strptime(post_data['release_date'], '%Y-%m-%d') > datetime.today()):
        #     errors['release_date'] = "Release date cannot be a future date."

    def validate_login(self):
        errors = {}
        return errors



class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=254, unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()