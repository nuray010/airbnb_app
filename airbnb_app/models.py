from random import choices
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    RoleChoices = (
    ('guest','guest'),
    ('host','host'),
    )
    user_role = models.CharField(max_length=30,choices=RoleChoices, default='guest')
    phone_field = PhoneNumberField(null=True,blank=True)
    avatar = models.ImageField(upload_to='user_photo', null=True,blank=True)

    def __str__(self):
      return f'{self.username}'


class City(models.Model):
    city_name = models.CharField(max_length=30)
    city_img = models.ImageField(upload_to='city_photo', null=True,blank=True)

    def __str__(self):
        return f'{self.city_name}'

class Rules(models.Model):
    rules_img = models.ImageField(upload_to='rules_photo', null=True,blank=True)
    rules_name = models.CharField(max_length=80)

    def __str__(self):
        return self.rules_name

class Property(models.Model):
    title = models.CharField(max_length=100)
    description  = models.TextField()
    price = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    PropertyChoices = (
    ('apartment','apartment'),
    ('house','house'),
    ('studio','studio'),
    ('penthouse','penthouse'),
    ('villa','villa'),
    )
    property_type = models.CharField(max_length=30,choices=PropertyChoices, default='apartment')
    rules = models.ManyToManyField(Rules)
    max_guests = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    def __str__(self):
        return f'{self.title}'

    def get_avg_rating(self):
        reviews = self.review_property.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(), 1)
        return 0

    def get_count_person(self):
        return self.review_property.count()

    def get_price_property(self):
        return self.price * 2

class PropertyImg(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    property_img = models.ImageField(upload_to='property_photo')

    def __str__(self):
        return f'{self.property},{self.property.img}'

class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    StatusChoices = (
    ('pending','pending'),
    ('approved','approved'),
    ('rejected','rejected'),
    ('cancelled','cancelled'),
    )
    status = models.CharField(max_length=30,choices=StatusChoices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property},{self.guest}'




class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.property},{self.guest}'





