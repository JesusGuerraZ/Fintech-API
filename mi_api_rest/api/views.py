from rest_framework import viewsets, serializers
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer
from .tasks import log_transaction_creation

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    swagger_tags = ['Account']

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    swagger_tags = ['Transaction']

    def perform_create(self, serializer):
        data = serializer.validated_data
        account = data['account']
        amount = data['amount']
        tx_type = data['type']
        dest_account = data.get('destination_account')

        if tx_type == 'deposit':
            account.balance += amount
            account.save()
        elif tx_type == 'withdrawal':
            if account.balance < amount:
                raise serializers.ValidationError('Saldo insuficiente para el retiro.')
            account.balance -= amount
            account.save()
        elif tx_type == 'transfer':
            if account.balance < amount:
                raise serializers.ValidationError('Saldo insuficiente para la transferencia.')
            if not dest_account:
                raise serializers.ValidationError('Debes indicar la cuenta destino para la transferencia.')
            account.balance -= amount
            account.save()
            dest_account.balance += amount
            dest_account.save()
        instance = serializer.save()
        # Ejecutar tarea asíncrona con Celery
        log_transaction_creation.delay(account.id, amount, tx_type, data.get('description', ''))