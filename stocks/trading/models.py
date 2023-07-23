from django.db import models


class Portfolio(models.Model):
    asset = models.CharField(max_length=4)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.asset

    

class Transaction(models.Model):
    quantity = models.IntegerField(null=True)
    price = models.IntegerField(null=True)
    symbol = models.CharField(max_length=4)
    date = models.DateTimeField(null=True)




    