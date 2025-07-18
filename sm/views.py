import datetime
import re
from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView , FormView
from django.views.generic import DetailView
# Create your views here.
from django.views import View
from sm.forms import *
from django.db.models import Avg
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
import requests
from django.views.decorators.csrf import ensure_csrf_cookie
from sm.currency_conversion import RealTimeCurrencyConverter
from datetime import date, timedelta
import ast , json
from django.contrib import messages










class IndexView(View):
    def get(self, request):
        about  =CMS.objects.all()
        agents = Agents.objects.all()
        properties = Property.objects.all().order_by('-id')
        rental = Property.objects.filter(rent = "Rent").order_by('-id')
        secondary = Property.objects.filter(Q(rent='Sell') | Q(rent='Buy')).order_by('-id')
        blogs = Blog.objects.all()
        review = Review.objects.all()
        partner = Partners.objects.all()   #.order_by('-id')
        office_images = OfficeImages.objects.all()  #.order_by('-id')
        banner = ProjectText.objects.all()   #.order_by('-id')
        off_plane = OffPlaneProperties.objects.all().order_by('-id')   #.order_by('-id')
        popular_area = PopularArea.objects.filter(status = 1).order_by('-id')
        properties_images = PropertyImages.objects.all()
        
        # lan = request.GET.get('language')
        # sp = request.GET.get('special')
        # if lan != None and sp != None:
        #     agents = Agents.objects.filter(specialization= sp,language=lan)


        context = {'agents':agents, 'properties':properties, 'blogs': blogs, 'review':review,
                    'partners': partner, 'office_images':office_images, 'banner':banner,
                      'about': about, 'off_plane':off_plane, 'popular_area':popular_area,
                      'rental':rental , 'secondary': secondary , 'properties_images':properties_images }
        return render(request, 'index.html', context)
    

    


##Ranjeet
def agentContactFormView(request):
    if request.method=='POST':

        print("AgentContact form called!!")
        template_name = 'index.html'
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect('/')
        else:
            form = ContactForm()
        return render(request, template_name , {'form':form})
    
# Nikhil
def property_search(request, property_type=None):
    location = request.GET.get('location')
    budget_range = request.GET.get('budget_range')
    selected_type = request.GET.get('selected_type')  # 'rent', 'sell', 'offices', etc.

    # Start with all active properties
    qs = Property.objects.filter(status=1)

    # Filter by location (case-insensitive contains)
    if location:
        qs = qs.filter(property_location__icontains=location)

    # Filter by budget range: "<low>-<high>"
    if budget_range:
        low, high = budget_range.split('-', 1)
        if low:
            qs = qs.filter(rate__gte=int(low))
        if high != 'None':
            qs = qs.filter(rate__lte=int(high))

    # Filter by tab type
    if selected_type == 'rent':
        qs = qs.filter(rent='Rent')
    elif selected_type in ('sell'):

        qs = Property.objects.filter(
            Q(rent='Sell') | Q(rent='Buy')
        )

    elif selected_type == 'offices':
        # For offices, ignore Rent/Buy; filter by property_type
        qs = qs.filter(property_type='Offices')
    

    # Convert to paginated queryset (if needed)
    # Example:
    # from django.core.paginator import Paginator
    # page = request.GET.get('page', 1)
    # paginator = Paginator(qs, 9)
    # properties = paginator.get_page(page)

    # For now, just return the filtered QuerySet as a context dict
    context = {
        'properties': qs,  
        'location': location if location else 'Dubai',
        'budget_range': budget_range,
        'selected_type': selected_type,
    }

    return render(request, 'property_search.html', context)
    
class AboutView(View):
    def get(self,request):
        about  =CMS.objects.all()
        agents = Agents.objects.all().order_by('-id')
        properties = Property.objects.all().order_by('-id')
        review = Review.objects.all().order_by('-id')
        context ={'agents':agents , 'properties':properties , 'review':review , 'about': about}
        return render(request, 'about.html',  context)
        
        
class CommingSoon(View):
    def get(self, request):
        return render(request, 'coming_soon.html')
        
    
class OffPlaneView(View):
    def get(self, request):
        properties = OffPlaneProperties.objects.filter(status = 1 )
        paginator = Paginator(properties,4)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        context ={'properties':properties }
        return render(request, 'off_plane.html',  context)
    
def Locationvia(request, property_location):
    off_plan = OffPlaneProperties.objects.filter(status = 1 , locations__icontains = property_location )
    properties = Property.objects.filter(status = 1 , property_location__icontains = property_location)
    paginator = Paginator(properties,4)
    page = request.GET.get('page')
    properties= paginator.get_page(page)
    context = {'properties':properties, 'property_location':property_location , 'off_plan': off_plan, 
               'lP': len(properties), 'lO': len(off_plan) , 'lA': len(properties) }
    return render(request, 'location_via.html' ,context ) 


