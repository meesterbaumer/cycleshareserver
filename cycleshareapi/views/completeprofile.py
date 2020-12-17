import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from cycleshareapi.models import Rider

@csrf_exempt
def complete_profile(request):
    '''Handles the completion of a new riders profile

    Method arguments:
      request -- The full HTTP request object
    '''

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Now save the extra info in the cycleshareapi_rider table
    rider = Rider.objects.create(
        user=User.objects.get(user=request.auth.user),
        address=req_body['address'],
        city=req_body['city'],
        state=req_body['state'],
    )

    # Commit the user to the database by saving it
    rider.save()
