from django.contrib import admin

from .models import Profile, NewsLetterSubscription
from django.contrib.auth.models import User
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'gender', 'category', 'blood_group', 'state', 'verified']
    list_editable = ['verified']
    list_filter = ['verified']

    def name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

admin.site.register(Profile, ProfileAdmin)

admin.site.register(NewsLetterSubscription)