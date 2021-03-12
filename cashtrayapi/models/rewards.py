from django.db import models

class Reward(models.Model):
    user = models.ForeignKey("Nonsmoker", on_delete=models.CASCADE)
    reward_name = models.CharField(max_length=50)
    reward_cost = models.FloatField()
    redeemed = models.BooleanField(default=False)