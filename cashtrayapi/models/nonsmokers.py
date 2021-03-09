from django.db import models
from django.contrib.auth.models import User

class Nonsmoker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    quit_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    cigs_per_day = models.IntegerField()
    price_per_pack = models.FloatField()
    cigs_per_pack = models.IntegerField()
    start_smoking_year = models.DateField(auto_now=False, auto_now_add=False)