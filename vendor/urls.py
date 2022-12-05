from django.urls import path
from accounts import views as AccountViews
from . import views

urlpatterns = [
    path('', AccountViews.vendorDashboard,name='vendor'),
    path('profile/',views.vprofile,name='vprofile'),

    
]