class offplaneWebDetailView(DetailView):     
    model = OffPlaneProperties 
    template_name = 'off_plan_web_details.html' 
    context_object_name = 'properties' 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        pk = self.kwargs.get('pk')   
        images = ImagesModule.objects.filter(module_id = pk , module_type = "OffPlan") 
        flatplan = FlatPlan.objects.filter(off_plane_id = pk) 
        paymentplan = PaymentPlan.objects.filter(off_plane_id = pk) 
        context['paymentplan'] = paymentplan  
        context['flatplan'] = flatplan  
        context['images'] = images  
        return context



class OffPlanWebDetailView(View):
    def get(self, request):
        return render(request, 'offplanedetails.html')


class PopularAreaView(View):
    def get(self, request):
        properties = PopularArea.objects.filter(status = 1 )
        paginator = Paginator(properties,4)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        context ={'properties':properties }
        return render(request, 'popular_area.html',  context)
    
    
    
class PartnerView(View):
    def get(self,request):
        partners  =Partners.objects.filter(status = 1 )
        return render(request, 'allpartner.html', {'partners': partners } )    


class SerachFilterView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1)
        form = PropertySearchForm(request.GET)

        if form.is_valid():
            # import pdb; pdb.set_trace()
            bedrooms = form.cleaned_data.get("bedrooms")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")
            price_range = form.cleaned_data.get("price_range",0)
            location = form.cleaned_data.get("location")
            property_type = form.cleaned_data.get("property_type")
            rent  =  form.cleaned_data.get("rent")
            #import pdb; pdb.set_trace()

            if bedrooms:
                properties = properties.filter(Q(bedroom__gte=bedrooms))
            if price_range == 10-100:
                properties = properties.filter(Q(rate__gte=10) & Q(rate__lte=100))      

            if min_price:
                properties = properties.filter(Q(rate__gte=min_price))

            if max_price:
                properties = properties.filter(Q(rate__lte=max_price))

            if location:
                properties = properties.filter(Q(property_location__icontains=location))

            if property_type:
                properties = properties.filter(Q(property_type__iexact=property_type))

            if rent:
                properties = properties.filter(Q(rent__icontains = rent))
        
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        context = {              
                'properties': properties,                
                'form': form,
                }

        return render(request, "properties.html",context)

    
class PropertiesView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1)
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)

        context = {  

                'properties': properties,
                'of': 'of'
                }
       

        return render(request, "properties.html",context  )
    
class PanthouseView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,property_type='Penthouses')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html', { 'properties':properties})

class TownhousesView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,property_type='Townhouses')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html',  {'properties':properties})
    
class VillaView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,property_type='villa')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html',  { 'properties':properties})

class ApartmentsView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,property_type='Apartments')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html',  { 'properties':properties})

class RentView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,rent='Rent')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html', {'properties': properties})
    
class BuyView(View):
    def get(self, request):
        properties = Property.objects.filter(status = 1 ,rent='Buy')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html', {'properties': properties})

class SellView(View):
    def get(self, request):
        properties = Property.objects.filter( status = 1 , rent='Sell')
        paginator = Paginator(properties,3)
        page = request.GET.get('page')
        properties= paginator.get_page(page)
        return render(request, 'properties.html', {'properties': properties})   


def currency_convert(request,pk):
   
    property = Property.objects.get(pk = pk)
    rate = property.rate
    target_currency = request.POST.get('currency')
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = RealTimeCurrencyConverter(url)
    

    convet_rate = converter.convert('AED',target_currency,rate)
    # convet_rate = convert_currency(rate,target_currency)
    data = {'convet_rate':convet_rate , 'target_currency':target_currency, 'rate':rate }
    return JsonResponse(data)
    


 


class PropertiesWebDetailView(DetailView ):
    model = Property
    template_name = 'properties_details.html'
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve data from ModelB related to this ModelA instance
        pk = self.kwargs.get('pk')
        images = ImagesModule.objects.filter(module_id = pk , module_type = "Property")
        properties_images = PropertyImages.objects.filter(property_img = pk )
        review_data = Review.objects.all()
        properties_data = Property.objects.all()
        
        indoor_value = self.object.indoor
        outdoor_value = self.object.outdoor
        lot_value = self.object.lot
        # list_indoor = re.findall(r'"\s*([^"]*?)\s*"', indoor_value)
        # list_outdoor =re.findall(r'"\s*([^"]*?)\s*"', outdoor_value)
        # list_lot = re.findall(r'"\s*([^"]*?)\s*"', lot_value)
        
        list_indoor = ast.literal_eval(indoor_value)

        list_outdoor = ast.literal_eval(outdoor_value)
        list_lot = ast.literal_eval(lot_value)
        
 
        # list_lot = ast.literal_eval(photo_value)
        
        
        
        # Get today's date
        today = date.today()
        # Calculate the start date of the current week (Sunday)
        start_of_week = today - timedelta(days=today.weekday())
        # Create a list of date and day name pairs for the current week
        current_week_dates = []
        for i in range(7):
            current_date = start_of_week + timedelta(days=i)
            day_name = current_date.strftime("%a")
            date_str = current_date.strftime("%Y-%m-%d")
            date_dm = current_date.strftime('%d %b')
            current_week_dates.append((day_name, date_str, date_dm))
        
        context['properties_data'] = properties_data
        context['review_data'] = review_data
        context['current_week_dates'] = current_week_dates
        context['list_indoor'] = list_indoor
        context['list_outdoor'] = list_outdoor
        context['list_lot'] = list_lot
        context['properties_images'] = properties_images
        # context['list_photo'] = list_from_string
        
        return context
    

    
    
    




    

