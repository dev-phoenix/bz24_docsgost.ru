from django import forms
from .models import *
from datetime import date

from .models import \
    TemplateModel, WorkTypeModel, VuzModel, TplFileModel, \
    StyleModel, ParagraphModel, FontModel, FontModificationModel, FontTypefaceModel


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = {day: day for day in range(1, 32)}
        months = {month: month for month in range(1, 13)}
        years = {year: year for year in [2018, 2019, 2020]}
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split("-")
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return "{}-{}-{}".format(year, month, day)


class LoginForm(forms.Form):
    """
    Login form
    Add class to form field Django ModelForm
    https://stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    """

                    # form_login.html
    template_name =  "form_login.html"
    login_name = forms.CharField(label="Логин", max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "login"}))
    login_pass = forms.CharField(label="Пароль", max_length=100,
                                widget=forms.TextInput(attrs={'placeholder': "password", 'type': "password"}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            # visible.field.widget.attrs['placeholder'] = ''


class ContactForm(forms.Form):
    '''
    example form
    '''
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


def initGroup(field,group):
    field.column = group['column']
    field.group = group['group']
    field.template = group['template']

# class Templateform(forms.ModelForm):
class Templateform(forms.Form):
    '''
    Template form
    '''
    # Reserved.objects.filter(client=client_id).order_by('-check_in')
# 

    template_name =  "form_template.html"
    sizes = {'10':10, '11':11, '12':12, '14':14, '16':16}
    sizes = [10, 11, 12, 14, 16]

    # # Ориентация 2 пункта:  
    # orient = {'album':'Альбомная', 'book':'Книжная'}
    # # номера страниц - 7 пунктов: 
    # pgnums = {'no':'без номера', 'bc':'снизу поцентру', 'bl':'снизу слева', 'br':'снизу справа', 'tc':'сверху поцентру', 
    # 'tl':'сверху слева', 'tr':'сверху справа'}

    # # tts = DateSelectorWidget()
    # # field1 = forms.DateField(widget=DateSelectorWidget())
    # templateName = forms.CharField(label="Имя шаблона", max_length=100, required=False,
    #                             widget=forms.TextInput(attrs={'placeholder': "Шаблон"}))
    

    
    # =========================
    
    # =========================
    
    wSelect = forms.Select(attrs={'placeholder': "", "class":"22",'data-issel':'1'})
    widgetNum = forms.NumberInput(attrs={'placeholder': ""})
    wRadio = forms.RadioSelect
    wCheck = forms.CheckboxInput
    wCheck = forms.CheckboxSelectMultiple

    # =========================

    _workTypeDt = WorkTypeModel.objects.all().order_by('id')

    # id шаблона
    tplid = forms.IntegerField(label="tpl ID", required=False, initial=0,
        widget=forms.HiddenInput)
    # filesCou = 0
    
    templateName = forms.CharField(label="Имя шаблона", max_length=256, 
                                widget=forms.TextInput(attrs={'placeholder': "Имя шаблона", 'type': "text"}))
    
    vuz = forms.CharField(label="Вуз", max_length=256, required=False,
                                widget=forms.TextInput(attrs={'placeholder': "Вуз", 'type': "text"}))
    worktype = forms.ModelChoiceField(queryset = _workTypeDt, required=False, widget=wSelect,
                                    label="Тип работы",initial=1)
    
    # =========================

    orient = [('album','Альбомная'), ('book','Книжная')]
    pgnums =    [('no', 'без номера'),
                ( 'bc', 'снизу поцентру'),
                ( 'bl', 'снизу слева'), 
                ( 'br', 'снизу справа'), ('tc', 'сверху поцентру'), 
        ('tl', 'сверху слева'), ( 'tr', 'сверху справа')]

    orientation = forms.ChoiceField(choices=orient, required=False, widget=wSelect,label="Ориентация")
    pagenumbers = forms.ChoiceField(choices=pgnums, required=False, widget=wSelect,label="Номера страниц")

    # =========================
    sizes = [('10',10), ('11',11), ('12',12), ('14',14), ('16',16)]
    # fonts = FontNameModel.objects.all().order_by('-family','name','-used')
    sizes = FontSizeModel.objects.all().order_by('weight')
    sizes = [(s.size, s.size) for s in sizes]
    fonts = FontNameModel.objects.all().order_by('-used','name','-family')
    
    # # CHOICES = FontNameModel.objects.all().order_by('-used')
    # field = forms.ChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)

    field_top = forms.FloatField(label="Верхнее", required=False, initial=0, widget=widgetNum)
    field_bottom = forms.FloatField(label="Нижнее", required=False, initial=0, widget=widgetNum)
    field_left = forms.FloatField(label="Левое", required=False, initial=0, widget=widgetNum)
    field_right = forms.FloatField(label="Правое", required=False, initial=0, widget=widgetNum)


    # def group1(self):
    #     return filter(lambda x: x.group == 1, self.fields.values())

    # def group1(self):
    #     return filter(lambda x: x.group == 1, self.fields.values())
    # def group3(self):
    #     return filter(lambda x: 'group' in x and x.group == 3, self.fields.values())

    # =========================

    font_style_ = (('b', '<b>Ж</b>'),('i', '<i>К</i>'),('u', '<u>Ч</u>'),)
    font_modif_ = (('str', 'Strikethrow'),('sup', 'Superscript'),('sub', 'Subscript'),('upp', 'Uppercase'),)
    text_align_ = (('l', 'Слева'),('c', 'По центру'),('r', 'Справа'),('w', 'По ширине'),)

    title_0 = 'Основной текст'
    sizes_0 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_0 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_0 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_0 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_0 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_0 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_0 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_0 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_0 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_0 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_0 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)

    # =========================

    title_1 = 'Заголовок 1'
    sizes_1 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_1 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_1 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_1 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_1 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_1 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_1 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_1 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_1 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_1 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_1 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================

    title_2 = 'Заголовок 2'
    sizes_2 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_2 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_2 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_2 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_2 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_2 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_2 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_2 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_2 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_2 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_2 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================

    title_3 = 'Заголовок 3'
    sizes_3 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_3 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_3 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_3 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_3 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_3 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_3 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_3 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_3 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_3 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_3 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================
    # "заголовок таблицы" и "текст в таблице", а также "Список литературы"

    title_4 = 'Заголовок таблицы'
    sizes_4 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_4 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_4 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_4 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_4 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_4 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_4 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_4 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_4 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_4 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_4 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================

    title_5 = 'Текст в таблице'
    sizes_5 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_5 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_5 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_5 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_5 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_5 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_5 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_5 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_5 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_5 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_5 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================

    title_6 = 'Список литературы'
    sizes_6 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_6 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_6 = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_6 = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_6 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    inter_bitwin_6 = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_6 = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_6 = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    marg_left_6 = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    marg_right_6 = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    first_line_6 = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================

    # title_GNUM = 'Основной текст'
    # sizes_GNUM = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    # fontName_GNUM = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    # font_style_GNUM = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    # font_modif_GNUM = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    # text_align_GNUM = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    # inter_bitwin_GNUM = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    # inter_before_GNUM = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    # inter_after_GNUM = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    # marg_left_GNUM = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    # marg_right_GNUM = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    # first_line_GNUM = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)
    
    # =========================
    
    # =========================
    
    fill_content_ = (('contents', 'Оглавление'),('content', 'Содержание'),)
    fill_content = forms.ChoiceField(choices=fill_content_, required=False, widget=wRadio, label="Заполнение",initial='contents')
    fill_char_ = (('', 'no'),('_', '_'),('.', '.'),)
    fill_char = forms.ChoiceField(choices=fill_char_, required=False, widget=wSelect, label="Заполнение",initial='.')
    # fontName_1.group = 1

    # =========================

    title_img = 'Рисунки'
    sizes_img = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    fontName_img = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    font_style_img = forms.MultipleChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    font_modif_img = forms.MultipleChoiceField(choices=font_modif_, required=False, widget=wCheck, label="Модификация шрифта")
    text_align_img = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    img_align_img = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание img")
    
    inter_bitwin_img = forms.FloatField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    inter_before_img = forms.FloatField(label="Перед", required=False, initial=0, widget=widgetNum)
    inter_after_img = forms.FloatField(label="После", required=False, initial=0, widget=widgetNum)

    # marg_left_img = forms.FloatField(label="Слева", required=False, initial=0, widget=widgetNum)
    # marg_right_img = forms.FloatField(label="Справа", required=False, initial=0, widget=widgetNum)
    # first_line_img = forms.FloatField(label="Первая строка", required=False, initial=0, widget=widgetNum)

    # =========================

    # file = forms.FileField(label="Файл", required=False)
    file_field = MultipleFileField(label="Файлы  ", required=False)
    
    # =========================
    # Test Template 236

    # column = 1
    # group = 'style'
    # field_top.group = group
    # field_bottom.group = group
    # template = 'style'
    # field_top.template = template
    # field_bottom.template = template
    # group = 'style-fill'
    # group = 'style-imgs'
    # group = 'style-file'
    # field_left.group = group
    # field_right.group = group
    # template = 'style-file'
    # field_left.template = template
    # field_right.template = template

    initGroup(field_top,{'column':1, 'group':'1', 'template':'style'})
    initGroup(field_bottom,{'column':1, 'group':'1', 'template':'style'})
    initGroup(field_left,{'column':2, 'group':'2', 'template':'style-fill'})
    initGroup(field_right,{'column':2, 'group':'2', 'template':'style-fill'})

    initGroup(fill_content,{'column':3, 'group':'3', 'template':'style-fill'})
    initGroup(fill_char,{'column':3, 'group':'3', 'template':'style-fill'})

    group_1={}
    group_1['a']=field_top
    group_1['b']=field_bottom
    group_1['c']=field_left
    group_1['d']=field_right

    group_fill={}
    group_fill['content']=fill_content
    group_fill['char']=fill_char
    group_fill = group_fill.items()

    fields_groups = {
        'style_layout':{
            'title':'Макет страницы',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'style_0':{
            'title':'Основной текст',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'style_1':{
            'title':'Заголовок 1',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'style_2':{
            'title':'Заголовок 2',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'style_3':{
            'title':'Заголовок 3',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'style_fill':{
            'title':'Заполнение',
            'contents':'1',
            'content':'0',
            'fill':'',
        },
        'style_imgs':{
            'title':'Рисунки',
            'font':'',
            'size':'',
            'align':'',
            'left':'',
            'right':'',
            'first':'',
        },
        'files':[],
        'files':[
            {
                'title':'Файл',
                'font':'',
                'size':'',
                'align':'',
                'left':'',
                'right':'',
                'first':'',
            }
        ],
    }

    def __init__(self, *args, **kwargs):
        super(Templateform, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            if 'data-issel' in visible.field.widget.attrs and visible.field.widget.attrs['data-issel'] == '1':
                visible.field.widget.attrs['class'] = 'form-select'
            # visible.field.widget.attrs['placeholder'] = '''data-issel'
            ...
        
        # print(self)
        # if self.fields['tplid'].value > 0:
        #     self.fields['filesCou'] = TplFileModel.objects.all().count()
        
        
        # self.group_fill={}
        # self.group_fill['content']=self.fill_content
        # self.group_fill['char']=self.fill_char
        # # self.group_fill = group_fill.items()

    # class Meta:
    #     model = StyleModel
    #     fields = ["name", "tpl"]