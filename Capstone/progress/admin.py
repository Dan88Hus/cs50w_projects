from django.contrib import admin
from .models import Started, Proceeding, Completed, Cancelled, User

# Register your models here.
admin.site.register(User)
admin.site.register(Started)
admin.site.register(Proceeding)
admin.site.register(Completed)
admin.site.register(Cancelled)