class BlogView(View):
    def get(self,request):
        blog_posts = Blog.objects.filter(status = 1)
        paginator = Paginator(blog_posts,3)
        page = request.GET.get('page')
        blog_posts= paginator.get_page(page)
        context = {'blog_posts':blog_posts }
        return render(request, 'blog.html', context)


class BlogWebDetailView(DetailView):
    model = Blog
    template_name ='blog_details.html'
    context_object_name = 'blogs'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        images = ImagesModule.objects.filter(module_id = pk , module_type = "Blog")
        context['images'] = images
        return context









class OurTeamView(View):
    def get(self, request):
        management =  Agents.objects.filter(status = 1 , team='Management')
        agents = Agents.objects.filter(status = 1 , team= "Agents")
        paginator = Paginator(agents,4)
        page = request.GET.get('page')
        agents= paginator.get_page(page)

        # lan = request.GET.get('language')
        # sp = request.GET.get('special')
        
        
        # if lan != None:
        #     agents = Agents.objects.filter(language=lan)
        # if sp != None:
        #     agents = Agents.objects.filter(specialization= sp)
            
        context = { 'agents': agents, 'of':'of' , 'management':management }
        return render(request, 'agents.html', context)

class AgentsView(View):
    def get(self, request):
        agents = Agents.objects.filter(status = 1 , team= "Agents")
        paginator = Paginator(agents,4)
        page = request.GET.get('page')
        agents= paginator.get_page(page)

        # lan = request.GET.get('language')
        # sp = request.GET.get('special')
        
        
        # if lan != None:
        #     agents = Agents.objects.filter(language=lan)
        # if sp != None:
        #     agents = Agents.objects.filter(specialization= sp)
            
        context = { 'agents': agents, 'of':'of' }
        return render(request, 'agent_listing.html', context)


class AgentsSearchView(View):
    def get(self, request):
        agents = Agents.objects.filter(status = 1 , team= "Agents")
        lan = request.GET.get('language')
        sp = request.GET.get('special')
        
        
        if lan:
            agents = agents.filter(Q(language=lan))
        if sp:
            agents = agents.filter(Q(specialization= sp))
        paginator = Paginator(agents,4)
        page = request.GET.get('page')
        agents= paginator.get_page(page)    
        context = { 'agents': agents, 'lan':lan , 'sp':sp   }
        return render(request, 'agent_listing.html', context)

        
class AgentsWebDetailView(DetailView):
    model = Agents
    template_name = 'agents_details.html'
    context_object_name = 'agents'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve data from ModelB related to this ModelA instance
        review_data = Review.objects.all()
        agent_data = Agents.objects.all()
        context['agent_data'] = agent_data
        context['review_data'] = review_data
        return context
    
    





class NewsView(View):
    def get(self, request):
        news = News.objects.all()
        paginator = Paginator(news,3)
        page = request.GET.get('page')
        news= paginator.get_page(page)
        context = {'news':news}
        return render(request, 'news.html', context)

class NewsWebDetailView(DetailView):
    model= News
    template_name ='news_details.html'
    context_objet_name= 'news'


class ContactView(View):
    template_name = 'contact.html'
    def get(self, request):
        form = ContactForm()
        context = {'form':form}
        return render(request , self.template_name, context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Contact submitted successfully!'})
        else:
            errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)
    

class BookAppointmentView(View):
    
    def get(self, request):
        form = BookAppointmentForm()
        context = {'form':form}
        return render(request , 'properties_details.html', context)
    
    def post(self, request):
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Appointment  submitted successfully!'})
        else:
            errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)


class AgentsInquiryView(View):
    def get(self, request):
        form = AgentInquiryForm()
        context = {'form':form}
        return render(request , 'agent_contact.html', context)
    
    def post(self, request):
        form = AgentInquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Agent Contact  submitted successfully!'})
        else:
            errors = form.errors.as_json()
        return JsonResponse({'errors': errors}, status=400)





class ReviewView(View):
    def get(self, request):
        review = Review.objects.all()
        paginator = Paginator(review,6)
        page = request.GET.get('page')
        review= paginator.get_page(page)
        return render(request, 'reviews_list.html', {'review':review})



class AddReviewView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, 'add_review.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect('/review/')
        else:
            form = ReviewForm()
        return render(request, 'add_review.html', {'form':form})
    


