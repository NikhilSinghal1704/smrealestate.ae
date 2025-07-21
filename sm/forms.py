from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class PropertiesForm(forms.ModelForm):
    INDOOR_CHOICES = (
        ('Balcony', 'Balcony'),
        ('Central-air-conditioning', 'Central-air-conditioning'),
        ('Built-in-wardrobes', 'Built-in-wardrobes'),
        ('Kitchen', 'Kitchen'),
        )
    
    OUTDOOR_CHOICES = (
        ('Sauna', 'Sauna'),
        ('Gymnasium', 'Gymnasium'),
        ('Restaurants', 'Restaurants'),
        ('Covered-parking', 'Covered-parking'),
        ('Childrens-play-area', 'Childrens-play-area'),
        ('Communal-gardens', 'Communal-gardens'),
        
       )
    LOT_CHOICES = (
        ('Shared-swimming-pool', 'Shared-swimming-pool'),
        ('View-of-Water', 'View-of-Water'),
        ('View-of-Landmark', 'View-of-Landmark'),
        ('Public-parking', 'Public-parking'),
        ('Security', 'Security'),
        ('Concierge-Service', 'Concierge-Service'),
        ('Shopping-mall', 'Shopping-mall'),
        ('Public-park', 'Public-park'))
    
    indoor = forms.MultipleChoiceField(choices=INDOOR_CHOICES,
        widget=forms.CheckboxSelectMultiple, 
        required=False  
    )
    outdoor = forms.MultipleChoiceField(choices=OUTDOOR_CHOICES,
    widget=forms.CheckboxSelectMultiple, 
    required=False  
    )
    lot = forms.MultipleChoiceField(choices=LOT_CHOICES,
    widget=forms.CheckboxSelectMultiple, 
    required=False  
    )
    class Meta:
        model = Property
        fields = ['title', 'property_location', 'total_area', 'property_type',
                   'rate', 'bedroom', 'bathroom', 'rent', 'status', 'assign_agents',
                     'desc' , 'indoor', 'outdoor', 'lot', 'display_images' ]


class OffPlanePropertiesForm(forms.ModelForm):

    class Meta:
        model = OffPlaneProperties
        fields = "__all__"

class PopularAreaForm(forms.ModelForm):
    class Meta:
        model = PopularArea
        fields = "__all__"


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"


class NewsForm(forms.ModelForm):
    class Meta:
        model =News
        fields = "__all__"


class AgentsForm(forms.ModelForm):
    class Meta:
        model = Agents
        fields = "__all__"

class ReviewForm(forms.ModelForm):

    # rating = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'type': 'number', 'min': '0', 'max': '5'}),
    #     label='Star Rating')

    rating = forms.ChoiceField(
        choices=[('1', 'Poor'), ('2', 'Fair'), ('3', 'Good'), ('4', 'Excellent'), ('5', 'WOW!!!')],
        widget=forms.RadioSelect(attrs={'class': 'star-list'})),

    class Meta:
        model = Review
        fields = ['reviewer_name', 'reviewer_email', 'rating', 'comment', 'photo']





class PartnersForm(forms.ModelForm):
    class Meta:
        model = Partners
        fields = "__all__"


class OfficeImagesForm(forms.ModelForm):
    class Meta:
        model = OfficeImages
        fields = "__all__"


class ProjectTextForm(forms.ModelForm):
    class Meta:
        model = ProjectText
        fields = "__all__"


class CMSForm(forms.ModelForm):
    class Meta:
        model = CMS
        fields = "__all__"




class PropertySearchForm(forms.Form):
    bedrooms = forms.IntegerField(required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    price_range = forms.IntegerField(required=False)
    location = forms.CharField(required=False)
    property_type = forms.CharField(required=False)
    rent = forms.CharField(required = False)


class AgentSearchForm(forms.Form):
    sp = forms.CharField(required=False)
    lan = forms.CharField(required = False)







class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = BookAppointment
        fields = "__all__"


class AgentInquiryForm(forms.ModelForm):
    class Meta:
        model = AgentInquiry
        fields = "__all__"


class FlatPlanForm(forms.ModelForm):
    class Meta:
        model = FlatPlan
        fields ="__all__"

class PaymentPlanForm(forms.ModelForm):
    class Meta:
        model = PaymentPlan
        fields ="__all__"




class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



class ImagesForm(forms.ModelForm):
    class Meta:
        model = ImagesModule
        fields ="__all__"
        
        

