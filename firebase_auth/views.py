from rest_framework.decorators import api_view
from firebase_admin import auth
from rest_framework.response import Response
from django.contrib.auth.models import User



# Create your views here.

@api_view(['GET'])
def delete_user(request):
    user = request.user
    uid = user.username
    try:
        user.delete()
        auth.delete_user(uid)
    except Exception as e:
        return Response({"Exception":str(e)})
    return Response({})
