# pip3 install mimesniff python-dateutil requests
import os
import requests
import json
import base64
import random
import mimesniff
import re
import urllib.parse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dateutil.parser import parse

class browser:
    def __init__(self):
        self.cookies = {}
        self.headers = {}
        self.set = {}
        self.set2 = {}
        self.auth = ""
        self.basic = False
        self.redirect = ""
        self.onion = False
        self.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
        self.proxy = {'http': 'socks5://127.0.0.1:80', 'https': 'socks5://127.0.0.1:80'}
        self.error_msg = ''
        self.expires = {}
        self.time = 0

    def get(self, url, responseType = ''):
        return self.post(url, {}, responseType)

    def post(self, url, data, responseType = '', files1 = {}, files2 = {}, method = "", nobody = False, callable = False):
        files = {}
        if not method and (data or files1 or files2):
            method = "POST"
        if nobody:
            method = "HEAD"
        if not method:
            method = "GET"
        json = isset2(self.set, "Content-Type") == "application/json" or isset2(self.set2, "Content-Type") == "application/json"
        if not method and data and not json:
            self.set["Content-Type"] = "application/x-www-form-urlencoded"
        boundary = ""
        if not method and (files1 or files2):
            self.set["Content-Type"] = "multipart/form-data"
            boundary = str(rand(10000000,99999999))+str(rand(10000000,99999999))
            self.set["Content-Type"] += "; boundary=------------------------"+boundary
        self.redirect = ""
        for a, b in self.expires.copy().items():
            if self.time>=b:
                del self.cookies[a]
        self.headers = {}
        proxies = {'http': 'socks5://127.0.0.1:80', 'https': 'socks5://127.0.0.1:80'}
        old = {}
        if self.proxy != proxies or not self.onion and ".onion" in url:
            old = requests.proxies
            requests.proxies = self.proxy
        headers = {}
        headers["User-Agent"] = self.UserAgent
        for a, b in self.set.copy().items():
            headers[a] = b
        self.set = {}
        for a, b in self.set2.copy().items():
            if a == "Content-Type" and (data or files1 or files2):
                continue
            headers[a] = b
            self.set[a] = b
        cookies = {}
        if method not in ["OPTIONS","PUT"]:
            for a, b in self.cookies.copy().items():
                if a not in ['samesite','path','domain']:
                    cookies[a] = b
            if (files1 or files2) and not self.auth:
                for a, b in files1.copy().items():
                    DATA = file_get_contents(b)
                    files[a] = (os.path.basename(b), DATA, header_content_parse(mimesniff.what(DATA))["value"])
                for a, b in files2.copy().items():
                    files[a] = (b[0], b[1], header_content_parse(mimesniff.what(b[1]))["value"])
            elif json:
                json=data
                data={}
            if self.auth:
                if self.basic:
                    headers["Authorization"] = "Basic " + base64_encode(self.auth.encode('ascii')).decode('ascii')
                else:
                    headers["Authorization"] = self.auth
        stream = False
        if callable:
            stream = True
        req = ""
        try:
            req = requests.request(method, url, stream=stream, data=data, json=json, headers=headers, cookies=cookies, files=files, verify=False)
            if callable:
                self.parseheader(req);
                for data in req.iter_content(16064):
                    if callable(self, data):
                        break
            requests.proxies = old
            if callable:
                return
        except Exception as e:
            requests.proxies = old
            print("Error: " + str(e));
            return ""
        self.headers["code"] = headers["status"] = req.status_code
        wo = self.parseheader(req, url, data, responseType, files, files2)
        if wo:
            return wo
        if responseType == 'json':
            return json_decode(req.text)
        return req.text

    def parseheader(self, req, url="", data={}, responseType="", files={}, files2={}):
        setcookie = ""
        for r in req.history:
            setcookie += self.setData(r, url)
        setcookie += self.setData(req, url)
        if setcookie:
            self.parse(setcookie)
        A = ""
        if isset(self.headers, "location"):
            A = trim(self.headers["location"])
        if isset(self.headers, "Location"):
            A = trim(self.headers["Location"])
        if A:
            if A.startswith("'") or A.startswith('"'):
                A = A.substr(1, -1)
            if A.startswith('http'):
                C = A
            elif A.startswith('//'):
                C = "http:" + A
            else:
                D = url.split('/');
                C = D[0] + "/" + D[1] + "/" + D[2] + "/"
                if A.startswith('/'):
                    C += A.substr(1)
                else:
                    E = len(A.split('../')) -1
                    A = A.replace("../", "")
                    if A.startswith('./'):
                        A = A.substr(2)
                    F = A.split('/')
                    for G, H in enumerate(D):
                        if G > 2:
                            C += H + "/";
                        if G == len(D) - 2 - E:
                            break;
                    for G, H in enumerate(F):
                        if G != len(F) - 1:
                            C += H + "/";
                        else:
                            C += H;
            url = C;
            if isset2(self.headers, "status") == 307:
                return self.post(url, data, responseType, files1, files2)
            self.redirect = url

    def clean(self):
        self.cookies = {}

    def setData(self, data, url):
        setcookie = ""
        for a, b in data.headers.copy().items():
            if a.lower() == 'set-cookie':
                if setcookie:
                    setcookie+=";"
                for b in b.split(','):
                    if ' secure;' in b or b[len(b)-7:] == ' secure':
                        if 'ttps:' not in url:
                            continue;
                    setcookie+=" "+b
            elif a.lower() == 'date':
                self.time = strtotime(b)
            elif a.lower() == 'content-disposition' or a.lower() == 'content-type':
                self.headers[a] = header_content_parse(b)
            else:
                self.headers[a] = b
        return setcookie

    def setUserAgent(self, UserAgent):
        self.UserAgent = UserAgent

    def parse(self, a):
        for data in a.split(';'):
            data = data.split('=')
            if (len(data)>1):
                data[0] = trim(data[0])
                data[1] = trim(data[1].split(';')[0])
                data0 = data[0].lower()
                if data0 == 'expires':
                    self.expires[last] = strtotime(data[1])
                    if self.time >= self.expires[last]:
                        del self.expires[last]
                        del self.cookies[last]
                        continue
                elif data0 == 'max-age':
                    self.expires[last] = self.time + int(data[1])
                    if self.time >= self.expires[last]:
                        del self.expires[last]
                        del self.cookies[last]
                        continue
                else:
                    self.cookies[data[0]] = data[1]
                if data0 != 'expires' and data0 != 'max-age' and data0 != 'domain' and data0 != 'path' and data0 != 'secure' and data0 != 'samesite':
                    last = data[0]

    def auth(self, url, value, basic=True, data={}):
        self.basic = basic
        self.auth = value
        content = self.get(url, data)
        self.auth = ""
        return content

    def size(self, url, data=[]):
        self.post(url, data, '', {}, {}, "", True);
        if isset(self.headers, "content-length"):
            return int(self.headers["content-length"])
        if isset(self.headers, "Content-Length"):
            return int(self.headers["Content-Length"])
        return 0

    def writefunction(self, url, callable):
        return self.post(url, {}, "", {}, {}, "", False, callable);

