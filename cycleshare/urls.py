from django.conf.urls import include
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from rest_framework import routers
from cycleshareapi.views import register_user, login_user
from cycleshareapi.views import States, Riders, Bikes, Paymentjoins, MyBikes, BikeTypes, BikeSizes, MyReservations

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'states', States, 'state')
router.register(r'riders', Riders, 'rider')
router.register(r'bikes', Bikes, 'bike')
router.register(r'mybikes', MyBikes, 'mybike')
router.register(r'payments', Paymentjoins, 'payment')
router.register(r'biketypes', BikeTypes, 'biketype')
router.register(r'bikesizes', BikeSizes, 'bikesize')
router.register(r'reservations', MyReservations, 'reservations')



urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
