from rest_framework.decorators import api_view
from firebase_admin import auth
from rest_framework.response import Response
from fintly_back.models import UserLink
from fintly import belvo_api




# Create your views here.

@api_view(['GET'])
def delete_user(request):
    current_user = request.user
    uid = current_user.username
    user_links = UserLink.objects.filter(user=current_user).values('link_id')
    try:
        belvo_api.delete_user_links(user_links)
        current_user.delete()
        auth.delete_user(uid)
    except Exception as e:
        return Response({"Exception":str(e)})
    return Response({})
