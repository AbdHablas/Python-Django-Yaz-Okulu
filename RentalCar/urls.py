"""RentalCar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user import views as UserViews
from home import views
from rent.views import admin_send_pdf_rent_detail_to_email

urlpatterns = [
    path('logout/', UserViews.logout_view, name='logout_view'),
    path('login/', UserViews.login_view, name='login_view'),
    path('signup/', UserViews.signup_view, name='signup_views'),
    path('signup/', UserViews.signup_view, name='user_password'),

    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('car/', include('car.urls')),
    path('user/', include('user.urls')),
    path('rent', include('rent.urls')),
    path('contact', views.contact, name='contact'),
    path('references', views.references, name='references'),
    path('about', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('search/', views.search, name='search.urls'),
    path('category/<int:id>/<slug:slug>', views.ListCar, name='ListCar'),
    path('admin/rent/<int:pk>/send-pdf/', admin_send_pdf_rent_detail_to_email, name='send_pdf_to_email'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
