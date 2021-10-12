import uuid

from django.contrib.auth.models import User
from django.db import models


class Wallet(models.Model):
    class WalletStatus(models.TextChoices):
        ENABLE = 'Enabled'
        DISABLE = 'Disabled'

    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, primary_key=True)
    status = models.CharField(max_length=8, choices=WalletStatus.choices, default=WalletStatus.DISABLE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    enabled_at = models.DateTimeField(blank=True, null=True)
    disabled_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'


class Transaction(models.Model):
    class TransactionStatus(models.TextChoices):
        SUCCESS = 'Success'
        FAILED = 'Failed'

    id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True, primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=TransactionStatus.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refrence_id = models.UUIDField(editable=False, default=uuid.uuid4, unique=True)
    deposited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    deposited_at = models.DateTimeField(blank=True, null=True)
    withdrawn_by = models.ForeignKey(User, on_delete=models.CASCADE)
    withdrawn_at = models.DateTimeField(blank=True, null=True)
