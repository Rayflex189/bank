from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from .models import UserProfile, Transaction

from django.conf import settings
from django.db import transaction as db_transaction

User = get_user_model()

@receiver(post_save, sender=UserProfile)
def create_transaction_and_send_email(sender, instance, created, **kwargs):
    # Skip newly created profiles
    if created:
        return

    # Determine old balance safely
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
        old_balance = getattr(old_instance, '_old_balance', old_instance.balance)
    except UserProfile.DoesNotExist:
        old_balance = 0

    new_balance = instance.balance
    balance_diff = new_balance - old_balance

    if balance_diff == 0:
        return  # No change

    description = getattr(instance, '_description', 'Credit' if balance_diff > 0 else 'Debit')
    amount = abs(balance_diff)
    currency = getattr(instance, 'currency', 'USD')  # Default to NGN

    # Create transaction
    Transaction.objects.create(
        user=instance.user,
        amount=amount,
        balance_after=new_balance,
        description=description
    )

    # Send email after transaction commits
    def send_balance_email():
        subject = f"💰 Your account has been {description.lower()}ed"
        message = f"""
Hi {instance.user.get_full_name() or instance.user.email},

Your account has been {description.lower()}ed by: {currency} {amount:,.2f}
Your new balance is: {currency} {new_balance:,.2f}

Thank you for banking with us!
Horizon Trust Bank Security Team
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )

        print(f"Balance updated for user: {instance.user.username}")
        print(f"{description}: {currency}{amount:,.2f} | New Balance: {currency}{new_balance:,.2f}")

    db_transaction.on_commit(send_balance_email)


# Automatically create a profile when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, balance=0)


# Track balance changes and send alerts
@receiver(pre_save, sender=UserProfile)
def track_balance_changes(sender, instance, **kwargs):
    if not instance.pk:
        # Skip if profile is new
        return

    # Fetch old instance from the database
    old_instance = UserProfile.objects.filter(pk=instance.pk).first()
    if not old_instance:
        return

    old_balance = old_instance.balance
    new_balance = instance.balance

    if new_balance != old_balance:
        # Save the difference in the instance to use in post_save
        instance._balance_diff = new_balance - old_balance
        instance._old_balance = old_balance
        instance._description = 'Credit' if new_balance > old_balance else 'Debit'

