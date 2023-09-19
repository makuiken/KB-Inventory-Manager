from django.db import models

# Create your models here.
class Lumber(models.Model):
    ref_id = models.CharField(unique=True, primary_key=True, max_length=30)
    name = models.TextField()
    
    def __str__(self):
        return self.name

class Length(models.Model):
    ref_id = models.ForeignKey(Lumber, on_delete=models.CASCADE)
    length = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.ref_id}: {self.length}' - {self.quantity}"