class ComprassionView(View):
    def get(self, request):
        comp_items = request.session.get('comp_items', [])  
         
        request.session['comp_items'] = comp_items
        if len(comp_items) != 0: 
            comp = Property.objects.filter(id__in=comp_items)
            context ={ 'comp':comp  , 'comp_items': comp_items}
            return render(request, 'comprassion.html',  context)
        else:
            return render(request, 'comprassion_blank.html' )
        # comp = Property.objects.filter(id__in=comp_items)
        # context ={ 'comp':comp  , 'comp_items': comp_items}
        
        # return render(request, 'comprassion.html',  context)
        
        



class FavoriteView(View):
    def get(self, request):
        favorite_items = request.session.get('favorite_items', [])  
         
        request.session['favorite_items'] = favorite_items  

        if len(favorite_items) != 0:
            favorite = Property.objects.filter(id__in=favorite_items)
            context ={ 'favorite':favorite}
        
            return render(request, 'favorite.html',  context)
        else:
            return render(request, 'favorite_blank.html' )
        




    
    



from django.http import JsonResponse
# add to favorite 
# class add_to_favoritesView(View):
    
#     def get(self, request, pk):
#         import pdb; pdb.set_trace()
#         favorite_items = request.session.get('favorite_items', [])  # Retrieve the current list of favorite items
#         if pk not in favorite_items:
#             favorite_items.append(pk)  # Add the item to favorites
#         else:
#             favorite_items.remove(pk)  # Remove the item from favorites if already added
#         request.session['favorite_items'] = favorite_items  # Update the session variable

#         favorite = Property.objects.filter(id__in=favorite_items)
#         context ={ 'favorite':favorite}
#         return render(request, 'favorite.html',  context)
    

# # add to favorite 
# class add_to_comparissionView(View):
    
#     def get(self, request, pk):
#         comp_items = request.session.get('comp_items', [])  # Retrieve the current list of favorite items
#         if pk not in comp_items:
#             comp_items.append(pk)  # Add the item to favorites
#         else:
#             comp_items.remove(pk)  # Remove the item from favorites if already added
#         request.session['comp_items'] = comp_items  # Update the session variable

#         comp = Property.objects.filter(id__in=comp_items)
#         context ={ 'comp':comp}
#         return render(request, 'comprassion.html',  context)
        
        

def add_to_favorites(request,pk):
    #import pdb;pdb.set_trace()
    favorite_items = request.session.get('favorite_items', [])
    if pk not in favorite_items:
            favorite_items.append(pk)  # Add the item to favorites
    else:
        favorite_items.remove(pk)  # Remove the item from favorites if already added
    request.session['favorite_items'] = favorite_items  # Update the session variable

    

    favorite = Property.objects.filter(id__in=favorite_items)
    context ={ 'favorite':favorite}
    return render(request, 'favorite.html',  context)




def add_to_comparission(request, pk ):
    comp_items = request.session.get('comp_items', [])  # Retrieve the current list of favorite items
    if pk not in comp_items:
        comp_items.append(pk)  # Add the item to favorites
    else:
        comp_items.remove(pk)  # Remove the item from favorites if already added
    request.session['comp_items'] = comp_items  # Update the session variable

    comp = Property.objects.filter(id__in=comp_items)
    context ={ 'comp':comp}
    return render(request, 'comprassion.html',  context)



from django.http import HttpResponse
def clear_favorites(request):
    favorite_items = request.session.get('favorite_items', [])
    if 'favorite_items' in request.session:
        del request.session['favorite_items']  # Remove the 'favorites' key from the session
    return render(request, 'favorite_blank.html')


def clear_comparission(request):
    comp_items = request.session.get('comp_items', [])
    if 'comp_items' in request.session:
        del request.session['comp_items']  # Remove the 'comp' key from the session
    return render(request, 'comprassion_blank.html')


class TermConditionView(View):
    def get(self, request):
        return render(request, 'terms_condition.html' )
    

class privacypolicyView(View):
    def get(self, request):
        return render(request, 'privacy_policy.html' )
    





       
  



        













from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
@method_decorator(login_required, name='dispatch')
class AdminIndexView(View):
    def get(self, request):
        agents = Agents.objects.all()
        property =Property.objects.all()
        review = Review.objects.all()

        context = {'agents': agents, 'property':property, 'review':review}
        return render(request, 'dashboard/index.html', context)
    
@method_decorator(login_required, name='dispatch')   
class AddAgentsView(View):
    def get(self, request):
        form = AgentsForm()
        return render(request, 'dashboard/add_agents.html', {'form':form})

    def post(self,request):
        form = AgentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_agents/')
        else:
            form = AgentsForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_agents.html',{'form':form})
    

@method_decorator(login_required, name='dispatch')
class AgentsListView(View):
    def get(self, request):
        agents = Agents.objects.all()
        context = {'agents' : agents}
        return render(request, 'dashboard/agents_list.html', context)
    

