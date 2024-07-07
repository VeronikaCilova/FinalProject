"""personalportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from viewer.views import *

from personalportal import settings
from viewer.views import ProfileView, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='homepage'),
    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/password_change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/profile', ProfileView.as_view(), name='profile_detail'),
    path('profile/<pk>/', ProfileView.as_view(), name='profile'),

    path('goals/', GoalsView.as_view(), name='goals'),
    path('goal/<pk>/', GoalView.as_view(), name='goal'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
