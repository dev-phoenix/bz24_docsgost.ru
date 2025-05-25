from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import *
import json

admin.site.unregister(Group)
admin.site.site_header = "Админ панель"
admin.site.site_title = "Админ панель"
admin.site.index_title = "Добро пожаловать"

# Register your models here.


### КОНСТРУКТОР АНКЕТЫ ###
class FontSizeModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['size','weight']
    search_fields = ['size','weight']
    list_filter = ['size','weight']

    class Meta:
        model = FontSizeModel

admin.site.register(FontSizeModel, FontSizeModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class FontNameModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['name','family','used']
    search_fields = ['name','family']
    list_filter = ['name','family','used']

    class Meta:
        model = FontNameModel

admin.site.register(FontNameModel, FontNameModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class FontTypefaceModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['bold','underlined','italic','font']
    search_fields = ['bold','underlined','italic','font__style','font']
    list_filter = ['bold','underlined','italic','font__style','font']

    class Meta:
        model = FontTypefaceModel

admin.site.register(FontTypefaceModel, FontTypefaceModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class FontModificationModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['strikethrow','superscript','subscript','uppercase',]
    search_fields = ['strikethrow','superscript','subscript','uppercase']
    list_filter = ['strikethrow','superscript','subscript','uppercase']

    class Meta:
        model = FontModificationModel

admin.site.register(FontModificationModel, FontModificationModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class FontModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['fontname', 'size', 'color'#, 'typeface', 'modification'
                    ]
    search_fields = ['fontname']
    list_filter = ['fontname']

    class Meta:
        model = FontModel

admin.site.register(FontModel, FontModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class ParagraphModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = [
        'alignment', 'indentationFromLeft', 'indentationFromRight',
        'firstLine', 'intervalBefore', 'intervalAfter',
        'lineSpacing', 'prohibitionHangingLines', 'doNotTearFromNext',
        'doNotTearParagraph', 'fromNexPage']
    # search_fields = ['title_ru', 'text_ru', 'category_ru']
    # list_filter = ['category_ru', 'the_end']

    class Meta:
        model = ParagraphModel

admin.site.register(ParagraphModel, ParagraphModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class StyleModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    # list_display = ['font', 'paragraph', 'tab1', 'tab2']
    # search_fields = ['font', 'paragraph']
    # list_filter = ['font', 'paragraph']

    # def templateName(self, obj):
    #     for sub in TemplateModel.objects.all():
    #         if sub.id == obj.tpl_id:
    #             return sub.templateName
    # templateName.short_description = 'Шаблон'

    # list_display = ['name', 'tpl', 'templateName', 'tab1', 'tab2']
    list_display = ['name', 'tpl', 'tab1', 'tab2']
    # list_display = ['name', 'tpl_id', 'tab1', 'tab2']
    # list_display = ['name', 'tab1', 'tab2']
    search_fields = [ 'name', 'tab1', 'tab2']
    list_filter = [ 'name', 'tab1', 'tab2']
    # list_display_links = None

    class Meta:
        model = StyleModel

admin.site.register(StyleModel, StyleModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class TplFileModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['id','tpl','file']
    search_fields = ['tpl','file']
    list_filter = ['id','tpl','file']

    class Meta:
        model = TplFileModel

admin.site.register(TplFileModel, TplFileModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class VuzModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    list_display = ['id', 'name','tpl']
    search_fields = ['id', 'name','tpl']
    list_filter = ['name']

    class Meta:
        model = VuzModel

admin.site.register(VuzModel, VuzModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class WorkTypeModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    # list_display = ['id', 'name','tpl']
    # search_fields = ['id', 'name','tpl']
    # list_filter = ['name']


    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    list_filter = ['name']


    class Meta:
        model = WorkTypeModel

admin.site.register(WorkTypeModel, WorkTypeModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###


### КОНСТРУКТОР АНКЕТЫ ###
class TemplateModelAdmin(admin.ModelAdmin):
    """Модель категории"""

    # list_display = [
    #                 'vuz', 'workType', 'templateName'

    #                 # 'tpl_caption1', 'caption2', 'defaultText',
    #                 # 'content', 'tableName', 'tableCaption',
    #                 # 'tableText', 'pictureName', 'picture',
    #                 # 'formula',
    #                 #   'file',
    #                 ]
    # search_fields = ['vuz', 'workType', 'templateName']
    # list_filter = ['vuz', 'workType', 'templateName']

    fields_list = []
    fields_list.append('id')
    fields_list.append('templateName')
    fields_list.append('workType')
    fields_list.append('fieldtop')
    fields_list.append('fieldbottom')
    fields_list.append('fieldleft')
    fields_list.append('fieldright')
    fields_list.append('orientation')
    fields_list.append('pagenumber')
    fields_list.append('imgalign')
    fields_list.append('fill_content')
    fields_list.append('fill_char')

    list_display = fields_list
    search_fields = ['templateName']
    list_filter = ['id', 'templateName']

    class Meta:
        model = TemplateModel

admin.site.register(TemplateModel, TemplateModelAdmin)
### КОНСТРУКТОР АНКЕТЫ ###
