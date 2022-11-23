from django.db import models
from django.contrib.auth import get_user_model
from apps.computer.models import Laptop


User = get_user_model()

class Order(models.Model):
    
    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    product = models.ManyToManyField(
        to=Laptop,
        through='OrderItems'
    )
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
  

    def __str__(self) -> str:
        return f'Order #{self.id}'


class OrderItems(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    product = models.ForeignKey(
        to=Laptop,
        on_delete=models.RESTRICT,
        related_name='items'
    )
    quantity = models.PositiveIntegerField(default=1)









