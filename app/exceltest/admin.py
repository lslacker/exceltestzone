from django.contrib import admin
from exceltest import models

# Register your models here.
admin.site.register(models.Question)
admin.site.register(models.Review)
admin.site.register(models.Choice)
admin.site.register(models.Stimulus)
