"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from .api import RegisterView, LoginView, ChatHistory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', RegisterView.as_view()),
    path('api/login', LoginView.as_view()),
    path("api/chat/history/", ChatHistory.as_view(), name="chat-history"),
    path('', never_cache(TemplateView.as_view(template_name="index.html"))),
]