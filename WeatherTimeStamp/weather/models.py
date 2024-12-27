from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class City(models.Model):
    name = models.CharField(max_length=255)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

class WeatherTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    humidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Процент влажности от 0 до 100'
    )
    temperature = models.IntegerField(help_text='Температура в градусах Цельсия')
    city = models.ForeignKey(City, on_delete=models.CASCADE)