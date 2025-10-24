from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task
def log_transaction_creation(account_id, amount, transaction_type, description):
    logger.info(f'Transaction created: Account ID: {account_id}, Amount: {amount}, Type: {transaction_type}, Description: {description}')

@shared_task
def send_notification(account_id):
    # Simulate sending a notification
    logger.info(f'Notification sent for Account ID: {account_id}')