from django.core.mail import send_mail
from decouple import config

HOST = config('HOST_FOR_SEND_EMAIL')

def send_activation_email(email, code):
    activation_url = f'http://{HOST}/api/account/activate/?u={code}'

    send_mail(
        'Здравствуйте! Активируйте ваш аккаунт',
        'Для активаций аккаунта, перейдите по ссылке ниже'
        f'\n{activation_url}',
        'amirzakov9@gmail.com',
        [email],
        fail_silently=False
    )


def send_reset_password_email(email, reset_token):
    send_mail(
        subject = 'Сброс пароля',
        message = f'Для сброса пароля вам требуется скопировать код ниже и ввести его на сайте\n{reset_token}',
        from_email='amirzakov9@gmail.com',
        recipient_list=[email],
        fail_silently=False
    )