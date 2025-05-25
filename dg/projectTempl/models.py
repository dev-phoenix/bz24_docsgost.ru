# from django.db import models

# Create your models here.
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models

from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

'''
template
    style
        font
            fontTypeface
            fontModification
        paragraph
    file
    vus
    worktype
'''
'''
templateModel
    StyleModel
        FontModel
            FontTypefaceModel
            FontModificationModel
        ParagraphModel
    FileModel
    VuzModel
    WorktypeModel

'''




class WorkTypeModel(models.Model):
    name = models.CharField(max_length=256, help_text='Work type name')
    # tpl = models.ForeignKey(TemplateModel, on_delete=models.SET_NULL,
    #                         blank=True, null=True, verbose_name='Шаблон' )

    class Meta:
        db_table = 'worktype'
        ordering = ['-id']
        verbose_name = "тип работы"
        verbose_name_plural = "Типы работ"

    def __str__(self):
        return self.name


# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
class TemplateModel(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    # my_field_name = models.CharField(max_length=20, help_text='Enter field documentation')
    templateName = models.CharField(max_length=256, help_text='Template naem')
    # caption1 = models.ForeignKey( StyleModel, related_name='tpl_caption1', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='caption1')
    # caption2 = models.ForeignKey( StyleModel, related_name='tpl_caption2', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='caption2')
    # defaultText = models.ForeignKey( StyleModel, related_name='tpl_defaultText', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='defaultText')
    # content = models.ForeignKey( StyleModel, related_name='tpl_content', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='content')
    
    # tableName = models.ForeignKey( StyleModel, related_name='tpl_tableName', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='tableName')
    # tableCaption = models.ForeignKey( StyleModel, related_name='tpl_tableCaption', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='tableCaption')
    # tableText = models.ForeignKey( StyleModel, related_name='tpl_tableText', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='tableText')
    # pictureName = models.ForeignKey( StyleModel, related_name='tpl_pictureName', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='pictureName')
    # picture = models.ForeignKey( StyleModel, related_name='tpl_picture', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='picture')
    
    # formula = models.ForeignKey( StyleModel, related_name='tpl_formula', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='formula')
    # file = models.ForeignKey(TplFileModel, verbose_name='file', on_delete=models.SET_NULL, blank=True, null=True)
    workType = models.ForeignKey(WorkTypeModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Вид работы', )
    # vuz = models.ForeignKey(VuzModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Вуз' )
    # …
    fieldtop = models.FloatField(help_text='', verbose_name='Поле верхнее')
    fieldbottom = models.FloatField(help_text='', verbose_name='Поле нижнее')
    fieldleft = models.FloatField(help_text='', verbose_name='Поле левое')
    fieldright = models.FloatField(help_text='', verbose_name='Поле правое')
    orientation = models.CharField(max_length=256, help_text='', verbose_name='Ориентация')
    pagenumber = models.CharField(max_length=256, help_text='', verbose_name='Номер страницы')
    imgalign = models.CharField(max_length=8, help_text='', verbose_name='Выравнивание рисунка')
    fill_content = models.CharField(max_length=32, help_text='', verbose_name='Содержание')
    fill_char = models.CharField(max_length=8, help_text='', verbose_name='Заполнение')

    # Metadata
    class Meta:
        db_table = 'template'
        ordering = ['-id']
        verbose_name = "шаблон"
        verbose_name_plural = "Шаблоны"

    def __str__(self):
        return self.templateName

    # Methods
    # def get_absolute_url(self):
    #     """Returns the URL to access a particular instance of MyModelName."""
    #     return reverse('model-detail-view', args=[str(self.id)])

    # def __str__(self):
    #     """String for representing the MyModelName object (in Admin site etc.)."""
    #     return self.templateName


class StyleModel(models.Model):
    name = models.CharField(max_length=256, help_text='Style name')
    tpl = models.ForeignKey(TemplateModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Шаблон' )
    # font = models.ForeignKey( FontModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='font')
    # paragraph = models.ForeignKey( ParagraphModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='paragraph')
    tab1 = models.FloatField(help_text='tab1')
    tab2 = models.CharField(max_length=256, help_text='tab2')

    class Meta:
        db_table = 'style'
        ordering = ['-id']
        verbose_name = "стиль"
        verbose_name_plural = "Стили"

    def __str__(self):
        return self.name


class FontNameModel(models.Model):
    name = models.CharField(max_length=128, help_text='Font name', default='', verbose_name='Имя шрифта')
    family = models.CharField(max_length=64, help_text='Font family', default='', verbose_name='Семейство шрифта')
    used = models.IntegerField(help_text='Использован', default=0, verbose_name='Частота использования')

    class Meta:
        db_table = 'fontname'
        ordering = ['-id']
        verbose_name = "шрифт"
        verbose_name_plural = "Список шрифтов"

    def __str__(self):
        return self.name


class FontSizeModel(models.Model):
    size = models.IntegerField(default=0, help_text='Size', verbose_name='Размер')
    weight = models.IntegerField(default=0, help_text='Weight', verbose_name='Вес')
    class Meta:
        db_table = 'fontsize'
        ordering = ['weight']
        verbose_name = "размер"
        verbose_name_plural = "Размеры шрифтов"


class FontModel(models.Model):
    fontname = models.ForeignKey(FontNameModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Font name' )
    style = models.ForeignKey(StyleModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Стиль' )
    # name = models.CharField(max_length=256, help_text='Font name')
    size = models.IntegerField(help_text='Size')
    color = models.CharField(max_length=256, help_text='Color')
    # align = models.CharField(max_length=8, help_text='Alignment')
    # typeface = models.ForeignKey( FontTypefaceModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='FontTypeface')
    # modification = models.ForeignKey( FontModificationModel, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='FontModification')

    class Meta:
        db_table = 'font'
        ordering = ['-id']
        verbose_name = "шрифт"
        verbose_name_plural = "Шрифты"

    def __str__(self):
        return str(self.fontname)


class FontTypefaceModel(models.Model):
    bold = models.IntegerField( help_text='Вуз')
    underlined = models.IntegerField( help_text='Вуз')
    italic = models.IntegerField( help_text='Вуз')
    font = models.ForeignKey(FontModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Стиль' )

    class Meta:
        db_table = 'fonttypeface'
        ordering = ['-id']
        verbose_name = "тип шрифта"
        verbose_name_plural = "Типы шрифтов"

    # def __str__(self):
    #     return self.name


class FontModificationModel(models.Model):
    strikethrow = models.IntegerField( help_text='Strikethrow')
    superscript = models.IntegerField( help_text='Superscript')
    subscript = models.IntegerField( help_text='Subscript')
    uppercase = models.IntegerField( help_text='Uppercase')
    font = models.ForeignKey(FontModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Стиль' )

    class Meta:
        db_table = 'fontmodification'
        ordering = ['-id']
        verbose_name = "модификация"
        verbose_name_plural = "Модификации"

    # def __str__(self):
    #     return self.name


class ParagraphModel(models.Model):
    style = models.ForeignKey(StyleModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Стиль' )
    alignment = models.CharField(max_length=256, help_text='alignment')
    indentationFromLeft = models.FloatField(help_text='indentationFromLeft')
    indentationFromRight = models.FloatField(help_text='indentationFromRight')
    firstLine = models.FloatField(help_text='firstLine')
    intervalBefore = models.FloatField(help_text='intervalBefore')
    
    intervalAfter = models.FloatField(help_text='intervalAfter')
    lineSpacing = models.FloatField(help_text='lineSpacing')

    prohibitionHangingLines = models.BooleanField(help_text='prohibitionHangingLines')
    doNotTearFromNext = models.BooleanField(help_text='doNotTearFromNext')
    doNotTearParagraph = models.IntegerField(help_text='doNotTearParagraph')
    
    fromNexPage = models.IntegerField(help_text='fromNexPage')

    class Meta:
        db_table = 'paragraph'
        ordering = ['-id']
        verbose_name = "параграф"
        verbose_name_plural = "Параграфы"

    # def __str__(self):
    #     return self.alignment
    

class TplFileModel(models.Model):
    file = models.FileField(upload_to="media/uploads/", verbose_name='file')
    tpl = models.ForeignKey(TemplateModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Шаблон' )

    class Meta:
        db_table = 'tplfile'
        ordering = ['-id']
        verbose_name = "файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return str(self.file)


class VuzModel(models.Model):
    name = models.CharField(max_length=256, help_text='Вуз')
    tpl = models.ForeignKey(TemplateModel, on_delete=models.SET_NULL,
                            blank=True, null=True, verbose_name='Шаблон' )

    class Meta:
        db_table = 'vuz'
        ordering = ['-id']
        verbose_name = "вуз"
        verbose_name_plural = "Вузы"

    def __str__(self):
        return self.name