def urldecode(url):
    return urllib.parse.unquote(url)
def json_decode(a):
    json.loads(a)
def strtotime(s):
    return int(parse(s).timestamp())
def trim(a,b=" \n\r\t\v\x00"):
    while True:
        c = True
        for d in b:
            if a.endswith(d):
                c = False
                a = a[:-1]
            if a.startswith(d):
                c = False
                a = a[1:]
        if c:
            break
    return a
def isset(a, b):
    c = True
    try:
        a[b]
    except Exception as d:
        c = False
    return c
def isset2(a, b):
    try:
        c = a[b]
    except Exception as d:
        c = False
    return c
def header_content_parse(a):
    b = {}
    for c in list(filter(None, re.split(r';(?=([^"]*"[^"]*")*[^"]*$)', a))):
        d = list(filter(None, re.findall(r'<[^>]+>|[^=]+', c)))
        if isset(d, 1):
            b[trim(d[0], "\"'  \n\t\r")] = trim(d[1], "\"'  \n\t\r")
        else:
            b["value"] = trim(d[0], "\"'  \n\t\r")
    return b
def file_get_contents(a):
    if os.path.exists(a):
        b = open(a, "rb")
        c = b.read()
        b.close()
        return c
def file_put_contents(a, b):
    mkdir(os.path.dirname(os.path.abspath(a)))
    c = open(a, "w") 
    c.write(b)
    c.close()
def base64_encode(a):
    return base64.b64encode(a)
def mkdir(dir):
    os.makedirs(dir, exist_ok=True)
def rand(a,b):
    return random.randint(a,b)