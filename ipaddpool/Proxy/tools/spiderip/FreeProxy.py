#!/user/bin/env python
#coding=utf-8
import requests
from bs4 import BeautifulSoup
# @project : ProxyPool
# @author  : kalifun
# @file   : FreeProxy.py
# @ide    : PyCharm
# @time   : 2019/6/20 10:07

class SpiderFreeIp():
    def __init__(self):
        self.baseurl = "http://ip.jiangxianli.com/"

    def Readurl(self):
        try:
            headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
            req = requests.get(self.baseurl,headers)
            if req.status_code == 200:
                return req.text
        except :
            return "连接失败"

    def analysis(self):
        html = self.Readurl()
        soup_string = BeautifulSoup(html,"html.parser")
        button_str = soup_string.findAll(attrs={"class":"btn-speed"})
        addresspool = {}
        for data_list in button_str:
            ip = data_list.get('data-ip')
            port = data_list.get('data-port')
            dataprotocol = data_list.get('data-protocol')
            if (ip == None) or (port == None) or (ip == "") or (port == "") :
                pass
            else:
                addresspool[ip+":"+port] = dataprotocol
        return addresspool