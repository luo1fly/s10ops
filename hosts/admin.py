from django.contrib import admin
from hosts import models
from hosts import auth_admin
from django.contrib.auth.models import Group
# Register your models above.


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'idc', 'port', 'enabled', 'memo')
    search_fields = ('name', 'ip_address', 'idc__name', 'port', 'enabled', 'memo')
    list_filter = ('idc', 'enabled')
    # list_editable = ('enabled',)


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_type', 'password')


class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'host_user', 'get_groups')
    filter_horizontal = ('host_groups',)

admin.site.register(models.UserProfile, auth_admin.UserProfileAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.IDC)
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)

admin.site.unregister(Group)




