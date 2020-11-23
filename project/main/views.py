from django.shortcuts import render
from django.http import HttpResponse

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
    return render(request, 'main/index.html')

def login(request):
    return render(request, 'main/login.html')
    
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
            print("KLAS 접근에러: 아이디 입력 란 없음.")
        try:
            driver.execute_script("arguments[0].value='" + kid + "'", ele)
        except:
            print("KLAS 동작에러: 아이디 입력 문제")
            
        ele = is_located_xpath(10,'//*[@id="loginPwd"]')
        if ele == -1:
            print("KLAS 접근에러: 패스워드 입력 란 없음.")
        try:
            driver.execute_script("arguments[0].value='" + kpw + "'", ele)
        except:
            print("KLAS 동작에러: 비밀번호")
        ele = is_located_xpath(10,'/html/body/div[1]/div/div/div[2]/form/div[2]/button')
        if ele == -1:
            print("KLAS 접근에러: 로그인 안됨")
        try:
            ele.click()
        except:
            print("KLAS 동작에러: 로그인 안됨")
        # 과목정보 대기
        eles = is_located_xpaths(10,'//*[@id="appModule"]/div/div[2]/ul/li')
        if eles == -1:
            return render(request, 'main/wrong.html')
        try:
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            subs = soup.select(
                '#appModule > div > div:nth-child(2) > ul > li > div.left'
            )
        except:
            print("KLAS 동작에러: 과목수집 문제")
        # 과목정보 수집
        list_sub = []
        list_code = []
        for tmp in subs:
            tmp = tmp.text.strip().split(' ')
            list_sub.append(tmp[0])
            list_code.append(tmp[1].replace('(', "").replace(')', ""))

        context = {
            'subs':list_sub,
            'codes':list_code,
        }
        return render(request, 'main/register.html', context)
    else:
        return render(request, 'main/register.html')

def testing(request):
    context = {
        'a':['a','b','c'],
        'b':'c',
    }
    return render(request, 'main/test.html', context)
    #return HttpResponse("수집완료-콘솔에")