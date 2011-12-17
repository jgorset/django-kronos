from django.http import HttpResponse

from fandjango.decorators import facebook_authorization_required

@facebook_authorization_required()
def home(request):
    return HttpResponse()