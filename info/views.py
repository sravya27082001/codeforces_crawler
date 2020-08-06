from django.shortcuts import render,redirect
from  django.http import HttpResponse
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pandas import json_normalize
# Create your views here.

def get_user_info(Handle):

    html_content=requests.get(f'https://codeforces.com/profile/{Handle}').text
    return html_content

def home(request):

    return render(request,'info/home.html')

def about(request):
    Handle=request.GET.get('Handle')
    content=requests.get(f'https://codeforces.com/api/user.info?handles={Handle}').json()['result']
    rating_changes=requests.get(f'https://codeforces.com/api/user.rating?handle={Handle}').json()['result']
    user_status=requests.get(f'https://codeforces.com/api/user.status?handle={Handle}').json()['result']
    tdict = json_normalize(user_status)
    res={}
    res=dict(tdict['verdict'].value_counts())
    solved=[]
    for i in range(len(tdict)):
        if tdict['verdict'][i]=='OK':
            solved.append(tdict['problem.index'][i])

    df=pd.DataFrame(solved,columns=['problem_levels'])
    df.sort_values('problem_levels',axis=0,inplace=True)
    res1={}
    res1=dict(df['problem_levels'].value_counts())

    rank=content[0]['rank']
    handle=content[0]['handle']
    rating=content[0]['rating']
    maxRating=content[0]['maxRating']
    maxRank=content[0]['maxRank']
    li=[]
    for i in rating_changes:
        li.append(i['newRating']);
    li2=[]
    li1=[]

    for i,j in res.items():
        li2.append(j)

    for i,j in res1.items():
        li1.append(j)




    context={
    'rank':rank,
    'handle':handle,
    'rating':rating,
    'maxRating':maxRating,
    'maxRank':maxRank,
    'rating_changes':rating_changes,
    'res':res,
    'li1':li1,
    'li':li,
    'li2':li2,
    'res1':res1
    }
    return render(request,'info/about.html',context)


def contest_list(request):
    contests=requests.get('https://codeforces.com/api/contest.list?gym=false').json()['result']
    li=[]
    for r in contests:
        if r['phase']=='BEFORE':
            li.append(r);
        else:
            break

    return render(request,'info/contests.html',{'li':li})


def verdict(request,Handle):
    user_status=requests.get('https://codeforces.com/api/user.status?handle={Handle}').json()['result']
    tdict = json_normalize(user_status)
    result={}
    result=dict(tdict['verdict'].value_counts())


    return render(request,'info/verdicts.html',{'result':result})
