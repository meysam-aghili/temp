from django.db import models

# Create your models here.

class user(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=30)
    create_at = models.DateTimeField(auto_now_add=True, blank=True)

class pass_data(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=30)
    last_modified_date = models.DateTimeField(auto_now_add=True, blank=True)
 
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'name'], name='unique_user_id_name_combination'
            )
        ]