@method_decorator(login_required, name='dispatch')
class AddPropertiesView(View):
    def get(self, request):
        form = PropertiesForm() 
        
        agents = Agents.objects.all()
        return render(request, 'dashboard/add_properties.html' ,{'form':form, 'agents':agents})

    def post(self, request):
        agents = Agents.objects.all()
        form = PropertiesForm(request.POST, request.FILES)
        title = request.POST['title']
        property_location = request.POST['property_location']
        property_type = request.POST['property_type']
        total_area = request.POST['total_area']
        bedroom = request.POST['bedroom']
        bathroom = request.POST['bathroom']
        rate = request.POST['rate']
        rent = request.POST['rent']
        desc = request.POST['desc']
        status = request.POST['status']
        assign_agents = request.POST['assign_agents']
        assign_agents_instance = Agents.objects.get(pk=assign_agents)
        indoor = request.POST.getlist('indoor')
        outdoor = request.POST.getlist('outdoor')
        lot = request.POST.getlist('lot')
        display_images = request.FILES.get('display_images')
        
        images_list = request.FILES.getlist('photo')
        
       
        
        
        if form.is_valid():
            property = Property.objects.create(property_location= property_location,title = title,property_type=property_type,
                                 total_area=total_area, bedroom= bedroom, bathroom= bathroom, rate= rate, rent= rent,
                                    desc=desc, status= status, assign_agents= assign_agents_instance, indoor= indoor,
                                     outdoor= outdoor, lot= lot, display_images= display_images )
            for f in images_list:
                PropertyImages.objects.create(photo=f,property_img=property)
            
            messages.success(request, 'Form submitted successfully!')
            return  HttpResponseRedirect('/dashboard/add_properties/')
        else:
            form = PropertiesForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_properties.html' , {'form':form , 'agents':agents, })
    

@method_decorator(login_required, name='dispatch')
class PropertiesListView(View):
    def get(self, request):
        properties = Property.objects.all()
        context = { 'properties': properties}
        return render(request, 'dashboard/properties_list.html' , context)


@method_decorator(login_required, name='dispatch')
class AddOffPlanePropertiesView(View):
    def get(self, request):
        form = OffPlanePropertiesForm() 
        return render(request, 'dashboard/add_off_plane.html', {'form': form})

    def post(self, request):
        form = OffPlanePropertiesForm(request.POST, request.FILES)

        images_list = request.FILES.getlist('photo')  # multiple images from HTML field

        if form.is_valid():
            property_obj = form.save()

            # Save related property images
            for f in images_list:
                OffPlanePropertyImages.objects.create(photo=f, property_img=property_obj)

            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_offplane_properties/')
        else:
            messages.warning(request, 'Form not submitted, Please check fields!')

        return render(request, 'dashboard/add_off_plane.html', {'form': form})



@method_decorator(login_required, name='dispatch')
class AddOffPlanePropertiesListView(View):
    def get(self, request):
        properties = OffPlaneProperties.objects.all()
        context = { 'properties': properties}
        return render(request, 'dashboard/off_plane_list.html' , context)


@method_decorator(login_required, name='dispatch')
class AddPopularAreaView(View):
    def get(self, request):
        form = PopularAreaForm() 
        return render(request, 'dashboard/add_popular_area.html' ,{'form':form})

    def post(self, request):
        form = PopularAreaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return  HttpResponseRedirect('/dashboard/add_popular_area/')
        else:
            form = PropertiesForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_popular_area.html' , {'form':form })
    


@method_decorator(login_required, name='dispatch')
class PopularAreaListView(View):
    def get(self, request):
        properties = PopularArea.objects.all()
        context = { 'properties': properties}
        return render(request, 'dashboard/popular_area_list.html' , context)


@method_decorator(login_required, name='dispatch')
class AddFlatView(View):
    def get(self, request):
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        form = FlatPlanForm() 
        return render(request, 'dashboard/add_flat.html' ,{'form':form , 'off_plan':off_plan})

    def post(self, request):
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        form = FlatPlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return  HttpResponseRedirect('/dashboard/add_flat/')
        else:
            form = FlatPlanForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_flat.html' , {'form':form, 'off_plan':off_plan })

@method_decorator(login_required, name='dispatch')
class FlatListView(View):
    def get(self, request):
        flat = FlatPlan.objects.filter(status = 1)
        context = { 'flat': flat}
        return render(request, 'dashboard/flat_list.html' , context)


@method_decorator(login_required, name='dispatch')
class AddPaymentView(View):
    def get(self, request):
        flat_plan = FlatPlan.objects.filter(status = 1)
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        form = PaymentPlanForm() 
        return render(request, 'dashboard/add_payment_plan.html' ,{'form':form , 'off_plan':off_plan , 'flat_plan': flat_plan })

    def post(self, request):
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        flat_plan = FlatPlan.objects.filter(status = 1)
        form = PaymentPlanForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return  HttpResponseRedirect('/dashboard/add_payment_plan/')
        
        else:
            form = PaymentPlanForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_payment_plan.html' , {'form':form, 'off_plan':off_plan, 'flat_plan':flat_plan })

