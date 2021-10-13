import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    class WalletStatus(models.TextChoices):
        ENABLED = 'Enabled'
        DISABLED = 'Disabled'

    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, primary_key=True)
    status = models.CharField(max_length=8, choices=WalletStatus.choices, default=WalletStatus.DISABLED)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    enabled_at = models.DateTimeField(blank=True, null=True)
    disabled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        SUCCESS = 'Success'
        FAILED = 'Failed'

    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, primary_key=True)
    status = models.CharField(max_length=8, choices=TransactionStatus.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    refrence_id = models.UUIDField()
    transaction_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deposited_at = models.DateTimeField(blank=True, null=True)
    withdrawn_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.id}'