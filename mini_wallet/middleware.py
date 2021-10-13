import json

from django.http import HttpResponse
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_401_UNAUTHORIZED

from wallet.models import Wallet


class WalletMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith(reverse('wallet:wallet')) and request.method == 'GET' or request.path.startswith(
                reverse('wallet:deposits')) or request.path.startswith(reverse('wallet:withdraws')):
            auth = request.headers.get('Authorization')
            if not auth:
                return HttpResponse(json.dumps('Token Is Required'), status=HTTP_401_UNAUTHORIZED)

            token = auth.split()[1]
            token_obj = Token.objects.get(key=token)
            wallet = Wallet.objects.get(owned_by=token_obj.user)

            if wallet.status == 'Disabled':
                return HttpResponse(json.dumps('Wallet Is Disable You Need Activate Wallet'),
                                    status=HTTP_401_UNAUTHORIZED)
