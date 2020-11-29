from django.contrib import admin
from .models import Listing, Comment, Bid, Category, Picture

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
  list_display = ('title','active','startingBid', 'currentBid','creator')

class BidAdmin(admin.ModelAdmin):
  list_display = ('user','offer','date')

class CommentAdmin(admin.ModelAdmin):
  list_display = ('user','comment','listing')

admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Picture)