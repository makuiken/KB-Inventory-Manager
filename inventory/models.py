from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

# Create your models here.
class Lumber(models.Model):
    LUMBER_TYPES = (
        ('lvl', 'Versa-Lam Beam'),
        ('knottypine', '#2 White Pine'),
        ('clearpine', 'Clear White Pine'),
        ('poplar', 'Poplar'),
        ('knottycedar', 'Knotty Cedar'),
        ('clearcedar', 'Clear Cedar'),
    )

    ref_id = models.CharField(unique=True, primary_key=True, max_length=30)
    name = models.TextField()
    lumber_type = models.CharField(max_length=30, choices= LUMBER_TYPES, null=True, default=None)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')

class Length(models.Model):
    lumber = models.ForeignKey(Lumber, on_delete=models.CASCADE)
    length = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('lumber', 'length')

    def __str__(self):
        return f"{self.lumber.ref_id}: {self.length}' - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('home')

class Invitation(models.Model):
    code = models.CharField(max_length=12, unique=True, default=get_random_string(6))
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code    