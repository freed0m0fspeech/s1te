from django.urls import path, re_path
from . import views

urlpatterns = [
    # path('', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^portfolio/$', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^portfolio/add/testimonial/$', views.AddTestimonialPageView.as_view(), name='AddTestimonialPageView'),
    # path('freedom_of_speech', views.freedom_of_speech_PageView, name='freedom_of_speech_PageView')
    # path('freedom_of_speech/rules/', views.rulesPageView, name='rules'),
    # path('freedom_of_speech/rules/<int:id>', views.rulesPageView, name='rules chapter'),
]
