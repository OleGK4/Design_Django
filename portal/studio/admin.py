from django.contrib import admin
from .models import User, Order, Category


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'surname', 'patronymic', 'email', 'role')


admin.site.register(User, UserAdmin)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'summary', 'category', 'photo_file', 'comment')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
