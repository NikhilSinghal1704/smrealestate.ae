from django.forms import ValidationError
from django.utils import timezone
from django.db import models
from forex_python.converter import CurrencyRates
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator
from PIL import Image

def validate_image(image):
    # Validate if the uploaded file is an image
    try:
        img = Image.open(image)
        img.verify()  # Check if PIL can read and identify the image
    except Exception as e:
        raise ValidationError("Invalid image file: {}".format(e))



# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=155)
    email = models.CharField(max_length=155)
    # phone = models.IntegerField()
    phone = models.CharField(max_length=13,null=True , blank=True)

class AgentInquiry(models.Model):
    name = models.CharField(max_length=155)
    email = models.CharField(max_length=155)
    # phone = models.IntegerField()
    phone = models.CharField(max_length=13,null=True , blank=True)
    
class Agents(models.Model):
     
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
     
    TEAM = [
        ('Management', 'Management'),
        ('Agents', 'Agents'),
    ]


    photo = models.FileField(max_length=155)
    name = models.CharField(max_length=155)
    position = models.CharField(max_length=155)
    exprience = models.IntegerField()
    specialization = models.CharField(max_length=155)
    language = models.CharField(max_length=155)
    desc = models.TextField(max_length=9999)
    # phone = models.IntegerField()
    email = models.CharField(max_length=155)
    # whatsapp_number = models.IntegerField()
    team = models.CharField(choices=TEAM , default="Agents", max_length=155)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)
    phone = models.CharField(max_length=13,null=True , blank=True)
    whatsapp_number = models.CharField(max_length=13,null=True , blank=True)
    # indoor = models.CharField(choices=INDOOR , default="Kitchen", max_length=155)
    def __str__(self):
        return self.name




class Property(models.Model):

    Rent_Buy = [
        ('Rent', 'Rent'),
        ('Buy', 'Buy'),
        ('Sell', 'Sell')
    ]

    Type_Pro = [
        ('Apartments','Apartments'),
        ('villa', 'villa'),
        ('Penthouses', 'Penthouses'),
        ('Townhouses', 'Townhouses'),
        ('Duplexes', 'Duplexes'),
        ('Plots', 'Plots'),
        ('Offices', 'Offices')
    ]

    Bed =[
         (1, '1'),
        (2, '2 '),        
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6 '),
        (7, '7 '),
        (8, '8 '),
        (9, '9 '),
        (10, '10 ')
    ]


    
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
        
    INDOOR_CHOICES = [
        ('Balcony', 'Balcony'),
        ('Central-air-conditioning', 'Central-air-conditioning'),
        ('Built-in-wardrobes', 'Built-in-wardrobes'),
        ('Kitchen', 'Kitchen'),

    ]

    title = models.CharField(max_length=1555)
    
    property_location = models.CharField(max_length=155)
    property_type = models.CharField(max_length=155 , choices=Type_Pro)
    total_area = models.IntegerField()

    bedroom = models.IntegerField(choices=Bed)
    bathroom = models.IntegerField(default=0)
    rate = models.IntegerField()
    rent = models.CharField(max_length=155, choices=Rent_Buy , default="Buy")
    desc = models.TextField(max_length=15555 , default= "...")
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)
    assign_agents = models.ForeignKey(Agents, on_delete=models.CASCADE , default=True)
    indoor = models.CharField(  max_length=100, blank=True, null=True)
    outdoor = models.CharField(  max_length=100, blank=True, null=True)
    lot = models.CharField(  max_length=100, blank=True, null=True)
    #photo = models.FileField(max_length=100,null=True,blank=True, upload_to="documents/")
    # photo = models.CharField(max_length=155, blank=True, null=True)
    display_images = models.FileField(max_length=100,  blank=True, null=True , upload_to="display/", validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
        validate_image,  # Custom image validation function
    ])
    

    def square_meters(self):
        # 1 square foot is approximately equal to 0.092903 square meters
        return round(self.total_area * 0.092903, 2)

class PropertyImages(models.Model):
    photo = models.FileField(max_length=100,null=True,blank=True, upload_to="documents/" ,  validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
        validate_image,  # Custom image validation function
    ])
    property_img = models.ForeignKey(Property,related_name="property_image", on_delete=models.CASCADE,  null=True,blank=True)






# class PaymentPlan(models.Model):
#     pass

class PopularArea(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    images = models.FileField()
    name = models.CharField(max_length=155)
    price_from = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)


