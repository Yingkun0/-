# -*- coding:utf-8 -*-
import urllib,urllib2,re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from html_tool import *  #自己创建的工具类，处理内容的非文字部分

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()


class BDTB:
    def __init__(self,baseURL,seeLZ):
        self.baseURL = baseURL
        self.seeLZ = '?see_lz='+str(seeLZ)
        self.tool = Tool()
        self.floor = 1
        self.defaultTitle = u'百度贴吧'
        user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self.headers = {'User-Agent':user_agent}        
        print "Hello"

    def getPage(self,pageNum):
        url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)#pageNum帖子的页数
        request = urllib2.Request(url,headers=self.headers)
        response = urllib2.urlopen(request)
        Con = response.read()  
        return Con        
        
    def getTitle(self):        
        Con = self.getPage(1)
        pat = re.compile('<h3 class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>',re.S)
        title = re.search(pat,Con)
        return title.group(1).decode('utf-8')
        
    def getAuthor(self):
        Con = self.getPage(1)
        pat = re.compile('<div class="louzhubiaoshi.*?author="(.*?)">',re.S)
        author = re.search(pat,Con)
        return author.group(1).decode('utf-8')
        
    def getReply_num(self):
        Con = self.getPage(1)
        pat = re.compile('<li class="l_reply_num".*?<span class="red">(.*?)</span>',re.S)
        reply_num = re.search(pat,Con)
        return reply_num.group(1).decode('utf-8')
        
    def getContent(self,page):
       # Con = self.getPage(1)
        pat = re.compile('<div id="post_content_.*?">(.*?)</div>',re.S)
        items = re.findall(pat,page)
        contents = []
        for item in items:
            #print floor,u'楼--------------------------------------------------------------\n'
            content = self.tool.replace(item).decode('utf-8').strip()
            contents.append(content)
        return contents

    def setFileTitle(self,title):
        if title is not None:
            self.file = open(r'd:\1\\'+title+'.txt','w+')
        else:
            self.file = open(self.defaultTitle+'.txt','w+')

    def writeData(self,content):
        for item in content:
            floorline ='\n'+str(self.floor)+'--------------------------------------------------------------\n'
            self.file.write(floorline)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getReply_num()
        title = self.getTitle()
        self.setFileTitle(title)
        if pageNum == None:
            print 'URL写入无效，请重试'
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1,int(pageNum)+1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        #出现写入异常
        except IOError,e:
            print "写入异常，原因" + e.message
        finally:
            print "写入任务完成"
 


if __name__ == '__main__':
    print u'请输入帖子代号'
    baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))    
    bdtb = BDTB(baseURL,1)
    seeLZ = raw_input(u"是否只获取楼主发言，是输入1，否输入0\n")
    bdtb.start()

        


