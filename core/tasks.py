from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# Assuming models might be needed in the future
# from escrow.models import Escrow
# from .services import BlockchainService

@shared_task
def send_email_notification_task(recipient_email, subject, message):
    """
    A shared Celery task to send an email notification.
    """
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        return f"Email sent to {recipient_email}"
    except Exception as e:
        # Handle exceptions, maybe retry the task
        return f"Failed to send email to {recipient_email}: {e}"

@shared_task
def check_escrow_funding_task():
    """
    Periodically checks for escrow deals that should be funded.
    This is a placeholder task. A real implementation would query the blockchain.
    """
    # Placeholder logic
    # two_hours_ago = timezone.now() - timedelta(hours=2)
    # pending_escrows = Escrow.objects.filter(status='CREATED', created_at__lte=two_hours_ago)

    # blockchain_service = BlockchainService()

    # for escrow in pending_escrows:
    #     is_funded = blockchain_service.get_deal_status(escrow.deal_id, escrow.order.currency)
    #     if is_funded:
    #         escrow.status = 'FUNDED'
    #         escrow.save()
    #         # Notify user
    #         send_email_notification_task.delay(
    #             escrow.order.buyer.email,
    #             "Your order has been funded!",
    #             f"The escrow for order #{escrow.order.id} has been successfully funded."
    #         )

    return "Checked escrow funding status for pending deals."
