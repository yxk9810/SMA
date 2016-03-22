#-*- encoding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass
import MySQLdb
import codecs
import datetime
from textrank4zh import TextRank4Keyword, TextRank4Sentence

Users={
    'test01':'test01',
    'test02':'test02',
    'test03':'test03',
    'test04':'test04',
    'test05':'test05'
}
# Create your views here.
def index(request):
	    return render(request, 'index.html', {})

def dataset(request):
	    return render(request, 'dataset.html', {})

def paper(request):
	    return render(request, 'paper.html', {})
def about(request):
	    return render(request, 'about.html', {})
def signin(request):
	    return render(request, 'signin.html', {})
def annotation(request,questionid):
        if  not  'username' in request.session:
           	return render(request, 'signin.html', {})
        else:
            db = MySQLdb.connect(user='root', db='annotation', passwd='root', host='10.141.250.170',charset="utf8")
            cursor = db.cursor()
            cursor.execute('SELECT max(id) as icount  FROM questions ')
            res = cursor.fetchone()
            cursor = db.cursor()
            num = res[0]
            if int(questionid)<=num:
                cursor.execute('SELECT * FROM questions where id='+questionid)
                res = cursor.fetchone()
                desc = cursor.description
                cursor.close()
                dict = {}
                for (name, value) in zip(desc, res) :
                    dict[name[0]] = value
                dict['next'] = dict['id']+1 if questionid< num else -1 
                return render(request, 'annotation.html',dict)
            else:
                print num,questionid
def label(request):
    db = MySQLdb.connect(user='root', db='annotation', passwd='root', host='10.141.250.170',charset="utf8")
    cursor = db.cursor()
    questionid = request.GET.get('questionid', '-1');
    answer     = request.GET.get('answer','-1')
    add_userlog = ("INSERT INTO userlog "
              "(username, questionid, answer, createtime) "
              "VALUES (%(username)s, %(questionid)s, %(answer)s, %(createtime)s)")
    data_salary = {
      'questionid': questionid,
      'answer': answer,
      'username': 'tomorrow',
      'createtime':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    cursor.execute(add_userlog, data_salary)
    count  = cursor.rowcount if cursor.rowcount > 0 else 0  
    db.commit
    cursor.close()
    db.close()
    if count:
    	return  HttpResponse(json.dumps({'code':1}))
    else:
    	return  HttpResponse(json.dumps({'code':0}))
"""
user login
"""
def login(request):
    db = MySQLdb.connect(user='root', db='annotation', passwd='root', host='10.141.250.170',charset="utf8")
    cursor = db.cursor()
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username in Users and Users[username] == password:
        request.session['username'] = username
        cursor.execute("SELECT username,max(questionid) FROM userlog where username='"+username+"' group by username ")
        res = cursor.fetchone()
        cursor.close()
        if res==None:
            return HttpResponseRedirect('/annotation/1/')
        else:
            return HttpResponseRedirect('/annotation/'+str((res[1]+1))+'/')
    else:
        return  render(request, 'signin.html', {'error':'用户名或者密码错误!'})

def logout(request):
        del request.session['username']
        return render(request, 'signin.html', {})


def keywords(request):
	if request.method =='GET':
		text = request.GET.get('data', '');
		tr4w = TextRank4Keyword()
		tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
		return  HttpResponse(json.dumps(tr4w.get_keywords(20, word_min_len=1)))
