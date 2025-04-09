from django.contrib import admin
from .models import Breed, Dog

class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'owner')  # Отображаемые поля
    search_fields = ('name',)  # Поля для поиска
    list_filter = ('breed',)  # Фильтрация по породе

admin.site.register(Breed)
admin.site.register(Dog, DogAdmin)
