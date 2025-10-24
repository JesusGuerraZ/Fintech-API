from django.core.management.base import BaseCommand
from api.models import Account, Transaction
from django.utils import timezone

class Command(BaseCommand):
    help = 'Carga datos de ejemplo para Account y Transaction'

    def handle(self, *args, **options):
        # Evitar duplicados
        if Account.objects.exists():
            self.stdout.write(self.style.WARNING('Ya existen cuentas, no se cargan datos de ejemplo.'))
            return

        # Crear cuentas
        a1 = Account.objects.create(owner_name='Juan', balance=1000.00, currency='USD', created_at=timezone.now(), updated_at=timezone.now())
        a2 = Account.objects.create(owner_name='Ana', balance=500.00, currency='EUR', created_at=timezone.now(), updated_at=timezone.now())
        a3 = Account.objects.create(owner_name='Luis', balance=750.00, currency='COP', created_at=timezone.now(), updated_at=timezone.now())

        # Crear transacciones
        Transaction.objects.create(account=a1, amount=200.00, type='deposit', description='Depósito inicial', created_at=timezone.now())
        Transaction.objects.create(account=a2, amount=100.00, type='withdrawal', description='Retiro de efectivo', created_at=timezone.now())
        Transaction.objects.create(account=a1, amount=50.00, type='transfer', description='Transferencia a Ana', created_at=timezone.now(), destination_account=a2)

        self.stdout.write(self.style.SUCCESS('Datos de ejemplo cargados correctamente.'))
