from django.urls import path, include
from .views import SignUpView

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('registration/', include('social_django.urls', namespace="social")),
]