@method_decorator(login_required, name='dispatch')
class PaymentListView(View):
    def get(self, request):
        payment = PaymentPlan.objects.all()
        context = { 'payment_plan': payment}
        return render(request, 'dashboard/payment_plan_list.html' , context)

@method_decorator(login_required, name='dispatch')
class AddImagesView(View):
    def get(self, request):
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        form = ImagesForm() 
        return render(request, 'dashboard/add_images.html' ,{'form':form , 'off_plan':off_plan})

    def post(self, request):
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        form = ImagesForm(request.POST, request.FILES)
        module_id = request.POST['module_id']
        module_type = request.POST['module_type']
        

        if form.is_valid():
            for f in request.FILES.getlist('photo'):
                image = ImagesModule( module_id=module_id, photo=f,module_type=module_type )
                image.save()
            messages.success(request, 'Form submitted successfully!')
            return render(request, 'dashboard/add_images.html' , {'form':form  })
        else:
            form = ImagesForm()
            messages.warning(request, 'Form not submitted , Please check fields !')

        return render(request, 'dashboard/add_images.html' , {'form':form })

@method_decorator(login_required, name='dispatch')
class ImagesListView(View):
    def get(self, request):
        images = ImagesModule.objects.all()
        context = { 'images': images}
        return render(request, 'dashboard/images_list.html' , context)







@method_decorator(login_required, name='dispatch')   
class ReviewListView(View):
    def get(self, request):
        reviews = Review.objects.all()
        context = { 'reviews': reviews}
        return render(request, 'dashboard/review_list.html' , context)
    


@method_decorator(login_required, name='dispatch')
class AddBlogView(View):
    def get(self,request):
        form = BlogForm()
        return render(request, 'dashboard/add_blog.html', {'form':form})

    def post(self, request):
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_blog/')
        else:
            form = BlogForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_blog.html',{'form':form})



@method_decorator(login_required, name='dispatch')
class BlogListView(View):
    def get(self,request):
        blogs = Blog.objects.all()
        context = { 'blogs': blogs }
        return render(request, 'dashboard/blog_list.html', context)



@method_decorator(login_required, name='dispatch')
class AddNewsView(View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'dashboard/add_news.html', {'form':form})
    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_news/')
        else:
            form= NewsForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_news.html', {'form': form})
    


@method_decorator(login_required, name='dispatch')
class NewsListView(View):
    def get(self, request):
        news = News.objects.all()
        context = {'news': news}
        return render(request, 'dashboard/news_list.html', context)



@method_decorator(login_required, name='dispatch')
class AddpartnerView(View):
    def get(self, request):
        form = PartnersForm()
        return render(request, 'dashboard/add_partner.html',{'form':form})
    
    def post(self, request):
        form = PartnersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_partner/')
        else:
            form = PartnersForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_partner.html', {'form':form})



@method_decorator(login_required, name='dispatch')
class PartnerListView(View):
    def get(self, request):
        partner = Partners.objects.all()
        context = {'partner': partner}
        return render(request, 'dashboard/partner_list.html' , context)
    


@method_decorator(login_required, name='dispatch')
class AddOfficeImageView(View):
    def get(self , request):
        form = OfficeImagesForm()
        return render(request, 'dashboard/add_office_images.html', {'form':form})
    
    def post(get, request):
        form = OfficeImagesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_office_images/')
        else:
            form = OfficeImagesForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_office_images.html', {'form':form})
    



@method_decorator(login_required, name='dispatch')
class OfficeImagesListView(View):
    def get(self, request):
        office_images = OfficeImages.objects.all()
        context = {'office_images':office_images}
        return render(request, 'dashboard/office_images_list.html' , context)
    



@method_decorator(login_required, name='dispatch')
class AddProjectTextView(View):
    def get(self , request):
        form = ProjectTextForm()
        return render(request, 'dashboard/add_project_text.html', {'form':form})
    
    def post(get, request):
        form = ProjectTextForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_project_text/')
        else:
            form = ProjectTextForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_project_text.html', {'form':form})



@method_decorator(login_required, name='dispatch')
class ProjectTextListView(View):
    def get(self, request):
        projecttext = ProjectText.objects.all()
        context = {'projecttext' : projecttext}
        return render(request, 'dashboard/project_text_list.html', context)
    

@method_decorator(login_required, name='dispatch')
class ContactListView(View):
    def get(self, request):
        contact = Contact.objects.all()
        context = {'contact' : contact}
        return render(request, 'dashboard/contact_list.html', context)

@method_decorator(login_required, name='dispatch')
class AppointmentListView(View):
    def get(self, request):
        appointment = BookAppointment.objects.all()
        context = {'appointment' : appointment}
        return render(request, 'dashboard/appointment_list.html', context)


@method_decorator(login_required, name='dispatch')
class AgentInquiryListView(View):
    def get(self, request):
        agents_inquiry = AgentInquiry.objects.all()
        context = {'agents_inquiry' : agents_inquiry}
        return render(request, 'dashboard/agents_inquiry_list.html', context)






