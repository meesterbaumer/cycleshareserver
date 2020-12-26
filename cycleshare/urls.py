from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from cycleshareapi.views import register_user, login_user
from cycleshareapi.views import States, Riders, Bikes, Paymentjoins

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'states', States, 'state')
router.register(r'riders', Riders, 'rider')
router.register(r'bikes', Bikes, 'bike')
router.register(r'payments', Paymentjoins, 'payment')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
