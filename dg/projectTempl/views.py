from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
# from .models import Book, Author, BookInstance, Genre
from .models import *
from .models import \
    TemplateModel, WorkTypeModel, VuzModel, TplFileModel, \
    StyleModel, ParagraphModel, FontModel, FontModificationModel, FontTypefaceModel
# from .forms import UploadFileForm

from django.core.mail import send_mail
from .forms import LoginForm, Templateform, DateSelectorWidget
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from dg.lib import dump, printc
from django.conf import settings

messages = {}
def mess(mess, request, _type='success'):
    uid = request.user.id
    if not uid in messages:
        messages[uid] = []
    messages[uid].append({'type':_type, 'mess':mess})

def _404View(request):
    """
    404 page template
    """
    context = {
        'django': 'the web framework for perfectionists with deadlines',
        'home_link':'/',
        'home_title':'Home',
    }
    return render(request, '404.html', context=context)

def index(request):
    """View function for home page of site."""

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")

    # Generate counts of some of the main objects
    num_books = TemplateModel.objects.all().count()
    num_instances = WorkTypeModel.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = WorkType.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = TplFileModel.objects.count()

    context = {
        'django': 'the web framework for perfectionists with deadlines',
        'num_books': num_books,
        'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'home_link':'/',
        'home_title':'Home',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login.html', context=context)

def logoutView(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def loginView(request):
    """View function for home page of site.
    https://docs.djangoproject.com/en/5.0/topics/forms/
    https://forum.djangoproject.com/t/form-template-name-issue-templatenotfound/11451/4
    Try placing that form template in your app/templates/common directory,
    where app is the app containing that form.

    authentication system
    https://docs.djangoproject.com/en/5.0/topics/auth/default/
    """

    mess = ''
    messClass = 'success'
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect("/")

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # rendered_form = form.render("form_login.html")
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            u = None
            user = None
            try:
                user = authenticate(username=form.cleaned_data['login_name'],
                                    password=form.cleaned_data['login_pass'])
                dump('user', user)
                u = User.objects.get(username=form.cleaned_data['login_name'])
                dump('u', u)
            except Exception as e:
                dump('user', e)
            dump('form.cleaned_data', form.cleaned_data)
            # redirect to a new URL:
            if user is not None:
                # A backend authenticated the credentials
                login(request, user)
                mess = 'Вы успешно залогинены'
                messClass = 'success'
                # return HttpResponseRedirect("/login/")
            else:
                # No backend authenticated the credentials
                mess = 'Не верные данные'
                messClass = 'warning'
                # return HttpResponseRedirect("/login/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        # rendered_form = form.render("form_login.html")

    # ***************
    # Generate counts of some of the main objects
    num_books = TemplateModel.objects.all().count()
    num_instances = WorkTypeModel.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = WorkType.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = TplFileModel.objects.count()

    context = {
        # "form": rendered_form,
        "form": form,
        "mess": mess,
        "messClass": messClass,
        'django': 'the web framework for perfectionists with deadlines',
        'num_books': num_books,
        'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'home_link':'/',
        'home_title':'Home',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login.html', context=context)

def contact(request):
    """View function for home page of site."""

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["sender"]
            cc_myself = form.cleaned_data["cc_myself"]

            recipients = ["info@example.com"]
            if cc_myself:
                recipients.append(sender)

            send_mail(subject, message, sender, recipients)
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    # ***************
    # Generate counts of some of the main objects
    num_books = TemplateModel.objects.all().count()
    num_instances = WorkTypeModel.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = WorkType.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = TplFileModel.objects.count()

    context = {
        "form": form,
        'django': 'the web framework for perfectionists with deadlines',
        'num_books': num_books,
        'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'home_link':'/',
        'home_title':'Home',
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'login.html', context=context)


def handle_uploaded_file(f):
    pathdir = settings.MEDIA_ROOT
    with open('media/uploads/'+f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def getTemplate(tplid=0):
    '''
    Получить данные шаблона
    '''
    # dump('tplid', tplid, color='green')
    filesCou = 0
    if tplid==0:
        data = {
        'tplid': tplid,
        'field_bottom': 0,
                'filesCou': filesCou,
                'pagenumbers':'tc',# 'fill_content':'content',
                'text_align_0': 'w',
                'text_align_1': 'w',
                'text_align_2': 'w',
                'text_align_3': 'w',
                'text_align_4': 'w',
                'text_align_5': 'w',
                'text_align_6': 'w',
                'img_align_img': 'w',
                'text_align_img': 'w',
            }
        return data
    
    data = {
        'tplid': tplid,
        'field_bottom': 0,
            'pagenumbers':'tc',# 'fill_content':'content',
            'text_align_0': 'w',
            'text_align_1': 'w',
            'text_align_2': 'w',
            'text_align_3': 'w',
            'text_align_4': 'w',
            'text_align_5': 'w',
            'text_align_6': 'w',
            'img_align_img': 'w',
            'text_align_img': 'w',
        }

    # =========================
    
    if tplid > 0:
        filesCou = TplFileModel.objects.filter(tpl_id=int(tplid)).all().count()
    data['filesCou'] =  filesCou

    # =========================
    
    # tpl = TemplateModel(id=tplid)
    tpl = TemplateModel.objects.filter(id=tplid).first()
    if tpl:
        data['tplid'] = tpl.id
        data['templateName'] = tpl.templateName
        data['worktype'] = tpl.workType

        data['field_top'] = tpl.fieldtop
        data['field_bottom'] = tpl.fieldbottom
        data['field_left'] = tpl.fieldleft
        data['field_right'] = tpl.fieldright
        data['orientation'] = tpl.orientation
        data['pagenumbers'] = tpl.pagenumber
        data['img_align_img'] = tpl.imgalign
        data['fill_content'] = tpl.fill_content
        data['fill_char'] = tpl.fill_char

        # dump('tpl', tpl, color='green')
        # dump('tpl data', dict(data), color='green')

        # w = WorkTypeModel.objects.filter(tpl_id=tplid);
        # if w: data['worktype'] = w.all()[0].id;

        w = VuzModel.objects.filter(tpl_id=tplid);
        if w: data['vuz'] = w.all()[0].name;

        # =========================

        data = getTemplateBlock(tpl,'defaulttext',data, '0')
        data = getTemplateBlock(tpl,'title_1',data, '1')
        data = getTemplateBlock(tpl,'title_2',data, '2')
        data = getTemplateBlock(tpl,'title_3',data, '3')
        data = getTemplateBlock(tpl,'table_title',data, '4')
        data = getTemplateBlock(tpl,'table_text',data, '5')
        data = getTemplateBlock(tpl,'literature_list',data, '6')
        data = getTemplateBlock(tpl,'images',data, 'img')

    # =========================
    # printc('getTemplate data', data, color='green')

    return data


def getTemplateBlock(tpl, modName, data, dataSufix):
    # printc('getTemplateBlock modName', modName, color='green')
    # printc('getTemplateBlock data', data, color='green')

    # =========================
    
    # m = StyleModel.objects.filter(tpl_id=tplid, name= 'defaulttext').first();
    m = StyleModel.objects.filter(tpl=tpl, name=modName).first();
    if m:
        # data['vuz'] = w.all()[0].name;

        # printc('StyleModel', m)
        w = ParagraphModel.objects.filter(style=m).first();
        if w:
            data['text_align_' + dataSufix] = w.alignment;
            data['marg_left_' + dataSufix] = w.indentationFromLeft;
            data['marg_right_' + dataSufix] = w.indentationFromRight;
            data['first_line_' + dataSufix] = w.firstLine;
            data['inter_before_' + dataSufix] = w.intervalBefore;
            data['inter_after_' + dataSufix] = w.intervalAfter;
            data['inter_bitwin_' + dataSufix] = w.lineSpacing;
            # data['vuz'] = w.prohibitionHangingLines;
            # data['vuz'] = w.doNotTearFromNext;
            # data['vuz'] = w.doNotTearParagraph;
            # data['vuz'] = w.fromNexPage;

        f = FontModel.objects.filter(style=m).first();
        if f:
            data['fontName_' + dataSufix] = f.fontname;
            data['sizes_' + dataSufix] = f.size;
            # data['marg_left_' + dataSufix] = f.color;

            ft = FontTypefaceModel.objects.filter(font=f).first();
            if ft:
                ftdata = []
                if ft.bold: ftdata.append('b')
                if ft.underlined: ftdata.append('u')
                if ft.italic: ftdata.append('i')
                data['font_style_' + dataSufix] = ftdata;

            fm = FontModificationModel.objects.filter(font=f).first();
            if fm:
                ftdata = []
                if fm.strikethrow: ftdata.append('str')
                if fm.superscript: ftdata.append('sup')
                if fm.subscript: ftdata.append('sub')
                if fm.uppercase: ftdata.append('upp')
                data['font_modif_' + dataSufix] = ftdata;

    # =========================
    return data

def tplUpdate(request,tplid,form):
    '''
    обновление или создание шаблона
    '''
    # dump( 'request.POST', dict(request.POST) )
    # print( 'Templateform', dict(form.cleaned_data) )
    # dump( 'request.FILES', dict(request.FILES) )

    data = form.cleaned_data
    tplid = data['tplid']
    created = False

    tpl = TemplateModel.objects.filter(id=tplid).first()
    if not tpl:
        tpl = TemplateModel()
        created = True

    tpl.templateName = data['templateName']
    tpl.workType = data['worktype']

    tpl.fieldtop = data['field_top']
    tpl.fieldbottom = data['field_bottom']
    tpl.fieldleft = data['field_left']
    tpl.fieldright = data['field_right']
    tpl.orientation = data['orientation']
    tpl.pagenumber = data['pagenumbers']
    tpl.imgalign = data['img_align_img']
    tpl.fill_content = data['fill_content']
    tpl.fill_char = data['fill_char']
    tpl.save()
    tplid = tpl.id

    if created:
        mess(f'добавлен шаблон с id:{tplid}', request)
    else:
        mess(f'изменён шаблон с id:{tplid}', request)

    # data['templateName'] = tpl.templateName
    # form.cleaned_data['tplid'] = tplid # not work

    # print( 'Templateform', templateform.cleaned_data )
    # dump( 'request.FILES', request.FILES )
    # handle_uploaded_file(request.FILES["file"])
    # for each in templateform.cleaned_data['file']:
    #     dump( 'FILES each', each )
    #     ...
    #     # handle_uploaded_file(each)
    
    files = form.cleaned_data["file_field"]
    for f in files:
        # dump( 'FILES file_field', f )
        ...  # Do something with each file.

        # instance = TplFileModel(file=request.FILES["file_field"])
        instance = TplFileModel(file=f, tpl=tpl)
        instance.save()
    

    d_vuz = data['vuz']
    m_vuz = VuzModel.objects.filter(tpl_id=tplid).first()
    if m_vuz: m_vuz.name = d_vuz; m_vuz.save();
    else: VuzModel(name=d_vuz, tpl=tpl).save()

    # dt = data['vuz']
    # model = WorkTypeModel.objects.filter(tpl_id=tplid).first()
    # if model: model.name = dt; model.save();
    # else: WorkTypeModel(name=d_vuz, tpl=tpl).save()
    # WorkTypeModel(name=f, tpl=tpl).save()

    # =========================

    # d = data['vuz']
    # sizes_0 = forms.ChoiceField(choices=sizes, required=False, widget=wSelect, label="Размер")
    # fontName_0 = forms.ModelChoiceField(queryset = fonts, required=False,label="Шрифт")
    # font_style_0 = forms.ChoiceField(choices=font_style_, required=False, widget=wCheck, label="Стиль шрифта")
    # font_modif_0 = forms.ChoiceField(choices=font_modif_, required=False, widget=wRadio, label="Модификация шрифта")
    # text_align_0 = forms.ChoiceField(choices=text_align_, required=False, widget=wRadio, label="Выравнивание")
    
    # inter_bitwin_0 = forms.IntegerField(label="Междустрочный", required=False, initial=0, widget=widgetNum)
    # inter_before_0 = forms.IntegerField(label="Перед", required=False, initial=0, widget=widgetNum)
    # inter_after_0 = forms.IntegerField(label="После", required=False, initial=0, widget=widgetNum)

    # marg_left_0 = forms.IntegerField(label="Слева", required=False, initial=0, widget=widgetNum)
    # marg_right_0 = forms.IntegerField(label="Справа", required=False, initial=0, widget=widgetNum)
    # first_line_0 = forms.IntegerField(label="Первая строка", required=False, initial=0, widget=widgetNum)

    # =========================

    tplUpdateBlock(tpl,'defaulttext',data, '0')
    tplUpdateBlock(tpl,'title_1',data, '1')
    tplUpdateBlock(tpl,'title_2',data, '2')
    tplUpdateBlock(tpl,'title_3',data, '3')
    tplUpdateBlock(tpl,'table_title',data, '4')
    tplUpdateBlock(tpl,'table_text',data, '5')
    tplUpdateBlock(tpl,'literature_list',data, '6')
    tplUpdateBlock(tpl,'images',data, 'img')

    # =========================

    return tplid


def tplUpdateBlock(tpl, modName, data, dataSufix):
    # printc('tplUpdateBlock', modName, color='green')

    # get StyleModel
    # modName = 'defaulttext'
    # mod = StyleModel.objects.filter(tpl_id=tplid, name=modName).first()
    mod = StyleModel.objects.filter(tpl=tpl, name=modName).first()
    modData = {}
    modData['tpl'] = tpl
    modData['name'] = modName
    modData['tab1'] = '0'
    modData['tab2'] = '0'
    if mod:
        dump('StyleModel '+ modName, 'exists')
        # mod.name = modName;
    # else: 
    if not mod:
        dump('StyleModel '+ modName, 'new')
        mod = StyleModel(**modData)
    for k, v in modData.items():
        setattr(mod, k, v)
    # print(mod)
    # dump('StyleModel ', mod)
    mod.save();
    style_id = mod.id

    # Paragraf
    paragrafData = {}
    paragrafData['style'] = mod
    paragrafData['alignment'] = data['text_align_' + dataSufix]

    if not dataSufix == 'img':
        paragrafData['indentationFromLeft'] = data['marg_left_' + dataSufix]
        paragrafData['indentationFromRight'] = data['marg_right_' + dataSufix]
        paragrafData['firstLine'] = data['first_line_' + dataSufix]
    else:
        paragrafData['indentationFromLeft'] = 0
        paragrafData['indentationFromRight'] = 0
        paragrafData['firstLine'] = 0

    paragrafData['intervalBefore'] = data['inter_before_' + dataSufix]
    paragrafData['intervalAfter'] = data['inter_after_' + dataSufix]
    paragrafData['lineSpacing'] = data['inter_bitwin_' + dataSufix]
# prohibitionHangingLines doNotTearFromNext doNotTearParagraph fromNexPage
    paragrafData['prohibitionHangingLines'] = 0
    paragrafData['doNotTearFromNext'] = 0
    paragrafData['doNotTearParagraph'] = 0
    paragrafData['fromNexPage'] = 0
    # paragraf = ParagraphModel.objects.filter(style_id=style_id).first()
    paragraf = ParagraphModel.objects.filter(style=mod).first()
    if not paragraf:
        paragraf = ParagraphModel(**paragrafData)
    for k, v in paragrafData.items():
        setattr(paragraf, k, v)
    # dump('paragraf ', '')
    # print(paragraf)
    paragraf.save();

    # font
    fontData = {}
    fontData['style'] = mod
    fontData['fontname'] = data['fontName_' + dataSufix]
    fontData['size'] = data['sizes_' + dataSufix]
    fontData['color'] = '#000'
    font = FontModel.objects.filter(style=mod).first()
    if not font:
        font = FontModel(**fontData)
    for k, v in fontData.items():
        setattr(font, k, v)
    font.save();
    fontid = font.id

    fontName = data['fontName_' + dataSufix]
    if fontName:
        fn = FontNameModel.objects.filter(id=fontName.id).first()
        printc('fontName', fn)
        fused = fn.used
        fn.used = fused + 1
        fn.save()

    # font type
    fontData = {}
    fontData['font'] = font
    fontData['bold'] = int( 'b' in data['font_style_' + dataSufix] )
    fontData['underlined'] = int( 'u' in data['font_style_' + dataSufix])
    fontData['italic'] = 'i' in data['font_style_' + dataSufix]
    fonttype = FontTypefaceModel.objects.filter(font=font).first()
    if not fonttype:
        fonttype = FontTypefaceModel(**fontData)
    for k, v in fontData.items():
        setattr(fonttype, k, v)
    fonttype.save();

    # font modif
    fontData = {}
    fontData['font'] = font
    fontData['strikethrow'] = int( 'str' in data['font_modif_' + dataSufix] )
    fontData['superscript'] = int( 'sup' in data['font_modif_' + dataSufix])
    fontData['subscript'] = 'sub' in data['font_modif_' + dataSufix]
    fontData['uppercase'] = 'upp' in data['font_modif_' + dataSufix]
    fonttype = FontModificationModel.objects.filter(font=font).first()
    if not fonttype:
        fonttype = FontModificationModel(**fontData)
    for k, v in fontData.items():
        setattr(fonttype, k, v)
    fonttype.save();

    # =========================

def tplnew(request,tplid=0):
    """создание или изменение шаблона."""

    if not request.user.is_authenticated:        return HttpResponseRedirect("/login/")
    uid = request.user.id
    if not uid in messages:
        messages[uid] = []

    files = []
    filesCou = 0
    fonts = FontNameModel.objects.all().order_by('-used')
    # Generate counts of some of the main objects
    tpls_cou = TemplateModel.objects.all().count()
    num_instances = WorkTypeModel.objects.all().count()
    if tplid > 0:
        files = TplFileModel.objects.filter(tpl_id=int(tplid)).all()
        filesCou = files.count()

    # Available books (status = 'a')
    # num_instances_available = WorkType.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = TplFileModel.objects.count()

    # tsform = DateSelectorWidget(request.POST)

    if request.method == "POST":
        templateform = Templateform(request.POST, request.FILES)
        # dump( 'request.POST', request.POST )
        if templateform.is_valid():
            tplid = tplUpdate(request,tplid,templateform)
            # templateform.cleaned_data['tplid'] = tplid
            templateform.tplid = tplid
            return HttpResponseRedirect(reverse('tplget', args=[tplid]))
        else:
            mess('have some error', request)
    else:
        data = getTemplate(tplid)
        templateform = Templateform(initial=data)
    templateform.files =  files
    templateform.filesCou =  filesCou

    # forms = {}
    # forms = []
    # for fnum in range(0,2):
    #     # forms['form_num_'+str(fnum)] = fnum
    #     # forms['form_'+str(fnum)] = Templateform(request.POST)
    #     forms.append(fnum)
    #     forms.append(Templateform(request.POST))
        
    pagename = 'Новый шаблон'
    if tplid: 
        data = getTemplate(tplid)
        if 'templateName' in data:
            pagename = '{} [ID:{}]'.format( data['templateName'], data['tplid'] )

    # mess(f'filesCou {filesCou}', request)
    # dump('templateform.file_field',templateform.file_field)
    # printc('templateform.file_field',templateform.fields ['file_field'])
    context = {
        'messages': messages[uid],
        'pagename': pagename,
        'action': '/tplnew/',
        # 'tsform':tsform,
        'fonts':fonts,
        # 'forms':forms,
        'Templateform': templateform,
        'filesCou': filesCou,
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
        'cols': (0,1,2,3),
        'tpls_cou': tpls_cou,
        'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    messages[uid] = []

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'newItem.html', context=context)

def templateList(request,page=1,limit=100):
    """список шаблонов"""
    tpls_cou = TemplateModel.objects.all().count()
    tplfrom = int(page-1) * int(limit)
    tpls = TemplateModel.objects.all().order_by('-id')[tplfrom:tplfrom+int(limit)] 
    filesCou = {}
    tlist = []
    for tpl in tpls:
        id = tpl.id
        fcou = TplFileModel.objects.filter(tpl_id=id).all().count()
        filesCou[id] = fcou
        tlist.append( {'tpl':tpl,"files":fcou} )

    pageCou = tpls_cou//limit
    if tpls_cou%limit:
        pageCou +=1
    # pageCou *=10
    pages = [(p, p) for p in range(1,pageCou+1)]

    pagePrevDis = False
    pageNextDis = False
    if page <= 1: pagePrevDis = True
    if page >= pageCou: pageNextDis = True
    pagePrev = page - 1
    pageNext = page + 1
    if pagePrev < 1: pagePrev = 1
    if pageNext > pageCou: pageNext = pageCou

    sli = 5
    if page > sli and page < pageCou - sli: pages = pages[page - sli - 1:]
    # pages = pages[:sli*2 + 1:]
    if page < pageCou - sli : pages = pages[:sli*2 + 1:]
    else: pages = pages[-(sli*2+1)::]


    pagename = 'Список шаблонов'
    context = {
        'pagename': pagename,
        'action': '/tplnew/',

        'pages': pages,
        'pagePrev': pagePrev,
        'pagePrevDis': pagePrevDis,
        'pageNext': pageNext,
        'pageNextDis': pageNextDis,
        'limit': limit,
        'currentPage': page,
        'pageCou': pageCou,
        'sli': sli,

        # 'tpls' = tlist,
        'tpls_cou': tpls_cou,
        'tplsList': tlist,
        'filesCou': filesCou,
    }
    return render(request, 'template-list.html', context=context)

def tplstatistic(request):
    """View function for home page of site."""

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login/")

    # Generate counts of some of the main objects
    num_books = TemplateModel.objects.all().count()
    num_instances = WorkTypeModel.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = WorkType.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = TplFileModel.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        # 'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def removeFile(request, fid):
    if not request.user.is_authenticated:        return HttpResponseRedirect("/login/")
    file = TplFileModel.objects.get(pk=fid)
    if file:
        tplid = file.tpl_id
        file.delete()
        return HttpResponseRedirect(reverse('tplget', args=[tplid]))
    return HttpResponseRedirect(reverse('templateList'))

class BookListView(generic.ListView):
    # model = Book
    ...