@method_decorator(login_required, name='dispatch')
class AddCMSView(View):
    def get(self, request):    
        return render(request, 'dashboard/add_cms.html')
    def post(self,request):
        form = CMSForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submitted successfully!')
            return HttpResponseRedirect('/dashboard/add_cms/')
        else:
            form = CMSForm()
            messages.warning(request, 'Form not submitted , Please check fields !')
        return render(request, 'dashboard/add_cms.html')



@method_decorator(login_required, name='dispatch')
class CMSListView(View):
    def get(self, request):
        cms = CMS.objects.all()
        context = { 'cms': cms}
        return render(request, 'dashboard/cms_list.html', context)
    




# update view 
@method_decorator(login_required, name='dispatch')
class AgentsUpdateView(UpdateView):
    model = Agents
    template_name = 'dashboard/agents_update.html'
    fields ="__all__"
    success_url = reverse_lazy('agentslist')




    
@method_decorator(login_required, name='dispatch')
class PropertiesUpdateView(UpdateView):
    model = Property
    form_class = PropertiesForm
    template_name = 'dashboard/properties_update.html'
    success_url = reverse_lazy('propertieslist')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        images_list = self.request.FILES.getlist('photo')
        for f in images_list:
            PropertyImages.objects.create(photo=f, property_img=self.object)

        messages.success(self.request, 'Form submitted successfully!')
        return HttpResponseRedirect(self.get_success_url())



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        indoor_value = self.object.indoor
        outdoor_value = self.object.outdoor
        lot_value = self.object.lot
        list_indoor = ast.literal_eval(indoor_value)
        list_outdoor = ast.literal_eval(outdoor_value)
        list_lot = ast.literal_eval(lot_value)
        pro_images = PropertyImages.objects.filter(property_img = pk)
        
        # Retrieve data from ModelB related to this ModelA instance
        agents = Agents.objects.all()
        context['agents'] = agents
        context['list_indoor'] = list_indoor
        context['list_outdoor'] = list_outdoor
        context['list_lot'] = list_lot
        context['pro_images'] = pro_images
        return context



@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'dashboard/blog_update.html'
    fields ="__all__"
    success_url = reverse_lazy('bloglist')


@method_decorator(login_required, name='dispatch')
class NewsUpdateView(UpdateView):
    model = News
    template_name = 'dashboard/news_update.html'
    fields ="__all__"
    success_url = reverse_lazy('newslist')


@method_decorator(login_required, name='dispatch')
class PartnerUpdateView(UpdateView):
    model = Partners
    template_name = 'dashboard/partner_update.html'
    fields ="__all__"
    success_url = reverse_lazy('partnerlist')


@method_decorator(login_required, name='dispatch')
class ImagesUpdateView(UpdateView):
    model = ImagesModule
    template_name = 'dashboard/images_update.html'
    fields ="__all__"
    success_url = reverse_lazy('image_list')


@method_decorator(login_required, name='dispatch')
class ProjectTextUpdateView(UpdateView):
    model = ProjectText
    template_name = 'dashboard/project_text_update.html'
    fields ="__all__"
    success_url = reverse_lazy('projecttextlist')



@method_decorator(login_required, name='dispatch')
class CMSUpdateView(UpdateView):
    model = CMS
    template_name = 'dashboard/cms_update.html'
    fields ="__all__"
    success_url = reverse_lazy('cmslist')
    

