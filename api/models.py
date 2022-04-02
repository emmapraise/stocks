from django.db import models

# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=100)
    exchange = models.CharField(max_length=100)
    is_etf = models.BooleanField(default=0)

    def __str__(self):
        return self.name