class OffPlaneProperties(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    images = models.FileField()
    name = models.CharField(max_length=155)
    locations = models.CharField(max_length=155)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)
    starting_price = models.CharField(max_length= 155 , default= 0 )
    starting_area = models.CharField(max_length=155, default= 0)
    handover = models.CharField(max_length=155 ,  blank=True, null=True)
    description = models.TextField(max_length=9999,  blank=True, null=True)
    location_description = models.CharField(max_length=9999 , blank=True , null= True)
    price_valid = models.CharField(max_length=155,blank=True , null= True )
    total_number_flat = models.CharField(max_length= 155, blank= True , null= True)
    status_of_project = models.CharField(max_length=155, blank= True , null= True)
    units = models.CharField(max_length= 155 , blank= True , null= True) 
    developer = models.CharField(max_length= 155 , blank= True , null= True) 
    payment_plan = models.CharField(max_length=155 , blank= True , null= True) 

    def __str__(self):
        return self.name


class FlatPlan(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    flat_type = models.CharField(max_length=155)
    total_area = models.IntegerField()
    starting_price_flat = models.IntegerField()
    flat_images_models = models.FileField(max_length = 155)
    category = models.CharField(max_length= 155)
    unit_type = models.CharField(max_length=155)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)
    off_plane_id = models.ForeignKey(OffPlaneProperties, on_delete=models.CASCADE , default=True)                

    def __str__(self):
        return self.flat_type + "->" + self.off_plane_id.name



class PaymentPlan(models.Model):
    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    persentage_installment = models.CharField(max_length=1555)
    payment_year = models.CharField(max_length=1555)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)
    off_plane_id = models.ForeignKey(OffPlaneProperties, on_delete=models.CASCADE , default=True)
    flat_plan_id = models.ForeignKey(FlatPlan, on_delete=models.CASCADE , default=True, null=True)
    



class ImagesModule(models.Model):
    MODULE_TYPE = [
        ('Property','Property'),
        ('OffPlan', 'OffPlan'),
        ('Blog', 'Blog'),

    ]
    photo  = models.FileField(max_length=155)
    module_type = models.CharField(max_length=155,choices=MODULE_TYPE )
    module_id = models.IntegerField()
    






class Blog(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )

    blog_name = models.CharField(max_length=155)
    photo = models.FileField(max_length=155)
    desc = models.TextField(max_length=9999)
    date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)



class News(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )

    news_name = models.CharField(max_length=155)
    photo = models.FileField(max_length=155)
    desc = models.TextField(max_length=9999)
    date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)


# class Agents(models.Model):
     
#     STATUS_CHOICES = (
#         (1, 'Active'),
#         (0, 'Inactive'),
#     )
     
#     photo = models.FileField(max_length=155)
#     name = models.CharField(max_length=155)
#     position = models.CharField(max_length=155)
#     exprience = models.IntegerField(max_length=100)
#     specialization = models.CharField(max_length=155)
#     language = models.CharField(max_length=155)
#     desc = models.TextField(max_length=9999)
#     phone = models.IntegerField(max_length=18)
#     email = models.CharField(max_length=155)
#     whatsapp_number = models.IntegerField(max_length=118)
#     status = models.IntegerField(choices=STATUS_CHOICES , default=1)


class Review(models.Model):

    

    reviewer_name = models.CharField(max_length=100)
    photo = models.FileField(max_length=155, default= False, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    reviewer_email = models.EmailField()
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reviewer_name
    
    def average_rating(self):
        from django.db.models import Avg, ExpressionWrapper, F, fields
        total_avg = Review.objects.filter().aggregate(Avg('rating'))['rating__avg']
        round_of_avg = round(total_avg,1)
        return round_of_avg
    
    def get_star_icons(self):
        filled_stars = '<span class="fas fa-star"></span>' * self.rating
        empty_stars = '<span class="far fa-star"></span>' * (5 - self.rating)
        return filled_stars + empty_stars
    



class Partners(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )
    
    partners_name = models.CharField(max_length=155)
    partners_images = models.FileField(max_length=155)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)

    def __str__(self):
        return self.partners_name
    
class OfficeImages(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )

    office_images_name = models.CharField(max_length=155)
    office_images = models.FileField(max_length=155)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)

    def __str__(self):
        return self.office_images_name
   
class ProjectText(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )

    our_project_text = models.TextField(max_length=1555)
    our_project_images = models.FileField(max_length=155)
    heading = models.CharField(max_length=155,default="NEW HOME FOR GENRATIONS") 
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)


class CMS(models.Model):

    STATUS_CHOICES = (
        (1, 'Active'),
        (0, 'Inactive'),
    )

    cms_page_name = models.CharField(max_length=155)
    description =  models.TextField(max_length=1555)
    status = models.IntegerField(choices=STATUS_CHOICES , default=1)

    




   


    
class Comprassion(models.Model):
    product_id = models.IntegerField()




class BookAppointment(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    appointment_type = models.CharField(max_length=20)
    appointment_date = models.DateTimeField(default= timezone.now )