@method_decorator(login_required, name='dispatch')
class OffPlanePropertiesUpdateView(UpdateView):
    model = OffPlaneProperties
    template_name = 'dashboard/off_plan_update.html'
    fields ="__all__"
    success_url = reverse_lazy('off_plane_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        images_list = self.request.FILES.getlist('photo')
        for f in images_list:
            OffPlanePropertyImages.objects.create(photo=f, property_img=self.object)

        messages.success(self.request, 'Form submitted successfully!')
        return HttpResponseRedirect(self.get_success_url())



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        pro_images = OffPlanePropertyImages.objects.filter(property_img = pk)
        
        context['pro_images'] = pro_images
        return context

    
@method_decorator(login_required, name='dispatch')
class PopularAreaUpdateView(UpdateView):
    model = PopularArea
    template_name = 'dashboard/popular_area_update.html'
    fields ="__all__"
    success_url = reverse_lazy('popular_area_list')

@method_decorator(login_required, name='dispatch')
class FlatPlanUpdateView(UpdateView):
    model = FlatPlan
    template_name = 'dashboard/flat_plan_update.html'
    fields ="__all__"
    success_url = reverse_lazy('flat_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        context['off_plan'] = off_plan
        return context

@method_decorator(login_required, name='dispatch')
class PaymentPlanUpdateView(UpdateView):
    model = PaymentPlan
    template_name = 'dashboard/payment_plan_update.html'
    fields ="__all__"
    success_url = reverse_lazy('payment_plan_list')
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        flat_plan = FlatPlan.objects.filter(status = 1)
        context['off_plan'] = off_plan
        context['flat_plan'] = flat_plan
        return context
    
    
# delete
@method_decorator(login_required, name='dispatch')
class AgentDeleteView(DeleteView):
    model = Agents
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('agentslist')


@method_decorator(login_required, name='dispatch')
class PropertiesDeleteView(DeleteView):
    model = Property
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('propertieslist')

    



@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('bloglist')



@method_decorator(login_required, name='dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('newslist')



@method_decorator(login_required, name='dispatch')
class ProjectTextDeleteView(DeleteView):
    model = ProjectText
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('projecttextlist')



@method_decorator(login_required, name='dispatch')
class ImagesDeleteView(DeleteView):
    model = ImagesModule
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('image_list')



@method_decorator(login_required, name='dispatch')
class PartnerDeleteView(DeleteView):
    model = Partners
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('partnerlist')




@method_decorator(login_required, name='dispatch')
class CMSDeleteView(DeleteView):
    model = CMS
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('cmslist')



@method_decorator(login_required, name='dispatch')
class OffplaneDeleteView(DeleteView):
    model = OffPlaneProperties
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('off_plane_list')


@method_decorator(login_required, name='dispatch')
class PopularAreaDeleteView(DeleteView):
    model = PopularArea
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('popular_area_list')

@method_decorator(login_required, name='dispatch')
class FlatPlanDeleteView(DeleteView):
    model = FlatPlan
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('flat_list')

@method_decorator(login_required, name='dispatch')
class PaymentPlanDeleteView(DeleteView):
    model = PaymentPlan
    template_name = 'dashboard/item_confirm_delete.html'
    success_url = reverse_lazy('payment_plan_list')




#view  Details
@method_decorator(login_required, name='dispatch')
class AgentsDetailView(DetailView):
    model = Agents
    template_name = 'dashboard/agents_details.html'
    context_object_name = 'item'



@method_decorator(login_required, name='dispatch')
class PropertiesDetailView(DetailView):
    model = Property
    template_name = 'dashboard/properties_details.html'
    form_class = PropertiesForm
    context_object_name = 'item'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.object.pk
        indoor_value = self.object.indoor
        outdoor_value = self.object.outdoor
        lot_value = self.object.lot
        list_indoor = ast.literal_eval(indoor_value)
        list_outdoor = ast.literal_eval(outdoor_value)
        list_lot = ast.literal_eval(lot_value)
        pro_images = PropertyImages.objects.filter(property_img = pk)
        
        # Retrieve data from ModelB related to this ModelA instance
        agents = Agents.objects.all()
        context['form'] = self.form_class()
        context['agents'] = agents
        context['list_indoor'] = list_indoor
        context['list_outdoor'] = list_outdoor
        context['list_lot'] = list_lot
        context['pro_images'] = pro_images
        return context


@method_decorator(login_required, name='dispatch')
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'dashboard/blog_details.html'
    context_object_name = 'item'


@method_decorator(login_required, name='dispatch')
class NewsDetailView(DetailView):
    model = News
    template_name = 'dashboard/news_details.html'
    context_object_name = 'item'



@method_decorator(login_required, name='dispatch')
class PartnerDetailView(DetailView):
    model = Partners
    template_name = 'dashboard/partner_details.html'
    context_object_name = 'item'



@method_decorator(login_required, name='dispatch')
class ProjectTextDetailView(DetailView):
    model = ProjectText
    template_name = 'dashboard/project_text_details.html'
    context_object_name = 'item'


@method_decorator(login_required, name='dispatch')
class ImagesDetailView(DetailView):
    model = ImagesModule
    template_name = 'dashboard/images_details.html'
    context_object_name = 'item'



@method_decorator(login_required, name='dispatch')
class CMSDetailView(DetailView):
    model = CMS
    template_name = 'dashboard/cms_details.html'
    context_object_name = 'item'
    

@method_decorator(login_required, name='dispatch')
class OffPlanDetailView(DetailView):
    model = OffPlaneProperties
    template_name = 'dashboard/off_plan_details.html'
    context_object_name = 'item'



@method_decorator(login_required, name='dispatch')
class PopularAreaDetailView(DetailView):
    model = PopularArea
    template_name = 'dashboard/popular_area_details.html'
    context_object_name = 'item'

@method_decorator(login_required, name='dispatch')
class FlatPlanDetailView(DetailView):
    model = FlatPlan
    template_name = 'dashboard/flat_plan_details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        context['off_plan'] = off_plan
        return context

@method_decorator(login_required, name='dispatch')
class PaymentPlanDetailView(DetailView):
    model = PaymentPlan
    template_name = 'dashboard/payment_plan_details.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        off_plan = OffPlaneProperties.objects.filter(status = 1)
        flat_plan = FlatPlan.objects.filter(status = 1)
        context['off_plan'] = off_plan
        context['flat_plan'] = flat_plan
        return context






