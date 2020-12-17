from django.conf.urls import include
from django.urls import path
from cycleshareapi.views import register_user, login_user, complete_profile
from rest_framework import routers
from cycleshareapi.views import States

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'states', States, 'state')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('completeprofile', complete_profile),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]