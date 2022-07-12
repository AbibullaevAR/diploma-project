"""
Realize functional for work with email.

Functions:
    send_complete_reg_mail(scheme, host, email)
"""
from django.core.mail import send_mail


def send_complete_reg_mail(scheme, host, email):
    """
    Sending complete registration letter.

    :param scheme: type protocol HTTP/HTTPS
    :type scheme: str
    :param host: server host
    :type host: str
    :param email: sending email
    :type email: str
    :return: None
    """
    send_mail(
        'Регистрация аккаунта diploma project',
        'Вы зарегистрировали аккаунт в diploma project для завершения регистрации перейдите по ссылке и сбросте ' +
        f'пароль используйте ваш email в качестве username. {scheme}://{host}/accounts/' +
        'rest_password_start/',
        None,
        [email, ],
        fail_silently=False
    )
