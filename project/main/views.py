from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone

from .models import Post, Subject, Blog

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def is_located_xpath(ttime,xpath):
    try:
        element = WebDriverWait(driver, ttime).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return driver.find_element_by_xpath(xpath)
    except:
        return -1
def is_located_xpaths(ttime,xpath):
    try:
        element = WebDriverWait(driver, ttime).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return driver.find_elements_by_xpath(xpath)
    except:
        return -1

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
driver = webdriver.Chrome('chromedriver.exe', options=options)

# Create your views here.
def index(request):
    return redirect('/main/0')

def nav(request, nav_id):
    context={'n'+str(nav_id):'1',}
    return render(request, 'main/index.html', context)

def post(request, board_id, post_id):
    detail = get_object_or_404(Post, pk=post_id)
    context = {
        'post':detail,
        'board_id':board_id,
    }
    return render(request, 'main/post/post.html', context)

def subject(request, code):
    blogs = Blog.objects.filter(code=code)
    context = {
        'blogs':blogs,
        'code':code,
    }
    return render(request, 'main/subject/list.html', context)

def subwrite(request, code):
    if request.method == "POST":
        blog = Blog()
        blog.title = request.POST.get('title')
        blog.body = request.POST.get('body')
        blog.code = code
        blog.name = ""
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/main/subject/' + code)
    else:
        context = {
            'code':code,
        }
        return render(request, 'main/subject/write.html', context)

def subpost(request, code, post_id):
    detail = get_object_or_404(Blog, pk=post_id) 
    context = {
        'post':detail,
        'code':code,
    }#여까지 OK
    return render(request, 'main/subject/post.html', context)

def board(request, board_id):
    #posts = Post.objects.order_by('-pub_date')
    
    posts = Post.objects.filter(board=board_id)
    context = {
        'posts':posts,
        'board_id':board_id,
        'n1':'1',
    }
    if board_id == 1:
        context['title']='자유게시판'
        context['body']='자유게시판은 실명제로 교내외 활동과 관련된 정보 공유 및 개인의 의견을 담은 게시물을 올릴 수 있습니다.'
    elif board_id == 2:
        context['title']='비밀게시판'
        context['body']='익명으로 소통하는 게시판입니다.'
    elif board_id == 3:
        context['title']='건의게시판'
        context['body']='커뮤니티에 관한 불만사항, 건의사항, 개선아이디어 등 커뮤니티와 관련된 모든 사항을 자유롭게 올려주세요.'
    return render(request, 'main/post/list.html', context)

def write(request, board_id):
    if request.method == "POST":
        post = Post()
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.pub_date = timezone.datetime.now()
        post.board = board_id
        post.save()
        return redirect('/main/board/' + str(board_id))
    else:
        context = {
            'board_id':board_id,
        }
        return render(request, 'main/post/write.html', context)

def loginform(request):
    return render(request, 'main/account/login.html')

def join(request):
    return render(request, 'main/account/join.html')

def welcome(request):
    return render(request, 'main/account/welcome.html')

def logout(request):
    auth.logout(request)
    return redirect('main:index')
    
def testing(request, name):
    context = {
        {'name':name,}
    }
    return render(request, 'main/test.html', context)
    #return HttpResponse("수집완료-콘솔에")

def login(request):
    if request.method == "POST":
        id = request.POST['id']
        pw = request.POST['pw']
        user = auth.authenticate(request, username=id, password=pw)
        if user is not None:
            auth.login(request, user)
            return redirect('main:index')
        else:
            context = {'txt':'아이디 또는 비밀번호를 확인해주세요.'}
            return render(request, 'main/account/login.html', context)
    return redirect('main:loginform')
    
def register(request):
    if request.method == "POST":
        kid = request.POST['kid']
        kpw = request.POST['kpw']

        # 초기화
        driver.get('https://klas.kw.ac.kr/usr/cmn/login/Logout.do')
        driver.get('https://klas.kw.ac.kr/')
        # 로그인
        ele = is_located_xpath(10,'//*[@id="loginId"]')
        if ele == -1:
            context = {
                'txt':"KLAS 접근에러: 아이디 입력 란 안뜸.",
            }
            return render(request, 'main/repeat/err.html', context)
        try:
            driver.execute_script("arguments[0].value='" + kid + "'", ele)
        except:
            context = {
                'txt':"KLAS 동작에러: 아이디 입력문제.",
            }
            return render(request, 'main/repeat/err.html', context)
            
        ele = is_located_xpath(10,'//*[@id="loginPwd"]')
        if ele == -1:
            context = {
                'txt':"KLAS 접근에러: 비밀번호 입력 란 안뜸.",
            }
            return render(request, 'main/repeat/err.html', context)
        try:
            driver.execute_script("arguments[0].value='" + kpw + "'", ele)
        except:
            context = {
                'txt':"KLAS 동작에러: 비밀번호",
            }
            return render(request, 'main/repeat/err.html', context)
        ele = is_located_xpath(10,'/html/body/div[1]/div/div/div[2]/form/div[2]/button')
        if ele == -1:
            context = {
                'txt':"KLAS 접근에러: 확인 버튼을 연속해서 누른 경우 발생합니다. 한 번만 누르고 기다려주세요.",
            }
            return render(request, 'main/repeat/err.html', context)
        try:
            ele.click()
        except:
            context = {
                'txt':"KLAS 접근에러: 로그인 안됨.",
            }
            return render(request, 'main/repeat/err.html', context)
        
        # 과목정보 대기
        eles = is_located_xpaths(18,'//*[@id="appModule"]/div/div[2]/ul/li')
        if eles == -1: # 과목정보 수집을 못한다면 비밀번호 오류
            return render(request, 'main/account/wrong.html')

        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            subs = soup.select(
                '#appModule > div > div:nth-child(2) > ul > li > div.left'
            )
        except:
            context = {
                'txt':"KLAS 동작에러: 과목수집 안됨.",
            }
            return render(request, 'main/repeat/err.html', context)

        # 과목정보 수집
        list_sub = []
        list_code = []
        for tmp in subs:
            tmp = tmp.text.strip().split(' ')
            list_sub.append(tmp[0])
            list_code.append(tmp[1].replace('(', "").replace(')', ""))

        user = User.objects.create_user(
            username=kid,password=kpw
        )

        for i in range(len(list_sub)):
            subject = Subject()
            subject.user = user
            subject.name = list_sub[i]
            subject.code = list_code[i]
            subject.save()

        auth.login(request,user)      
        return redirect('main:welcome')
        #return render(request, 'main/register.html', context)
    else:
        return render(request, 'main/account/register.html')