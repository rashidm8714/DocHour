from django.contrib import admin

# Register your models here.
from doctor import models

admin.site.register(models.Doctor)
admin.site.register(models.Schedule)
admin.site.register(models.Specialization)
admin.site.register(models.Message)