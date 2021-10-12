from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']
