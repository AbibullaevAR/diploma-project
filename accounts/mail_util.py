from django.core.mail import send_mail


def send_complete_reg_mail(scheme, host, email):
    send_mail(
        'Регистрация аккаунта diploma project',
        'Вы зарегистрировали аккаунт в diploma project для завершения регистрации перейдите по ссылке и сбросте ' +
        f'пароль используйте ваш email в качестве username. {scheme}//{host}/' +
        'rest_password_start/',
        'diploma project@',
        [email, ],
        fail_silently=False
    )
