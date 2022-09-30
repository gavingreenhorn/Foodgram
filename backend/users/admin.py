from django.contrib import admin, auth
from django.contrib.auth.admin import UserAdmin

User = auth.get_user_model()


@admin.register(User)
class FoodgramUserAdmin(UserAdmin):
    list_filter = ('username', 'email')

    admin_fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username", "first_name", "last_name",
                    "email", "password1", "password2", "is_active"),
            },
        ),
    )

    def get_fieldsets(self, request, obj):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)
        if not obj:
            return self.add_fieldsets
        else:
            return self.admin_fieldsets
