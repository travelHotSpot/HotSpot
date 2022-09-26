"""category URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.showTable, name='showTable'),
    path('festival', views.show_festival, name='festival'),
    path('festival/<int:festival_id>/', views.festival_detail, name='festival_detail'),
    path('festival/write_comment/<int:festival_id>', views.create_comment_festival, name='create_comment_festival'),
    path('festival/delete_comment/<int:festival_id><int:comment_id>', views.delete_comment_festival, name='delete_comment_festival'),
    path('busan/', views.busan, name='busan'),
    path('busan/getPlaceList/', views.get_place_list, name='get_place_list'),
    path('api/getRoute/', views.get_route, name='get_route'),
    path('dashboard',views.dashboard, name='dashboard')
]