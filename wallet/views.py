from django.db.models import F
from django.utils import timezone

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet, Transaction
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

        if wallet.status == 'Enabled':
            raise NotFound('Wallet Is Active')

        if wallet:
            wallet.status = 'Enabled'
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

        if wallet.status == 'Disabled':
            raise NotFound('Wallet Is Disabled')

        if wallet:
            if is_disabled:
                wallet.status = 'Disabled'
                wallet.disabled_at = timezone.now()
                wallet.save()

                serializer = WalletSerializer(wallet)

                return Response({
                    'status': 'success',
                    'data': serializer.data
                })


class WalletDeposit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        refrence_id = data.get('refrence_id')
        amount = data.get('amount')

        deposit = Transaction.objects.create(
            amount=amount,
            refrence_id=refrence_id,
            status='Success',
            transaction_by=request.user,
            deposited_at=timezone.now()
        )

        wallet_balance = Wallet.objects.get(owned_by=self.request.user)
        wallet_balance.balance = F('balance') + amount
        wallet_balance.save()

        return Response({
            'status': 'success',
            'data': {
                'deposit': {
                    'id': deposit.id,
                    'deposited_by': deposit.transaction_by.id,
                    'status': deposit.status,
                    'deposited_at': deposit.deposited_at,
                    'amount': deposit.amount,
                    'refrence_id': deposit.refrence_id
                }
            }
        })


class WalletWithdraw(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        refrence_id = data.get('refrence_id')
        amount = data.get('amount')

        wallet_balance = Wallet.objects.get(owned_by=self.request.user)
        if wallet_balance.balance < 0:
            return Response({
                'message': 'You dont have balance'
            })

        withdrawl = Transaction.objects.create(
            amount=amount,
            refrence_id=refrence_id,
            status='Success',
            transaction_by=request.user,
            withdrawn_at=timezone.now()
        )

        wallet_balance.balance = F('balance') - amount
        wallet_balance.save()

        return Response({
            'status': 'success',
            'data': {
                'deposit': {
                    'id': withdrawl.id,
                    'withdraw_by': withdrawl.transaction_by.id,
                    'status': withdrawl.status,
                    'withdraw_at': withdrawl.withdrawn_at,
                    'amount': withdrawl.amount,
                    'refrence_id': withdrawl.refrence_id
                }
            }
        })
