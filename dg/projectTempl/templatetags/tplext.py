
# https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/#howto-writing-custom-template-filters
# sites/docsgost.ru/dg/projectTempl/templatetags/tplext.py

from django import template
from django.templatetags.static import static
from django.urls import reverse
from ..models import \
    TemplateModel, WorkTypeModel, VuzModel, TplFileModel, \
    StyleModel, ParagraphModel, FontModel, FontModificationModel, FontTypefaceModel

from dg.lib import printc

register = template.Library()
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, "")
def lower(value):  # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()
def _dir(value): printc('_dir', dir(value)); return dir(value)
def _print(value): printc('_print', value); "printc('_print 2')"; return ''
def _printdir(value): printc('_printdir'); print(dir(value)); return ''
def _type(value): printc('_type'); return type(value)
def _str(value): return str(value)
def _class(value): 
    printc('_printdir', value.__class__.__name__);
    return value.__class__.__name__
def dump(value):  # Only one argument.
    """Converts a string into all lowercase"""
    # out = dir(value)
    # if value.__class__.__name__ == 'dict':
    out = {}
    for k,v in dict(value).items():
        out[k] = v
    return out
def val(v,k): return v[k]
def fname(v): 'print(dir(v))'; print(str(v).split('/')[-1:]); return ''.join(str(v).split('/')[-1:])
def workType(tplid):
    # print('tplid',tplid);
    w= WorkTypeModel.objects.filter(tpl_id=tplid);
    if w:
        # print('len(w.all()) ',len(w.all()))
        return w.all()[0].name;
    else: return ''
def vuz(tplid):
    w= VuzModel.objects.filter(tpl_id=tplid);
    if w: return w.all()[0].name;
    else: return ''

def hasget(val):
    printc('hasget class',val.__class__.__name__)
    printc('hasget type',type(val))
    return _type(val)

# register.filter("cut", cut)
# register.filter("lower", lower)

register.filter("static", static)
register.filter("url", reverse)
register.filter("dir", _dir)
register.filter("print", _print)
register.filter("printdir", _printdir)
register.filter("type", _type)
register.filter("str", _str)
register.filter("class", _class)
register.filter("dump", dump)
register.filter("val", val)
register.filter("fname", fname)
register.filter("workType", workType)
register.filter("vuz", vuz)
register.filter("hasget", hasget)


# @register.filter(name="url")
# def url(value):
#     return reverse(value)+'?hi'

# @register.filter(name="cut")
# def reverse(value, arg):
#     return value.replace(arg, "")

# @register.filter(name="cut")
# def cut(value, arg):
#     return value.replace(arg, "")


# @register.filter
# def lower(value):
#     return value.lower()


@register.inclusion_tag("results.html")
def show_results(poll=''):
    # choices = poll.choice_set.all()
    choices = ['a'+poll,'b'+poll,'c'+poll]
    return {"choices": choices}


@register.inclusion_tag("link.html", takes_context=True)
def jump_link(context):
    return {
        "link": context["home_link"],
        "title": context["home_title"],
    }


# {% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}
@register.inclusion_tag("my_template.html")
def my_tag(a, b, *args, **kwargs):
    warning = kwargs["warning"]
    profile = kwargs["profile"]
    ...
    return ...