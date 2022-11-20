
class browser:
  def __init__(self):
    import requests
    self.requests = requests
    self.cookies = {}
    self.headers = {}
    self.Auth = ""
    self.UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.43"
    import json
    self.json = json
    import base64
    self.base64 = base64
    self.useSock = True;

  def get(self, url, responseType = ''):
    return self.post(url, {}, responseType)

  def post(self, url, post, responseType = ''):
    self.headers = {}
    requests = self.requests
    if ".onion" in url and self.useSock:
        requests = requests.session()
        requests.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
    headers = {}
    headers["User-Agent"] = self.UserAgent
    cookies = {}
    if self.Auth:
        headers["Authorization"] = "Basic " + self.base64.b64encode(this.Auth.encode('ascii')).decode('ascii')
    else:
        for key, value in self.cookies.copy().items():
            if key not in ['expires','path','domain']:
                cookies[key] = value
    try:
        if len(post):
            requests = requests.post(url, post, headers=headers, cookies=cookies)
        else:
            requests = requests.get(url, headers=headers, cookies=cookies)
    except Exception as e:
        print("Error: " + e);
        return ""
    headers = {}
    headers["code"] = headers["status_code"] = requests.status_code
    setcookie = ""
    for r in requests.history:
        setcookie += self.setData(r, url)
    setcookie += self.setData(requests, url)
    if setcookie:
        self.parse(setcookie);
    if responseType == 'json':
        return self.json.loads(requests.text)
    return requests.text

  def clean(self):
    self.cookies = {}

  def setData(self, data, url):
    setcookie = ""
    for key, value in data.headers.copy().items():
        if key.lower() == 'set-cookie':
            for value in value.split(','):
                if setcookie:
                  setcookie+=";"
                if ' secure;' in value or value[len(value)-7:] == ' secure':
                  if 'ttps:' not in url:
                    continue;
                setcookie+=" "+value
        else:
            self.headers[key] = value
    return setcookie

  def setUserAgent(self, UserAgent):
    self.UserAgent = UserAgent

  def parse(self, a):
    for data in a.split(';'):
        data = data.split('=')
        if (len(data)>1):
            self.cookies[data[0].strip()] = data[1].split(';')[0].strip()

  def auth(self, url, value):
    self.Auth = value
    content = self.get(url)
    self.Auth = ""
    return content

test = browser()
content = test.post("https://blablaland.fun/login", {'login': '', 'password': ''})
content = test.get("https://blablaland.fun")