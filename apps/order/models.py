from django.db import models
from django.contrib.auth import get_user_model
from apps.computer.models import Laptop


User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'открыто'),
        ('in_process', 'в обработке'),
        ('conceled', 'отмененный'),
        ('finished', 'завершенный')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )

