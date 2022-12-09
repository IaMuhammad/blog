from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, path
from django.utils.html import format_html

from apps import models
from apps.models import Blog, Category, Coment, CustomUser, Message


# Register your models here.

@register(CustomUser)
class User(ModelAdmin):
    list_display = ('username', 'first_name_field', 'last_name_field', 'is_superuser')

    def first_name_field(self, obj):
        if obj.first_name:
            return obj.first_name
        else:
            return 'null'

    def last_name_field(self, obj):
        if obj.last_name:
            return obj.last_name
        else:
            return 'null'


@register(Blog)
class Blog(ModelAdmin):
    # change_form_template = "admin/base_site.html"
    list_display = ('title', 'created_at', 'main_picture', 'category_set', 'is_active_icon', 'status_button')
    list_filter = ('created_at', 'category', 'is_active')
    readonly_fields = ('is_active', 'slug')
    change_form_template = "admin/change_form.html"

    def response_change(self, request, obj):
        if request.POST.get('status'):
            post = models.Blog.objects.filter(id=obj.id).first()
            post.is_active = request.POST.get('status')
            post.save()
            return HttpResponseRedirect("../")
        elif request.POST.get("_view"):
            return redirect('post_view', obj.slug)

        return super().response_change(request, obj)

    def get_urls(self):
        urls = super().get_urls()
        my_url = [
            path('active/<int:id>', self.active),
            path('canceled/<int:id>', self.canceled),
        ]
        return urls + my_url

    def active(self, request, id):
        post = models.Blog.objects.filter(id=id).first()
        post.is_active = models.Blog.Active.active
        post.save()
        return HttpResponseRedirect('../')

    def canceled(self, request, id):
        post = models.Blog.objects.filter(id=id).first()
        post.is_active = models.Blog.Active.canceled
        post.save()
        return HttpResponseRedirect('../')

    def category_set(self, obj: Blog):
        l = []
        for i in obj.category.all():
            # l.append(f"""<a href="">{i}</a>""")
            l.append(
                f'''<a style="font-weight:bold;text-decoration:none;" href="{reverse('admin:apps_category_change', args=(i.pk,))}">{i.name}</a>''')

        return format_html(', '.join(l))

    def is_active_icon(self, obj):
        data = {
            'pending': '<i class="fas fa-circle-notch fa-spin"></i>',
            'active': '<i class="fa-solid fa-check" style="color: green; font-size: 1em;margin-top: 8px; margin: auto;"></i>',
            'canceled': '<i class="fa-solid fa-circle-xmark"  style="color: red; font-size: 1em;margin-top: 8px; margin: auto;"></i>'
        }
        return format_html(data[obj.is_active])

    is_active_icon.short_description = 'status'

    Blog.status_button.short_description = 'Chose status'


@admin.register(Coment)
class Comment(ModelAdmin):
    list_display = ('author', 'blog')


@admin.register(Category)
class Category(ModelAdmin):
    list_display = ('name',)
    exclude = ('slug',)


@admin.register(Message)
class Message(ModelAdmin):
    list_display = ('message', 'author', 'written_at')
    readonly_fields = ('author', 'message',)
    list_filter = ('written_at',)

    def author(self, obj):
        return obj.username
