#!/user/bin/env python
#coding=utf-8
import json
import requests
from Proxy.tools.spiderip.FreeProxy import SpiderFreeIp

# @project : ProxyPool
# @author  : kalifun
# @file   : Verification.py
# @ide    : PyCharm
# @time   : 2019/6/20 11:18

class CheckIp():
    def __init__(self):
        self.ipdict = SpiderFreeIp().analysis()
        self.addapi = "http://ip.taobao.com/service/getIpInfo.php?ip="
        self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def CheckAddress(self,ip):
        fullurl = self.addapi + ip
        req = requests.get(fullurl,self.headers)
        if req.status_code == 200:
            getdata = req.text
            dataload = json.loads(getdata)
            jsondata = dataload["data"]
            country = jsondata["country"]
            region = jsondata["region"]
            city = jsondata["city"]
            fulladd = country + "-" + region + "-" + city
            isp = jsondata["isp"]
            return fulladd,isp
        else:
            fulladd = 'None'
            isp = 'None'
            return fulladd, isp

    def CheckSpend(self,ip,port):
        try:
            req = requests.get("http://"+ip+":"+port)
            spend = req.elapsed.total_seconds()
            return spend
        except Exception as e:
            spend = "0"
            return spend

    def AddinfotoIp(self):
        ipdic = self.ipdict
        if len(ipdic) == 0:
            print('获取的数据有误')
        else:
            iplist = []
            for ipinfo,httptype in ipdic.items():
                intodic = {}
                splitip = ipinfo.split(":")
                ip = splitip[0]
                port = splitip[1]
                add = self.CheckAddress(ip)
                needspend = self.CheckSpend(ip,port)
                try:
                    ipadd = add[0]
                    isp = add[1]
                except:
                    ipadd = "None"
                    isp = "None"
                print("[x] " + "ip: " + ip + ":" + port + " 地址:" + ipadd + " 运营商: " + isp + "响应速度: " + str(needspend))
                intodic["ip"] = ip
                intodic["port"] = port
                intodic["httptype"] = httptype
                intodic["address"] = ipadd
                intodic["isp"] = isp
                intodic["spend"] = needspend
                iplist.append(intodic)
            return iplist