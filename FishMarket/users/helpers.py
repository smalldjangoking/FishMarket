import uuid
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from users.models import User


def email_sender(request, user):
    token = uuid.uuid4().hex
    redis_key = settings.REDIS_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(redis_key, {"user_id": user.id}, timeout=settings.REDIS_USER_CONFIRMATION_TIMEOUT)

    confirm_link = request.build_absolute_uri(
        reverse_lazy(
            'users:email-confirmed', kwargs={'token': token}
        )
    )

    message = (
        f"Шановний(а) {user.email},\n\n"
        "Дякуємо за реєстрацію на нашому сайті! Щоб завершити процес реєстрації та активувати ваш обліковий запис, "
        "будь ласка, підтвердьте вашу адресу електронної пошти.\n\n"
        f"Перейдіть за посиланням: {confirm_link}\n\n"
        "Посилання дійсне протягом 1 години. Якщо ви не встигнете, запросіть новий лист.\n\n"
        "Якщо ви не реєструвалися, проігноруйте це повідомлення.\n\n"
        "З повагою,\nКоманда FishMarket"
    )

    send_mail(
        subject=("Підтвердження пошти | FishMarket"),
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email, ],
    )

def user_email_activator(token):
    redis_key = settings.REDIS_USER_CONFIRMATION_KEY.format(token=token)
    token_get = cache.get(redis_key) or {}

    if token_get:
        user = get_object_or_404(User, id=token_get.get('user_id'))
        user.is_email_confirmed = True
        user.save(update_fields=['is_email_confirmed'])

        return True
    return False





