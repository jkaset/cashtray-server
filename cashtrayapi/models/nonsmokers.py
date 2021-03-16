from django.db import models
from django.contrib.auth.models import User

class Nonsmoker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quit_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    cigs_per_day = models.IntegerField(null=True)
    price_per_pack = models.FloatField(null=True)
    cigs_per_pack = models.IntegerField(null=True)
    start_smoking_year = models.DateField(auto_now=False, auto_now_add=False, null=True)

    # custom property time_smoke_free and serialize it, edit list function with quit_date - datetime.datetime.now()

    @property
    def time_smoke_free(self):
        return self.__time_smoke_free

    @time_smoke_free.setter
    def time_smoke_free(self, value):
        self.__time_smoke_free = value

