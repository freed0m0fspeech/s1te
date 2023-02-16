from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^freedom_of_speech/$', views.HomePageView.as_view(), name='HomePageView'),
    re_path(r'^freedom_of_speech/profile/$', views.ProfilePageView.as_view(), name='ProfilePageView'),
    re_path(r'^freedom_of_speech/profile/(?P<username>[^\\/]+)/$', views.ProfilePageView.as_view(), name='UserProfilePageView'),
    re_path(r'^freedom_of_speech/signin/$', views.SignInPageView.as_view(), name='SignInPageView'),
    re_path(r'^freedom_of_speech/signup/$', views.SignUpPageView.as_view(), name='SignUpPageView'),
    re_path(r'^freedom_of_speech/signout/$', views.SignOutPageView.as_view(), name='SignOutPageView'),
    re_path(r'^freedom_of_speech/add/testimonial/$', views.AddTestimonialPageView.as_view(), name='AddTestimonialPageView'),
    re_path(r'^freedom_of_speech/edit/constitution/$', views.EditConstitutionPageView.as_view(), name='EditConstitutionPageView'),
    re_path(r'^freedom_of_speech/edit/laws/$', views.EditLawsPageView.as_view(), name='EditLawsPageView'),
    re_path(r'^freedom_of_speech/edit/username/$', views.EditUsernamePageView.as_view(), name='EditUsernamePageView'),
    re_path(r'^freedom_of_speech/edit/password/$', views.EditPasswordPageView.as_view(), name='EditPasswordPageView'),
    re_path(r'^freedom_of_speech/auth/telegram/$', views.AuthTelegramPageView.as_view(), name='AuthTelegramPageView'),
    # path('freedom_of_speech/edit', views.edit_constitution_button, name='edit_constitution_button'),
    # path('freedom_of_speech', views.freedom_of_speech_PageView, name='freedom_of_speech_PageView')
    # path('freedom_of_speech/rules/', views.rulesPageView, name='rules'),
    # path('freedom_of_speech/rules/<int:id>', views.rulesPageView, name='rules chapter'),
]
