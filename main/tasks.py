
from project.celery import app

from django.core.mail import send_mail

from django.conf import settings

from datetime import datetime, date

from .models import Task



@app.task
def check_tasks():
    print("check_tasks")
    tasks = Task.objects.filter(closed = False, verified = False)

    today = datetime.today().date()

    for task in tasks:
        print(task)
        if task.deadline >= today:
            print('>>>>')
            if task.deadline == today:
                print('today')
                send_notification_email_to_user.apply_async(args=[task.id, 'LAST DAY'])
                send_notification_email_to_verificator.apply_async(args=[task.id, 'LAST DAY'])

                continue


            date_day = date(task.deadline.year,
                            task.deadline.month,
                            task.deadline.day - 1)

            if date_day == today:
                print('one day')
                send_notification_email_to_user.apply_async(args=[task.id, 'ONE DAY'])
                send_notification_email_to_verificator.apply_async(args=[task.id, 'ONE DAY'])

                continue


            date_week = date(task.deadline.year,
                      task.deadline.month,
                      task.deadline.day - 7)

            if date_week == today:
                print('one week')
                send_notification_email_to_user.apply_async(args=[task.id, 'ONE WEEK'])
                send_notification_email_to_verificator.apply_async(args=[task.id, 'ONE WEEK'])
        else:
            task.closed = True
            task.save()
            #take money
            send_over_email_to_user.apply_async(args = [task.id])
            send_over_email_to_verificator.apply_async(args = [task.id])




@app.task
def send_verification_email_to_user(obj_id):
    obj = Task.objects.get(pk = obj_id)
    send_mail(
        f'Создание новой цели на {settings.SERVICE_NAME}',
        f"""Здравствуйте! На {settings.SERVICE_NAME} было создана новая цель на этот email.
                Данные цели:
                    Цель: {obj.goal}
                    Дедлайн: {obj.deadline}
                    Цена за невыполнение: {obj.payment}
                    Почта верификатора(кто подтвердит выполнение цели): {obj.verificator_email}
                """,
        settings.EMAIL_HOST_USER,
        [f'{obj.user_email}'])


@app.task
def send_verification_email_to_verificator(obj_id):
    obj = Task.objects.get(pk=obj_id)
    send_mail(
        f'Вас обозначили как верификатора на {settings.SERVICE_NAME}',
        f"""Здравствуйте! На {settings.SERVICE_NAME} было создана новая цель где вы были обозначены как верификатор(кто подтвердит вполнение цели).
                        Данные цели:
                            Цель: {obj.goal}
                            Дедлайн: {obj.deadline}
                            Цена за невыполнение: {obj.payment}
                            Почта создателя: {obj.user_email}

                    Для подтверждения выполнения задания перейдите по ссылке: http://{settings.SERVICE_DOMEN}/verify/{obj.id}
                        """,
        settings.EMAIL_HOST_USER,
        [f'{obj.verificator_email}'])


@app.task
def send_notification_email_to_user(obj_id, time):
    obj = Task.objects.get(pk=obj_id)
    send_mail(
        f'YOU HAVE {time}!',
        f"""Hi, you {time.lower()} day to rich your goal.
                    Данные цели:
                        Цель: {obj.goal}
                        Дедлайн: {obj.deadline}
                        Цена за невыполнение: {obj.payment}
                        Почта верификатора(кто подтвердит выполнение цели): {obj.verificator_email}
                    """,
        settings.EMAIL_HOST_USER,
        [f'{obj.user_email}'])


@app.task
def send_notification_email_to_verificator(obj_id, time):
    obj = Task.objects.get(pk=obj_id)
    send_mail(
        f'YOU HAVE {time}!',
        f"""Hi, did you forgot to verificate goal?
                        Данные цели:
                            Цель: {obj.goal}
                            Дедлайн: {obj.deadline}
                            Цена за невыполнение: ${obj.payment}
                            Почта создателя: {obj.user_email}

                    Для подтверждения выполнения задания перейдите по ссылке: http://{settings.SERVICE_DOMEN}/verify/{obj.id}
                        """,
        settings.EMAIL_HOST_USER,
        [f'{obj.verificator_email}'])


@app.task
def send_over_email_to_user(obj_id):
    obj = Task.objects.get(pk=obj_id)
    send_mail(
        f'YOU LOSE!',
        f"""Hi, You passed time for rich goal.
                    Данные цели:
                        Цель: {obj.goal}
                        Дедлайн: {obj.deadline}
                        Цена за невыполнение: {obj.payment}
                        Почта верификатора(кто подтвердит выполнение цели): {obj.verificator_email}
                    """,
        settings.EMAIL_HOST_USER,
        [f'{obj.user_email}'])


@app.task
def send_over_email_to_verificator(obj_id):
    obj = Task.objects.get(pk=obj_id)
    send_mail(
        f'YOU LOSE!',
        f"""Hi, a goal in which you verificator has over.
                        Данные цели:
                            Цель: {obj.goal}
                            Дедлайн: {obj.deadline}
                            Цена за невыполнение: {obj.payment}
                            Почта создателя: {obj.user_email}
                        """,
        settings.EMAIL_HOST_USER,
        [f'{obj.verificator_email}'])