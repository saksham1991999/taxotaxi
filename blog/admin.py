from django.contrib import admin
from . import models
# Register your models here.


class postAdmin(admin.ModelAdmin):
    list_display = ['title',
                    'category',
                    'date',
                    'published',
                    ]
    list_display_links = [
        'title',
        'category',
    ]
    list_filter = ['title',
                    'category',
                    'date',
                    'published',
    ]
    search_fields = [
                    'title',
                    'category',
                    'date',
                    'published',
                    'content',
    ]

class commentAdmin(admin.ModelAdmin):
    list_display = ['post',
                    'user',
                    'date',
                    ]
    list_display_links = [
        'post',
    ]
    list_filter = ['post',
                    'user',
                    'date',
    ]
    search_fields = [
        'post',
        'user',
        'date',
        'comment_text',
    ]

class likeAdmin(admin.ModelAdmin):
    list_display = ['post',
                    'user',
                    ]
    list_display_links = [
        'post',
    ]
    list_filter = ['post',
                    'user',
    ]
    search_fields = [
        'post',
        'user',
    ]

class categoriesAdmin(admin.ModelAdmin):
    list_display = ['title',
                    ]
    list_display_links = [
        'title',
    ]
    list_filter = ['title',
    ]
    search_fields = [
        'title',
        'keywords',
    ]


admin.site.register(models.post, postAdmin)
admin.site.register(models.comment, commentAdmin)
admin.site.register(models.like, likeAdmin)
admin.site.register(models.categories, categoriesAdmin)
