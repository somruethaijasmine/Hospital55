from django.db import models
from django.contrib.auth.models import User

class d_type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.type_name}"

class drug(models.Model):
    drug_id = models.AutoField(primary_key=True)
    drug_name = models.CharField(max_length=255)
    drug_type = models.ForeignKey(d_type, on_delete=models.CASCADE)
    drug_qty = models.IntegerField()
    drug_exp = models.DateField()
    def __str__(self):
        return f"{self.drug_name} , {self.drug_exp}"
    
class MedicationHistory(models.Model):
    drug_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)