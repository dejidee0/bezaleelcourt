from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('pricing/', pricing, name='pricing'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('faq/', faq, name='faq'),
    path('services/', services, name='services'),
    path('add-property/', add_property, name='add_property'),
    path('verification-required/', verification_required, name='verification_required'),
    path('my-profile/', my_profile, name='my_profile'),
   
]