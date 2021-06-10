"""bootcampStudentsUnite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from bootcampstudentsuniteapi.views import register_user, login_user
from rest_framework import routers
from bootcampstudentsuniteapi.views import JobBoards, GroupProjects, Profile
from django.conf import settings
from django.conf.urls.static import static

# if did not have slash is false i would have to manually place it in the url
# router is an instance of the default router class. default router class is built in to the django framework
router = routers.DefaultRouter(trailing_slash=False)

router.register(r'groupprojects', GroupProjects, 'groupproject')
router.register(r'profile', Profile, 'profile')
router.register(r'jobboard', JobBoards, 'jobboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
