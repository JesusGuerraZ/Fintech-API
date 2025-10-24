from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner_name', 'balance', 'currency', 'created_at', 'updated_at']
        swagger_schema_fields = {
            'example': {
                'owner_name': 'Juan',
                'balance': '1000.00',
                'currency': 'USD'
            }
        }

class TransactionSerializer(serializers.ModelSerializer):
    destination_account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False, allow_null=True)

    def validate(self, data):
        if data.get('type') == 'transfer' and not data.get('destination_account'):
            raise serializers.ValidationError({'destination_account': 'Este campo es obligatorio para transferencias.'})
        return data

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'type', 'description', 'created_at', 'destination_account']
        swagger_schema_fields = {
            'example': {
                'account': 1,
                'amount': '200.00',
                'type': 'deposit',
                'description': 'Depósito inicial',
                'created_at': '2025-10-23T01:00:00Z',
                'destination_account': None
            },
            'transfer_example': {
                'account': 1,
                'amount': '50.00',
                'type': 'transfer',
                'description': 'Transferencia a Ana',
                'created_at': '2025-10-23T03:00:00Z',
                'destination_account': 2
            }
        }