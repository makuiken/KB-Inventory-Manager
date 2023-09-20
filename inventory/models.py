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

    class Meta:
        unique_together = ('ref_id', 'length')

    def __str__(self):
        return f"{self.ref_id}: {self.length}' - {self.quantity}"
    
    def save(self, *args, **kwargs):
    # Check if a record with the same ref_id and length already exists
        existing_length = Length.objects.filter(ref_id=self.ref_id, length=self.length).first()

        if existing_length:
            # Update the quantity of the existing record
            existing_length.quantity += self.quantity
            existing_length.save()
        else:
            # Create a new record
            super().save(*args, **kwargs)