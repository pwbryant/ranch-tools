from django.db import models

# Create your models here.


class Cow(models.Model):
    animal_id = models.CharField(max_length=10)
    birth_year = models.IntegerField(blank=True, null=True)

    def __repr__(self):
        return self.animal_id

    def __str__(self):
        return self.__repr__()

    class Meta:
        unique_together = [['animal_id', 'birth_year']]


class PregCheck(models.Model):
    breeding_season = models.IntegerField()
    check_date = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True)
    cow = models.ForeignKey('Cow', on_delete=models.CASCADE, blank=True, null=True)
    is_pregnant = models.BooleanField()
    recheck = models.BooleanField(default=False)

    def __repr__(self):
        preg_status = {True: 'Pregnant', False: 'Open'}[self.is_pregnant]
        return f'{self.cow} - {preg_status} - {self.check_date}'

    def __str__(self):
        return self.__repr__()
