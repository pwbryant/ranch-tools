from django.db import models

# Create your models here.


PREG_STATUS_CHOICES = (('O', 'Open',), ('P', 'Pregnant',))


class Cow(models.Model):
    animal_id = models.CharField(max_length=10, unique=True)
    birth_year = models.IntegerField(blank=True, null=True)

    def __repr__(self):
        return self.animal_id

    def __str__(self):
        return self.__repr__()


class PregCheck(models.Model):
    breeding_season = models.IntegerField()
    check_date = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True)
    cow = models.ForeignKey('Cow', on_delete=models.CASCADE, blank=True, null=True)
    preg_status = models.CharField(max_length=1, choices=PREG_STATUS_CHOICES, blank=False)

    def __repr__(self):
        return f'{self.cow} - {self.preg_status} - {self.check_date}'

    def __str__(self):
        return self.__repr__()
