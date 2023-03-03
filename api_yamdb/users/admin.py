from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role',
        'is_superuser', 'bio', 'first_name', 'last_name',
    )
    list_editable = ('role',)
    search_fields = ('username', 'role',)
