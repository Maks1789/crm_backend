from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    class EventType(models.TextChoices):
        MEETING = 'meeting', 'Зустріч'
        PRESENTATION = 'presentation', 'Презентація'
        TRAINING = 'training', 'Тренінг'
        DINNER = 'dinner', 'Вечеря'
        OTHER = 'other', 'Інше'

    title = models.CharField('Назва події', max_length=200)

    clients = models.ManyToManyField(
        'Client',
        blank=True,
        null=True,
        related_name='events',
        verbose_name='Клієнти (якщо є)'
    )
    description = models.TextField('Опис', blank=True)
    start = models.DateTimeField('Початок')
    end = models.DateTimeField('Кінець')
    event_type = models.CharField(
        'Тип події',
        max_length=20,
        choices=EventType.choices,
        default=EventType.MEETING
    )
    price = models.IntegerField(default=0)
    payed = models.BooleanField(default=False)
    performed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name='Власник'
    )
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Подія'
        verbose_name_plural = 'Події'
        ordering = ['start']

    def __str__(self):
        return f'{self.title} ({self.start} - {self.end})'


class Client(models.Model):
    name = models.CharField('Ім\'я', max_length=50)
    last_name = models.CharField('Прізвище', max_length=50)
    fathers_name = models.CharField('Пo-батькові', max_length=50, blank=True, null=True)
    email = models.EmailField('Електронна пошта', max_length=255, blank=True, null=True, unique=True)
    phone_number = models.CharField('Номер телефону', max_length=20, blank=True, null=True, unique=True)
    company = models.CharField('Компанія', max_length=255, blank=True, null=True)
    how_payed = models.IntegerField(default=0)
    date_of_birth = models.DateField('Дата народження', blank=True, null=True)
    first_contact = models.DateTimeField('Перший контакт', auto_now_add=True)
    last_contact = models.DateTimeField('Останній контакт', auto_now=True)

    owner = models.ForeignKey(  # ✅ Зв'язок з користувачем, який є "власником" цього клієнта
        User,
        on_delete=models.CASCADE,
        related_name='clients',  # Зручна назва для зворотного зв'язку
        verbose_name='Власник клієнта'
    )

    # events = models.ManyToManyField(
    #     Event,
    #     related_name='participants',
    #     verbose_name='Події за участю'
    # )
# Додаткова інформація
    notes = models.TextField('Примітки', blank=True, null=True)
    address = models.TextField('Адреса', blank=True, null=True)
    # Статуси
    is_active = models.BooleanField('Активний', default=True)  # Чи є клієнт активним
    # client_status = models.CharField('Статус клієнта', max_length=50, blank=True, null=True) # Наприклад: 'Lead', 'Customer', 'Lost'

    # Дата створення та оновлення
    created_at = models.DateTimeField('Створено', auto_now_add=True)
    updated_at = models.DateTimeField('Оновлено', auto_now=True)

    class Meta:
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
        ordering = ['last_name']

    def __str__(self):
        return self.last_name # Буде відображатися як "title" на фронтенді