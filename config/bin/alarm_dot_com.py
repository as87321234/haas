import json
import requests
from requests import Response
from requests.cookies import RequestsCookieJar
from requests.sessions import Session

from bs4 import BeautifulSoup


class AlarmDotCom:

    def __init__(self):
        self.two_factor_authentication_id = ''
        self.big_ip = ''
        self.cookie_jar = ''
        self.BIGipServer_AlarmApplication_Alarm_WEBADC_Alarm_HTTPS = ''
        self.headers = None
        self.cookies = None
        self.session = requests.Session()

    def __str__(self):
        return self.two_factor_authentication_id

    @staticmethod
    def dump_response(ses: Session, res: Response):
        print('--------------------------------------')
        print(ses.params)
        print(res.cookies)
        print(res.headers)
        print()

        # soup = BeautifulSoup(res.content, 'html.parser')
        # print(soup.prettify())

    @staticmethod
    def dump_json(o: object, msg: str):
        print(msg)
        print(json.dumps(o, indent=4, sort_keys=True))

# 
    @staticmethod
    def dump_cookie_jar(cookie_jar: RequestsCookieJar, msg: str):
        print(msg)
        serialized_cookie_dict = ""
        serialized_cookie_dict = json.dumps(dict(cookie_jar))
        dump_json(serialized_cookie_dict, ms)  # --- Correctly serialized CookieJar
        # deserialized_cookie_dict = requests.cookies.cookiejar_from_dict(
        #     json.loads(serialized_cookie_dict))  # --- Successful!

    def login(self):
        print("Login to alarm.com")

        # GET /login?m=logout HTTP/1.1

        header = {
            'Host': 'www.alarm.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            # 'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96”',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.alarm.com/web/system/home',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        self.headers = header

        with self.session as s:
            res = s.get("https://www.alarm.com/login.aspx",
                        headers=header,
                        cookies={},
                        auth=(),
                        )

            self.cookies = res.cookies
            self.headers.update(res.headers)

            self.dump_json(self.headers, "login: dump headers")
            self.dump_cookie_jar(self.cookies, "login: dump cookies")

            AlarmDotCom.dump_response(s, res)

            soup = BeautifulSoup(res.content, 'html.parser')
            viewstate = soup.select('input#__VIEWSTATE')[0].get('value')
            self.cookies.update({'__VIEWSTATE': viewstate})

            payload = {
                'ctl00$ContentPlaceHolder1$loginform$txtUserName': 'as87321234@gmail.com',
                'txtPassword': 'Plokij1234!',
                'ctl00$ContentPlaceHolder1$loginform$signInButton': 'Logging+In...',
                'ctl00$ContentPlaceHolder1$loginform$hidLoginID': '',
                'JavaScriptTest': '1',
                'IsFromNewSite': '1',
                'loginFolder': ''
            }

            res = s.post("https://www.alarm.com/web/Default.aspx",
                         data=payload,
                         cookies=self.cookies,
                         headers={
                             'Origin': 'https: // www.alarm.com',
                             'Host': 'www.alarm.com',
                             'DNT': '1',
                             'Referer': 'https://www.alarm.com/login?m=logout'
                         },
                         auth=(),
                         )

            self.cookies.update(res.cookies)
            self.headers.update(res.headers)

            print(self.headers)
            print(self.cookies)

            AlarmDotCom.dump_response(s, res)

    def select_system(self, system):
        header = {
            'Referer': 'https://www.alarm.com/web/system/home',
            'SourcePath': '/web/system/home',
            'Host': 'www.alarm.com',
            'cookieTest': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:94.0) Gecko/20100101 Firefox/94.0',
            'IsFromNewSite': '1',
            'adc_e_loggedInAsSubscriber': '1',
            'login': 'as87321234@gmail.com',
            'auth_CustomerDotNet': '4F65454965BEE59D14BAF8EA434D431B22676797AB9F34237F6F3EEE7BB44D4A9E1E658F4E9AD0B4737E4337B37465F91AE5949EFC58397BCDB29DDDB2F7EAB068929CB1427155CC7CA0C00A48B07FFF'
        }

        self.headers.update(header)

        with self.session as s:
            res = s.get(
                "https://www.alarm.com/web/api/devices/sensors?ids%5B%5D=97140300-5&ids%5B%5D=97140300-1&ids%5B%5D=97140300-6&ids%5B%5D=97140300-4&ids%5B%5D=97140300-3&ids%5B%5D=97140300-229&ids%5B%5D=97140300-2&ids%5B%5D=97140300-8",
                headers=self.headers,
                cookies=self.cookies,
                params={},
                auth=(),
                )

        self.cookies.update(res.cookies)
        self.headers.update(res.headers)

        soup = BeautifulSoup(res.content, 'html.parser')
        print(soup.prettify())

    def get_sensor(self):
        header = {
            'Host': 'www.alarm.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            # 'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96”',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://www.alarm.com/login.aspx',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        with self.session as s:
            res = s.get("https://www.alarm.com/web/Security/Sensors.aspx",
                        headers=header,
                        cookies={},
                        auth=(),
                        )

        self.cookies = res.cookies
        self.headers = res.headers


alarm_dot_com: AlarmDotCom = AlarmDotCom()
alarm_dot_com.login()

alarm_dot_com.select_system('Home')
alarm_dot_com.get_sensor()
print('Done ...')
