from django.utils import timezone
from rest_framework import serializers

from .models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']


class DepositSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = ['amount', 'refrence_id']


class WithdrawnSerializer(serializers.ModelSerializer):
    withdrawn_by = serializers.SerializerMethodField(source='transaction_by')

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_by', 'status', 'deposited_at', 'amount', 'refrence_id']
