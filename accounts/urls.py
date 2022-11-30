from django.urls import path
from . import views

urlpatterns = [
    path('registerUser/', views.registerUser,name='registerUser'),
    path('registerVender/', views.registerVender,name='registerVender'),

    path('login/', views.login,name='login'),
    path('logout/', views.logout,name='logout'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('cusDashboard/', views.cusDashboard,name='cusDashboard'),
    path('vendorDashboard/', views.vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    
]