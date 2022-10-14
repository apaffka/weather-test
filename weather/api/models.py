from django.db import models


class Loging(models.Model):
    date = models.DateTimeField('request date', auto_now_add=True)
    city = models.CharField('city', max_length=200)
    latitude = models.CharField('latitude', max_length=50)
    longitude = models.CharField('longitude', max_length=50)
    status = models.CharField('status', max_length=200)

    class Meta:
        ordering = ['date']
        verbose_name = 'Логи'
        verbose_name_plural = 'Логи'

    def __str__(self):
        return f'{self.date}, {self.city}, {self.status}'
