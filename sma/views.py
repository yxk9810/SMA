#-*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import json
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence


# Create your views here.
def index(request):
	    return render(request, 'index.html', {})

def dataset(request):
	    return render(request, 'dataset.html', {})

def paper(request):
	    return render(request, 'paper.html', {})
def about(request):
	    return render(request, 'about.html', {})


def keywords(request):
	if request.method =='GET':
		text = request.GET.get('data', '');
		tr4w = TextRank4Keyword()
		tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
		return  HttpResponse(json.dumps(tr4w.get_keywords(20, word_min_len=1)))
