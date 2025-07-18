"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import path, include, re_path
from sm.views import *
from django.contrib.auth import views as auth_views
from django.views.defaults import page_not_found



urlpatterns = [
    path('', IndexView.as_view(), name = "Home"),
    path('comingsoon', CommingSoon.as_view(), name="CommingSoon"),
    path('contact/', ContactView.as_view(), name = "contact" ),
    path('bookappointment/', BookAppointmentView.as_view(), name = "book"),
    path('who_we_are/', AboutView.as_view(), name ="about"),
    path('allpartner/', PartnerView.as_view(), name ="allpartner"),
    path('properties/', PropertiesView.as_view(), name = "properties"),
    path('off_plane/', OffPlaneView.as_view() , name = "offplane"),
    path('panthouse_properties/', PanthouseView.as_view(), name = "panthouse"),
    path('townhouse_properties/', TownhousesView.as_view(), name = "townhouse"),
    path('villa_properties/', VillaView.as_view(), name = "villa"),
    path('apartment_properties/', ApartmentsView.as_view(), name = "apartment"),
    path('rent_properties/', RentView.as_view(), name = "rent"),
    path('buy_properties/', BuyView.as_view(), name = "buy"),
    path('sell_properties/', SellView.as_view(), name = "sell"),
    path('searchproperties/',SerachFilterView.as_view() , name = "searchproperties"),
    path('properties_details/<int:pk>/', PropertiesWebDetailView.as_view(), name = "propertiesdetails"),
    path('blog/', BlogView.as_view(), name="blog"),
    path('blog_details/<int:pk>/', BlogWebDetailView.as_view(), name="blogdetails"),
    path('our_team/', OurTeamView.as_view(), name = "Agents"),
    path('agents/', AgentsView.as_view(), name = "Agents"),
    path('searchagents/',AgentsSearchView.as_view() , name = "searchagents"),
    path('agents_contact/' , AgentsInquiryView.as_view(), name = "agentscontact"),
    path('agents_details/<int:pk>/', AgentsWebDetailView.as_view(), name = "agentsdetails"),
    path('news/', NewsView.as_view(), name = "news"),
    path('news_details/<int:pk>/', NewsWebDetailView.as_view(), name = "newsdetails"),
    path('review/',ReviewView.as_view(), name ="review"),
    path('add_review/',AddReviewView.as_view(), name ="addreview"),
    path('comprassion/', ComprassionView.as_view(), name = "comprassion"),
    path('favorite/', FavoriteView.as_view(), name = "favorite"), 
    path('add_to_favorites/<int:pk>/', add_to_favorites, name='add_to_favorites'),
    path('add_to_comparission/<int:pk>/', add_to_comparission, name='add_to_comparission'),
    path('clear_session_list/', clear_favorites, name='clear_session_list'),
    path('clear_session_list_comp/', clear_comparission, name='clear_session_list'),
    path('term_condition/', TermConditionView.as_view(), name="termcondition"),
    path('privacy_policy/', privacypolicyView.as_view(), name="privacy"),
    path('currency_convert/<int:pk>', currency_convert , name ="cc"),
    path('off_plan/<str:property_location>/' , Locationvia, name = "loactionvia"),
    path('popular_area/', PopularAreaView.as_view(), name = "popular_area"),
    path("property_search/<str:property_type>/", property_search, name="property_search"),
    # path('<str:property_location>/<str:title>/', Titlevia, name = "namevia"),



    ##Ranjeet
    
    
    path('agent-contact-form/',agentContactFormView,name="agent-contact-form"),





    path('dashboard/index/', AdminIndexView.as_view(), name = "adminindex"),
    path('dashboard/add_agents/', AddAgentsView.as_view() , name = "addagents"),
    path('dashboard/agents_list/', AgentsListView.as_view(), name = "agentslist"),
    path('dashboard/add_properties/', AddPropertiesView.as_view() , name = "addproperties"),
    path('dashboard/add_offplane_properties/',AddOffPlanePropertiesView.as_view(), name = "offplane"),
    path('dashboard/offplane_properties_list/', AddOffPlanePropertiesListView.as_view(), name = "off_plane_list"),
    path('dashboard/add_popular_area/', AddPopularAreaView.as_view(), name = "add_popular_area"),
    path('dashboard/popular_area_list/', PopularAreaListView.as_view(), name = "popular_area_list"),
    path('dashboard/properties_list/', PropertiesListView.as_view(), name = "propertieslist"),
    path('dashboard/review_list/', ReviewListView.as_view(),name = "reviewlist"),
    path('dashboard/add_blog/', AddBlogView.as_view(), name = "addblog"),
    path('dashboard/blog_list/', BlogListView.as_view(), name = "bloglist"),
    path('dashboard/add_news/', AddNewsView.as_view(), name = "addnews"),
    path('dashboard/news_list/', NewsListView.as_view(), name = "newslist"),
    path('dashboard/add_partner/', AddpartnerView.as_view(), name = "addpartner"),
    path('dashboard/partner_list/', PartnerListView.as_view(), name = "partnerlist"),
    path('dashboard/add_office_images/', AddOfficeImageView.as_view(), name = "officeimage"),
    path('dashboard/office_images_list/', OfficeImagesListView.as_view() , name = "officeimagelist"),
    path('dashboard/add_project_text/', AddProjectTextView.as_view(), name = "ourprojecttext"),
    path('dashboard/project_text_list/', ProjectTextListView.as_view(), name = "projecttextlist"),
    path('dashboard/contact_list/', ContactListView.as_view(), name = "contactlist"),
    path('dashboard/appointment_list/', AppointmentListView.as_view(), name = "appointmentlist"),
    path('dashboard/agents_inquiry_list/', AgentInquiryListView.as_view(), name = "agentsinquirylist"),
    path('dashboard/add_cms/', AddCMSView.as_view(), name ="addcms"), 
    path('dashboard/cms_list/', CMSListView.as_view(), name = "cmslist"),

    #update
    path('dashboard/agentsupdate/<int:pk>/',  AgentsUpdateView.as_view(), name = "agentsupdate"),
    path('dashboard/propertiesupdate/<int:pk>/',  PropertiesUpdateView.as_view(), name = "propertiesupdate"),
    path('dashboard/blogupdate/<int:pk>/',  BlogUpdateView.as_view(), name = "blogupdate"),
    path('dashboard/newsupdate/<int:pk>/',  NewsUpdateView.as_view(), name = "newsupdate"),
    path('dashboard/partnerupdate/<int:pk>/',  PartnerUpdateView.as_view(), name = "partnerupdate"),
    path('dashboard/imagesupdate/<int:pk>/',  ImagesUpdateView.as_view(), name = "imagesupdate"),
    path('dashboard/projecttextupdate/<int:pk>/',  ProjectTextUpdateView.as_view(), name = "projecttextupdate"),
    path('dashboard/cmsupdate/<int:pk>/',  CMSUpdateView.as_view(), name = "cmsupdate"),
    path('dashboard/offplaneupdate/<int:pk>/',  OffPlanePropertiesUpdateView.as_view(), name = "offplaneupdate"),
    path('dashboard/popularareaupdate/<int:pk>/',  PopularAreaUpdateView.as_view(), name = "popularareaupdate"),

    # delete
    path('dashboard/agentsdelete/<int:pk>/',  AgentDeleteView.as_view(), name = "agentsdelete"),
    path('dashboard/propertiesdelete/<int:pk>/',  PropertiesDeleteView.as_view(), name = "propertiesdelete"),
    path('dashboard/blogdelete/<int:pk>/',  BlogDeleteView.as_view(), name = "blogdelete"),
    path('dashboard/newsdelete/<int:pk>/',  NewsDeleteView.as_view(), name = "newsdelete"),
    path('dashboard/projecttextdelete/<int:pk>/',  ProjectTextDeleteView.as_view(), name = "projecttextdelete"),
    path('dashboard/imagesdelete/<int:pk>/',  ImagesDeleteView.as_view(), name = "imagesdelete"),
    path('dashboard/partnerdelete/<int:pk>/',  PartnerDeleteView.as_view(), name = "partnerdelete"),
    path('dashboard/cmsdelete/<int:pk>/',  CMSDeleteView.as_view(), name = "cmsdelete"),
    path('dashboard/offplanedelete/<int:pk>/',  OffplaneDeleteView.as_view(), name = "offplanedelete"),
    path('dashboard/popularareadelete/<int:pk>/',  PopularAreaDeleteView.as_view(), name = "popularareadelete"),


    # view details
    path('dashboard/agentsdetails/<int:pk>/',  AgentsDetailView.as_view(), name = "agents_details"),
    path('dashboard/propertiesdetails/<int:pk>/',  PropertiesDetailView.as_view(), name = "properties_details"),
    path('dashboard/blogsdetails/<int:pk>/',  BlogDetailView.as_view(), name = "blog_details"),
    path('dashboard/newsdetails/<int:pk>/',  NewsDetailView.as_view(), name = "news_details"),
    path('dashboard/projecttextdetails/<int:pk>/',  ProjectTextDetailView.as_view(), name = "projecttext_details"),
    path('dashboard/imagesdetails/<int:pk>/',  ImagesDetailView.as_view(), name = "images_details"),
    path('dashboard/partnerdetails/<int:pk>/',  PartnerDetailView.as_view(), name = "partner_details"),  
    path('dashboard/cmsdetails/<int:pk>/',  CMSDetailView.as_view(), name = "cms_details"),
    path('dashboard/offplandetails/<int:pk>/',  OffPlanDetailView.as_view(), name = "off_plan_details"),  
    path('dashboard/popularareadetails/<int:pk>/',  PopularAreaDetailView.as_view(), name = "popular_area_details"),


 


    










    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('<str:property_location>/<str:title>/', Titlevia, name = "namevia"),
    path('off_plan/<str:property_location>/<str:title>/<int:pk>/', offplaneWebDetailView.as_view(), name = "offplandetails"),
    path('dashboard/add_flat/', AddFlatView.as_view(), name = "add_flat"),
    path('dashboard/flat_list/', FlatListView.as_view(), name = "flat_list"),
    path('dashboard/add_payment_plan/', AddPaymentView.as_view(), name = "add_payment_plan"),
    path('dashboard/payment_plan_list/', PaymentListView.as_view(), name = "payment_plan_list"),
    
    path('dashboard/payment_plan_details/<int:pk>/', PaymentPlanDetailView.as_view(), name = "payment_plan_details"),
    path('dashboard/flat_plan_details/<int:pk>/', FlatPlanDetailView.as_view(), name = "flat_plan_details"),
    path('dashboard/flat_plan_update/<int:pk>/', FlatPlanUpdateView.as_view(), name = "flat_plan_update"),
    path('dashboard/payment_plan_update/<int:pk>/', PaymentPlanUpdateView.as_view(), name = "payment_plan_update"),
    path('dashboard/flat_plan_delete/<int:pk>/', FlatPlanDeleteView.as_view(), name = "flat_plan_delete"),
    path('dashboard/payment_plan_delete/<int:pk>/', PaymentPlanDeleteView.as_view(), name = "payment_plan_delete"),
    path('dashboard/add_images/', AddImagesView.as_view(), name = "images_add"),
    path('dashboard/images_list/', ImagesListView.as_view(), name = "image_list"),
    
]


urlpatterns += [
    re_path(r'^.*/$', page_not_found, {'exception': Exception('Page not found')}, name='404'),
]



