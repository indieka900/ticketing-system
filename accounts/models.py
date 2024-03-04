from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'Administrator')
        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractBaseUser, PermissionsMixin):
    
    Role_choices = (
        ("Administrator", "Administrator"),
        ("Student", "Student"),
        ("Chairperson", "Chairperson")
    )
    
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    email = models.EmailField(unique=True)
    profile_pic = models.CharField(max_length = 300,default='https://d326fntlu7tb1e.cloudfront.net/uploads/bdec9d7d-0544-4fc4-823d-3b898f6dbbbf-vinci_03.jpeg')
    full_name = models.CharField(max_length=60,default='')
    role = models.CharField(max_length=25, choices=Role_choices, default="Student")
    phone = models.PositiveIntegerField( blank=True, null=True,)
    verification = models.BooleanField(default=False)
    reg_no = models.CharField(max_length = 25)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone_verification = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    objects = CustomUserManager()
    
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def get_avatar_name(self):
        if self.image:
            return self.image.name
        else:
            return None
        
    def get_short_name(self):
        if (len(self.full_name) == 0):
            return self.email.split('@')[0].capitalize()
        
        else:
            return self.full_name.split(' ')[0]
        
    # def save(self, *args, **kwargs):
    #     if not self._id:
    #         self._id = str(ObjectId())
    #     if not self.verification_code:
    #         self.verification_code = generate_verification_code()
    #     super().save(*args, **kwargs)

# Create your models here.
