from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .forms import TitleChangeListForm
from reviews.models import Title, Genre, Category


# class TitleChangeList(ChangeList):

#     def __init__(self, request, model, list_display,
#         list_display_links, list_filter, date_hierarchy,
#         search_fields, list_select_related, list_per_page,
#         list_max_show_all, list_editable, model_admin):

#         super(TitleChangeList, self).__init__(request, model,
#             list_display, list_display_links, list_filter,
#             date_hierarchy, search_fields, list_select_related,
#             list_per_page, list_max_show_all, list_editable, 
#             model_admin)

#         # these need to be defined here, and not in MovieAdmin
#         self.list_display = ['action_checkbox','pk', 'genres']
#         #self.list_display = ['action_checkbox','pk','name','year', 'description', 'genres', 'category']
#         self.list_display_links = ['name']
#         self.list_editable = ['genre']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description', 'category') #'genres', 
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'

    # def get_changelist(self, request, **kwargs):
    #     return TitleChangeList

    # def get_changelist_form(self, request, **kwargs):
    #     return TitleChangeListForm

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Category)
class Categorydmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
