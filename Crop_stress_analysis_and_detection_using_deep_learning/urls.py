"""
URL configuration for Crop_stress_analysis_and_detection_using_deep_learning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from . import views as mv
from Admin import views as av
from Users import views as uv
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    #main view urls
    path('admin/', admin.site.urls),
    path('',mv.index,name='index'),
    path('userRegister',mv.userRegister,name='userRegister'),
    path('userLogin',mv.userLogin,name='userLogin'),
    path('adminLogin',mv.adminLogin,name='adminLogin'),

    #adminusrls
    path('adminLoginCheck',av.adminLoginCheck,name='adminLoginCheck'),
    path('adminHome',av.adminHome,name='adminHome'),
    path('userDetails',av.userDetails,name='userDetails'),
    path('activateUser',av.activateUser,name='activateUser'),
    path('deleteUser',av.deleteUser,name='deleteUser'),



    #userUrls
    path('userHome',uv.userHome,name='userHome'),
    path('register',uv.register,name='register'),
    path('userLoginCheck',uv.userLoginCheck,name='userLoginCheck'),
    path('Classification_result',uv.Classification_result,name='Classification_result'),
    path('prediction',uv.prediction,name='prediction'),
    

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)