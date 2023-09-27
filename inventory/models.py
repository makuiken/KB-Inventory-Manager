from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
import random

class LengthExistsError(Exception):
    pass

def get_default_user():
    default_user, created = User.objects.get_or_create(
        username='default_user',
        defaults={
            'email': 'default_user@example.com',
            'first_name': 'Default',
            'last_name': 'User',
        }
    )
    return default_user.id

def generate_random_change_code():
    while True:
        code = random.randint(100000, 999999)
        if not ChangeLog.objects.filter(change_code=str(code)).exists():
            return str(code)
        
def generate_random_sales_code():
    while True:
        code = random.randint(100000, 999999)
        if not Sale.objects.filter(sales_code=str(code)).exists():
            return str(code)


# Create your models here.
class Lumber(models.Model):
    LUMBER_TYPES = (
        ('lvl', 'Versa-Lam Beam'),
        ('knottypine', '#2 White Pine'),
    )

    ref_id = models.CharField(unique=True, primary_key=True, max_length=30)
    name = models.TextField()
    lumber_type = models.CharField(max_length=30, choices= LUMBER_TYPES, null=True, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    
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
        return f"{self.lumber.ref_id}: {self.length}'"
    
    def get_absolute_url(self):
        return reverse('home')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # Create a new ChangeLog entry
        change_log = ChangeLog(
            length_user=self.lumber.user,  # Use the lumber.user field instead of self.user
            changetype='adjustment',
        )
        change_log.save()

class Sale(models.Model):
    sales_code = models.CharField(max_length=6, primary_key=True, default=generate_random_sales_code)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    datetime = models.DateTimeField(auto_now_add=True)
    CHANGE_TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    ]
    changetype = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES, default="adjustment")
    salesorder = models.IntegerField(null=True, blank=True)
    product_id = models.ForeignKey(Lumber, on_delete=models.CASCADE)
    length = models.ForeignKey(Length, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.sales_code}: {self.length}' - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('home')
    
    def cut_from(self, user, product_id, selected_length, desired_length, quantity):
        # Get the selected length object
        length_obj = Length.objects.get(lumber=product_id, length=selected_length)

        if selected_length == desired_length and Length.objects.filter(lumber=length_obj.lumber, length=desired_length).exists():
            raise LengthExistsError("This length already exists.")

        # Check if there is enough quantity available for the cuts
        if length_obj.quantity < quantity:
            raise ValueError("Not enough quantity available for the requested cuts.")

        for _ in range(quantity):
            # Calculate the remaining length after cutting
            remaining_length = selected_length - desired_length

            # Update the quantity of the selected length
            length_obj.quantity -= 1
            length_obj.save()

            # Check if there's an existing length object with the remaining length
            remaining_length_obj, created = Length.objects.get_or_create(
                lumber=length_obj.lumber,
                length=remaining_length,
                defaults={'quantity': 0}
            )

            # Update the quantity of the remaining length
            remaining_length_obj.quantity += 1
            remaining_length_obj.save()

            # Get or create the desired length instance
            desired_length_obj, created = Length.objects.get_or_create(
                lumber=length_obj.lumber,
                length=desired_length,
                defaults={'quantity': 0}
            )

            # Update the quantity of the desired length
            desired_length_obj.quantity += 1
            desired_length_obj.save()

        # Return the desired_length_obj to indicate the operation was successful
        return desired_length_obj

class ChangeLog(models.Model):
    change_code = models.CharField(max_length=6, primary_key=True, default=generate_random_change_code)
    datetime = models.DateTimeField(auto_now_add=True)
    CHANGE_TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    ]
    changetype = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES)
    lumber_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='lumber_changelog')
    length_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='length_changelog')
    sale_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sale_changelog')

    def __str__(self):
        user = self.lumber_user or self.length_user or self.sale_user
        return f"{self.change_code}: {self.changetype} - {user} | {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}"

class Invitation(models.Model):
    code = models.CharField(max_length=12, unique=True, default=get_random_string(6))
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.code    