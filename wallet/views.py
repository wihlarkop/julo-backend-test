from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .serializers import WalletSerializer


class InitWalletView(APIView):
    def post(self, request):
        user_id = request.data.get('customer_xid')
        is_wallet_exists = Wallet.objects.filter(owned_by_id=user_id).exists()
        if not is_wallet_exists:
            wallet = Wallet.objects.create(owned_by_id=user_id)
            token = Token.objects.create(user_id=user_id)
        else:
            token = Token.objects.get(user_id=user_id)

        return Response({
            'data': {
                'token': token.key
            },
            'status': 'success',
        })


class WalletView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        wallet = Wallet.objects.get(owned_by=self.request.user)
        serializer = WalletSerializer(wallet)
        return Response({
            'status': 'success',
            'data': serializer.data
        })

    def post(self, request):
        wallet = Wallet.objects.get(owned_by=self.request.user)

        if wallet.status == 'Enable':
            raise NotFound('Wallet Is Active')

        if wallet:
            wallet.status = 'Enable'
            wallet.enabled_at = timezone.now()
            wallet.save()

            serializer = WalletSerializer(wallet)

            return Response({
                'status': 'success',
                'data': serializer.data
            })

    def patch(self, request):
        is_disabled = request.data.get('is_disabled')
        wallet = Wallet.objects.get(owned_by=self.request.user)

        if wallet.status == 'Disable':
            raise NotFound('Wallet Is Disabled')

        if wallet:
            if is_disabled:
                wallet.status = 'Disable'
                wallet.disabled_at = timezone.now()
                wallet.save()

                serializer = WalletSerializer(wallet)

                return Response({
                    'status': 'success',
                    'data': serializer.data
                })


class WalletDeposit(APIView):
    def post(self, request):
        pass


class WalletWithdraw(APIView):
    def post(self, request):
        pass
