"""pineraider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView

from blog import views as blog_views

urlpatterns = [
    path('', blog_views.HomeView.as_view(), name='home_view'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    url(r'^markdownx/', include('markdownx.urls')),
]

handler404 = blog_views.BlogView.as_view()
handler500 = lambda request: blog_views.ServerErrorView.as_view()(request)
handler403 = blog_views.ForbiddenView.as_view()