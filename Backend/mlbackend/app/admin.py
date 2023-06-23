from django.contrib import admin
from app.models import SaveImage
# Register your models here.

@admin.register(SaveImage)
class SaveImageAdmin(admin.ModelAdmin):
    list_display = ('id','comeing_img','output_img')
