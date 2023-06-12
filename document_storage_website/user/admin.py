from django.contrib import admin
from user.models import user, pass_data

# Register your models here.

class user_admin(admin.ModelAdmin):
    list_display = ("username", "password", "create_at")

class pass_data_admin(admin.ModelAdmin):
    list_display = ("user_id", "name", "username", "password", "last_modified_date")

admin.site.register(user, user_admin)
admin.site.register(pass_data, pass_data_admin)
