from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .form import UserCreationForm, UserChangeForm



# Register your models here.

# class UserResource(resources.ModelResource):
#    class Meta:
#       model = CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

  #resource_class = UserResource
  form = UserChangeForm
  add_form = UserCreationForm

  fieldsets = (
    (None, {'fields': ('email', 'password')}),
    ('Permission', {'fields': ('is_active', 'is_admin', 'is_superuser', 'groups', 'user_permissions')})
  )

  add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
  
  list_display = ('email', 'is_superuser')
  list_filter = ('email', 'is_active',)
  search_fields = ('email',)
  ordering = ('email',)