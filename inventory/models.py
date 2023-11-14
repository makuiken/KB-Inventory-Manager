from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
import random, math

#Exceptions
class LengthExistsError(Exception):
    pass

#Default Functions
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


#Model for boards
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

#Model for lengths
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
        if self.quantity == 0:
            self.delete()
        else:
            super().save(*args, **kwargs)
    

#Model for Sales
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
    
    def cut_from(self, user, product_id, selected, desired, quantity):
        
        # Get the selected length object
        length_obj = Length.objects.get(lumber=product_id, length=selected)
        remaining = []
        min_size = 8

        if selected == desired and Length.objects.filter(lumber=length_obj.lumber, length=desired).exists():
            raise LengthExistsError("This length already exists.")    
        
        if selected % desired == 0 and min_size <= desired:
            can_cut = math.ceil(selected / desired)
            can_cut
            min_size = 0
        else:
            can_cut = math.floor((selected - min_size) / desired)
            can_cut
        
        if desired * can_cut <= selected:
            boards_needed = math.ceil(quantity/can_cut)
        elif desired > ((selected - min_size)/2):
            boards_needed = math.ceil(quantity/can_cut)
        else:
            boards_needed = math.ceil(quantity/can_cut) + 1
        
        if can_cut > 1 and desired * quantity < selected:
            final_board_cut = 1
        elif can_cut > 1:
            final_board_cut = (quantity % can_cut)
            if final_board_cut == 0:
                final_board_cut = can_cut
        else:
            final_board_cut = 1
        
        if boards_needed > 1:
            for i in range(boards_needed-1):
                remaining.append(selected - (can_cut * desired))
            remaining.append(selected - (final_board_cut * desired))
        else:
            remaining.append(selected - desired * quantity)
        
        #Delete boards used
        for i in range(boards_needed):
            length_obj.quantity -= 1
            length_obj.save()

        #Add remaining length
        for i in range(len(remaining)):
            remaining_length_obj, created = Length.objects.get_or_create(
                lumber=length_obj.lumber,
                length=remaining[i],
                defaults={'quantity': 0}
            )
        # Update the quantity of the remaining length
            if remaining_length_obj.length != 0:
                remaining_length_obj.quantity += 1
                remaining_length_obj.save()     
            else:
                remaining_length_obj.delete()      

        for _ in range(quantity):
            desired_length_obj, created = Length.objects.get_or_create(
                lumber=length_obj.lumber,
                length=desired,
                defaults={'quantity': 0}
            
            )
        # Update the quantity of the desired length
            desired_length_obj.quantity += 1
            desired_length_obj.save()  
        
        # Return the desired_length_obj to indicate the operation was successful
        return desired_length_obj


#Model for monitoring changes (WIP)
class ChangeLog(models.Model):
    change_code = models.CharField(max_length=6, primary_key=True, default=generate_random_change_code)
    datetime = models.DateTimeField(auto_now_add=True)
    CHANGE_TYPE_CHOICES = [
        ('sale', 'Sale'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    ]
    changetype = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
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