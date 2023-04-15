from django.db import models
from market.models import Market
from core.models import *
from association.models import Association
from core.models import BaseDB
from django.core.validators import FileExtensionValidator

#Create your models here.
class Payment(BaseDB):
    society= models.ForeignKey(Association, on_delete=models.CASCADE)
    dated= models.DateField()
    accountno=models.CharField(max_length=20, verbose_name="Account Number")
    bank_name=models.CharField(max_length=20, verbose_name="Bank name")
    accountname = models.CharField(max_length=20, verbose_name="Account Name")
    amount=models.FloatField(verbose_name="Amount Paid")
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    desc=models.TextField(blank=True,null=True)
    is_canceled=models.BooleanField(default=False,null=True)
    receipt=models.ImageField(upload_to='receipt/',null=True,validators=[FileExtensionValidator(allowed_extensions=["png","PNG","JPG","jpg","pdf"])])

    def __str__(self):
        return self.society.name+' '+str(self.amount)
