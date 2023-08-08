from django.db import models
from django.contrib.auth.hashers import make_password
# User Registration Section

role = (
    ("user1", "Staff"),
    ("user2", "User"),
   
)
under = (
    ("Home Appliance", "Home Appliance"),
    ("Electronics", "Electronics"),
    ("Furniture", "Furniture"),
)
class User_Registration(models.Model):
    
    name = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    nickname = models.CharField(max_length=255,blank=True,null=True)
    gender = models.CharField(max_length=10,blank=True,null=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    role = models.CharField(max_length=255,blank=True,null=True,choices = role)
    username = models.CharField(max_length=255,blank=True,null=True)
    password = models.CharField(max_length=255,blank=True,null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    status =models.CharField(max_length = 255,blank=True,null=True)
    def _str_(self):
        return self.nickname
    
    def get_email_field_name(self):
        return 'email'

# Create Artist Profile
class Profile_User(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    firstname = models.CharField(max_length=255,blank=True,null=True)
    lastname = models.CharField(max_length=255,blank=True,null=True)
    phonenumber = models.CharField(max_length=20)
    secondnumber = models.CharField(max_length=20)
    email = models.EmailField(blank=True,null=True)
    gender = models.CharField(max_length=255,blank=True,null=True)
    date_of_birth = models.DateField(null=True)
    address =  models.TextField(blank=True,null=True)
    pro_pic = models.ImageField(upload_to='images/', default='static/images/logo/icon.png')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class bannerads(models.Model):
    banner_image1=models.FileField(upload_to='images/banner',blank=True,null=True)
    banner_image2=models.FileField(upload_to='images/banner',blank=True,null=True)
    banner_image3=models.FileField(upload_to='images/banner',blank=True,null=True)
    banner_image4=models.FileField(upload_to='images/banner',blank=True,null=True)
    banner_image5=models.FileField(upload_to='images/banner',blank=True,null=True)
    banner_title1 = models.CharField(max_length=255,blank=True,null=True)
    banner_title2 = models.CharField(max_length=255,blank=True,null=True)
    banner_title3 = models.CharField(max_length=255,blank=True,null=True)
    banner_title4 = models.CharField(max_length=255,blank=True,null=True)
    banner_title5 = models.CharField(max_length=255,blank=True,null=True)

class category(models.Model):
    category_name=  models.CharField(max_length=255,blank=True,null=True)
    image = models.FileField(upload_to='images/category-banner', default='static/images/logo/noimage.jpg')
    def _str_(self):
        return self.category_name

class item(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    category= models.ForeignKey(category, on_delete=models.SET_NULL, null=True, blank=True,default=None)
    name = models.CharField(max_length=255,blank=True,null=True)
    title_description = models.CharField(max_length=100,blank=True,null=True)
    description = models.CharField(max_length=255,blank=True,null=True)
    price = models.FloatField(default=0)
    offer_price=  models.FloatField(default=0)
    buying_count = models.IntegerField(default=0)
    offer = models.IntegerField(default=0)
    image = models.FileField(upload_to='images/items', default='static/images/logo/noimage.jpg')
    under_category=models.CharField(max_length=255,blank=True,null=True,choices = under)

class cart(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)

class checkout(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(item, on_delete=models.SET_NULL, null=True, blank=True)
    qty=models.IntegerField(null=True, blank=True)
    item_total=models.FloatField(null=True, blank=True)
    item_price=models.FloatField(null=True, blank=True)
    item_name = models.CharField(max_length=255,blank=True,null=True)
    date=models.DateTimeField(null=True, blank=True)


class offer_zone(models.Model):
    user = models.ForeignKey(User_Registration, on_delete=models.SET_NULL, null=True, blank=True)
    image =  models.FileField(upload_to='images/items', default='static/images/logo/noimage.jpg')
    title = models.CharField(max_length=255,blank=True,null=True)
    description = models.TextField(max_length=200,blank=True,null=True)
    price=  models.FloatField(default=0)
    offer_price=  models.FloatField(default=0)
    offer= models.IntegerField(default=0)

