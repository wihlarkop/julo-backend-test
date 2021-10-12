from django.urls import path

from .views import InitWalletView, WalletView, WalletDeposit, WalletWithdraw

app_name = 'wallet'

urlpatterns = [
    path('init/', InitWalletView.as_view(), name='init'),
    path('', WalletView.as_view(), name='wallet'),
    path('deposits/', WalletDeposit.as_view(), name='wallet'),
    path('withdrawals/', WalletWithdraw.as_view(), name='wallet'),
]
