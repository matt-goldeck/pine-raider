from django.conf.urls import include
from django.urls import path
from . import views


urlpatterns = [
	path('', views.BlogLandingView.as_view(), name='blog_landing_view'),
	path('<int:pk>/', views.PostView.as_view(), name='specific_post_view'),
]
