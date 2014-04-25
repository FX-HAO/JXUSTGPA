#!/usr/bin/env python

"""
# 程序:crawler for Jiangxi University of Science and Technology
# 版本:0.1
# 作者:HFX
# 日期:GMT 10:46:352014年 4月 19日 (星期六)
# 语言:Python 3.3
# 操作:输入学号和密码
# 功能:输出成绩的绩点
"""

import urllib.parse
import urllib.request
import http.cookiejar
import html.parser
import re

import py.utility.encodeToUrl

class GPA(object):
    def __init__(self,sno,pwd):
        self.sno=sno
        self.pwd=pwd
        self.cookie=http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        header={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://218.65.107.173/',
            'Connection': 'keep-alive'
            }
        self.headers=header
        self.viewstate='dDwxOTI3MTM3Mjk0Ozs+QfR6JETFyd62h+toLFFXl+4IoBw='

    def login(self):
        postData=urllib.parse.urlencode({
            'TextBox1':self.sno,
            'TextBox2':self.pwd,
            'RadioButtonList1':'学生',
            '__VIEWSTATE':self.viewstate,
            'Button1':''
            }).encode(encoding='gb2312')
        self.req=urllib.request.Request(
            url='http://218.65.107.173/default2.aspx',
            data=postData,
            headers=self.headers
            )
        result=str(self.opener.open(self.req).read(),'gb2312')
        try:
            self.url='http://218.65.107.173/%s' % py.utility.encodeToUrl.codeparse(re.findall('href="xscj_gc.aspx\?xh=.*?"',result)[0].replace('href=','').replace('"','').strip(),'gb2312')
        except IndexError as e:
            self.result='Incorrect username or password.'

    def main(self):
        self.req=urllib.request.Request(
            url=self.url,
            headers=self.headers
            )
        result=str(self.opener.open(self.req).read(),'gb2312')
        self.viewstate=re.findall('"__VIEWSTATE" value=".*?"',result)[0].replace('"__VIEWSTATE" value=','').replace('"','')

    def GPA(self):
        postData=urllib.parse.urlencode({
            '__VIEWSTATE':self.viewstate,
            'ddlXN':'',
            'ddlXQ':'',
            'Button2':'在校学习成绩查询',
            '__EVENTTARGET':'',
            '__EVENTARGUMENT':''
            }).encode(encoding='gb2312')
        self.req=urllib.request.Request(
            url=self.url,
            headers=self.headers,
            data=postData
            )
        result=str(self.opener.open(self.req).read(),'gb2312')
        reg='<td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td>'
        regex=re.compile(reg)
        result=re.findall(regex,result)
        for i in range(len(result)):
            result[i]=result[i].replace('<td>','').split('</td>')
        self.result=result

    def getGPA(self):
        self.login()
        if hasattr(self,'result'):
            return
        self.main()
        self.GPA()

def main():
    while(True):
        sno=input('Please enter your student number: ')
        pwd=input('Please enter your password: ')
        student=GPA(sno,pwd)
        student.getGPA()
        if student.result != 'Incorrect username or password.':
            for eachLine in student.result:
                print('%-40s %6s %6s %6s' % (eachLine[3],eachLine[6],eachLine[7],eachLine[8]))
        else:
            print(student.result)
        operator=input('u wanna try again? (Y/N):')
        if not operator.lower().startswith('y'):
            break

if __name__ == '__main__':
    main()
