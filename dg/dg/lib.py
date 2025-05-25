"""
conv_v2.1.py
created: 2024.04.10
author: WSD
"""
import re # библиотека регулярных выражений
import sys, os # библиотека системных функций
# from openpyxl import load_workbook
from json import dumps
import json
import uuid as id
from colorama import Fore, Back
import traceback
from inspect import currentframe, getframeinfo
from copy import deepcopy
import dg.color


def printc(name,*vals, **kwargs):
    sep = ''
    color = Fore.YELLOW
    if 'color' in kwargs and kwargs['color'].upper() in dir(Fore): # проверяем наличие атрибута
        color = getattr(Fore, kwargs['color'].upper()) # получаем значение атрибута
    print( '\033[1m' + color + name + ': ' + sep + '\033[0m' + Fore.RESET, *vals)


# функции отладки
def dump(name='',val=None, indent=2, **kwargs):
    print(kwargs)
    print('parse' not in kwargs)
    sep = ''
    color = Fore.YELLOW
    if 'color' in kwargs and kwargs['color'].upper() in dir(Fore): # проверяем наличие атрибута
        color = getattr(Fore, kwargs['color'].upper()) # получаем значение атрибута
    if val.__class__.__name__ == 'dict' or val.__class__.__name__ == 'list':
        if ('parse' in kwargs and not kwargs['parse']) or 'parse' not in kwargs: # 
            val = json.dumps(val, indent=indent, ensure_ascii=False)
        sep = '\n'
    print( '\033[1m' + color + name + ': ' + sep + '\033[0m' + Fore.RESET, val)


def line(): # текущая строка
    ln = sys._getframe().f_lineno
    ln = sys._getframe().f_back.f_lineno
    return str(ln)
def func(): # текущая функция
    cf = currentframe().f_back
    fr = getframeinfo(cf)
    # fl = fr.filename
    ln = fr.lineno
    # if short:
    fn = fr.function
    return str(fn)+'()'
def fileline(short=False, deep=2): # предыдущий вызов. файл, строка
    cf = currentframe().f_back
    if deep > 1: cf = cf.f_back
    fr = getframeinfo(cf)
    fl = fr.filename
    ln = fr.lineno
    if short:
        fn = fr.function
        fl = fl.split('/')[-1]
        return fl + ' : ' + fn + ' : ' + str(ln)
    return fl + ' : ' + str(ln)
def funcline(short=False): # предыдущий вызов, функция, строка
    cf = currentframe().f_back.f_back
    fr = getframeinfo(cf)
    # fl = fr.filename
    ln = fr.lineno
    # if short:
    fn = fr.function
    # fl = fl.split('/')[-1]
    return  fn + '() : ' + str(ln)
def fileline_short(short=False, deep=2): # предыдущий вызов. файл, функция, строка
    cf = currentframe().f_back
    if deep > 1: cf = cf.f_back
    if deep > 2: cf = cf.f_back
    if deep > 3: cf = cf.f_back
    fr = getframeinfo(cf)
    fl = fr.filename
    fn = fr.function
    ln = fr.lineno
    # print(fr)
    # if short:
    fl = fl.split('/')[-1]
    return fl + ' : ' + fn + '() : ' + str(ln)
# / функции отладки


# всомогательные фунции
def isDict(el): return el.__class__.__name__ == 'dict'
def isList(el): return el.__class__.__name__ == 'list'
def isStr(el): return el.__class__.__name__ == 'str'
def strtr(tpl,kwarr): 
    try:
        # dump('arr', 3)
        # dump('kwarr', kwarr)
        if tpl == None or tpl == True or tpl == False  :
            return tpl
        for k, v in kwarr.items():
            if tpl == None or tpl == True or tpl == False  :
                return tpl
            # dump('arr', 4)
            # dump('arr', (tpl, k, v))
            if v is None or v is True or v is False  :
                if tpl == k :
                    tpl = v
            else:
                tpl = tpl.replace(k,v)
        # dump('arr', 5)
    except Exception as e:
        dump(Fore.RED + 'arr', [tpl, kwarr])
    return tpl
def strtra(arr, rep):
    # dump('arr', arr)
    # dump('arr', 1)
    for k, v in arr.items():
        # dump('arr', 2)
        # if v is None or v is True or v is False  :
        #     arr[k] = v
        # else:
        arr[k] = strtr(v, rep)
    # dump('arr', 6)
    return arr
# / всомогательные фунции