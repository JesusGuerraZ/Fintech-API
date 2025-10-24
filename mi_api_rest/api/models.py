from django.db import models

class Account(models.Model):
    owner_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner_name} - {self.balance} {self.currency}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    destination_account = models.ForeignKey(Account, related_name='incoming_transfers', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        if self.type == 'transfer' and self.destination_account:
            return f"Transfer of {self.amount} from {self.account} to {self.destination_account} on {self.created_at}"
        return f"{self.type.capitalize()} of {self.amount} on {self.created_at}"