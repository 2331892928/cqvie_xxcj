import requests
import random

"""
----------------------配置文件
"""
user = ''  # 学号
dizhi = ''  # 地址，地址为空则当前电脑定位，定位失败则是：重庆市江津区圣泉街道重庆工程职业技术学院江津校区-第1教学楼,推荐手动填写，自动获取定位已失效
tuisong = ''

# 完成推送地址，推送消息请用{},dark。
"""
----------------------配置文件
"""


class gctd:
    def __init__(self):
        self.ip = "106.84." + str(random.randint(146, 254)) + "." + str(random.randint(1, 254))
        self.get_url = "https://sac.cqvie.edu.cn/reportApi/LoginApi/v1/userLogin"
        self.dw_url = "https://restapi.amap.com/v3/geocode/regeo?key=6d399f240a05329918e8006c29d12b5f&s=rsv3&language" \
                      "=zh_cn" \
                      "&extensions=base&platform=JS&logversion=2.0&appname=https%3A%2F%2Fsac.cqvie.edu.cn" \
                      "%2Ffxsq%2FuserLogin&csid=075A1EA9-A0BC-4510-92FB-932460F4C774&sdkversion=1.4.18 "
        self.tj_url = "https://sac.cqvie.edu.cn/reportApi/EpidemicApi/v1/submitEpidemic"
        self.heads = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Mi 10 Build/N2G470; wv) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Version/4.0 Chrome/ 95.0. 4638.74 Mobile Safari/537.36 MMWEBID/ 84 "
                          "MicroMessenger/8.0.2.1860(0x28000234) Process/tools WeChat/ arm32 Weixin NetType/ WIFI "
                          "Language/zh_ _CN ABI/arm32",
            "x-forwarded-for": self.ip,
            "x-remote-IP": self.ip,
            "x-remote-ip": self.ip,
            "x-client-ip": self.ip,
            "x-client-IP": self.ip,
            "X-Real-IP": self.ip,
            "client-IP": self.ip,
            "x-originating-IP": self.ip,
            "x-remote-addr": self.ip,
            "Client-Ip": self.ip,
            "Remote_Addr": self.ip

        }
        self.tj_heads = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; Mi 10 Build/N2G470; wv) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Version/4.0 Chrome/ 95.0. 4638.74 Mobile Safari/537.36 MMWEBID/ 84 "
                          "MicroMessenger/8.0.2.1860(0x28000234) Process/tools WeChat/ arm32 Weixin NetType/ WIFI "
                          "Language/zh_ _CN ABI/arm32",
            "Cookie": "",
            "x-forwarded-for": self.ip,
            "x-remote-IP": self.ip,
            "x-remote-ip": self.ip,
            "x-client-ip": self.ip,
            "x-client-IP": self.ip,
            "X-Real-IP": self.ip,
            "client-IP": self.ip,
            "x-originating-IP": self.ip,
            "x-remote-addr": self.ip,
            "Client-Ip": self.ip,
            "Remote_Addr": self.ip
        }
        self.phone = ""
        self.userid = ""
        if user == '':
            print("学号为空")
            return
        self.main()

    def main(self):
        global dizhi
        user_json = self.get_user()
        print(user_json)
        if user_json['status'] == 200:
            self.phone = user_json['data']['phone']
            self.userid = user_json['data']['id']
            if dizhi == '':
                dizhi = self.get_wz()
            self.tj()
        else:
            print("接口请求失败")

    def get_user(self):  # 获取信息
        ym = requests.post(self.get_url, headers=self.heads, data={
            'userNumber': user
        })
        if ym.status_code == 200:
            self.tj_heads['Cookie'] = "SESSION=" + ym.cookies['SESSION']
            return ym.json()
        else:
            print("请求接口失败")

    def get_wz(self):  # 获取位置
        ym_1 = requests.get(
            "https://webapi.amap.com/maps/ipLocation?key=6d399f240a05329918e8006c29d12b5f&callback=jsonp_919580_&platform=JS&logversion=2.0&appname=https%3A%2F%2Fsac.cqvie.edu.cn%2Ffxsq%2FuserLogin&csid=36CACA2A-DCCA-42BC-80BE-68995D810F5B&sdkversion=1.4.18")
        ym_1 = ym_1.content.decode()
        amen_fz = fz()
        j = amen_fz.jqzf(ym_1, 'lng":"', '"')
        w = amen_fz.jqzf(ym_1, 'lat":"', '"')
        ym = requests.get(self.dw_url + "&location=" + j + "," + w)
        if ym.status_code == 200:
            if ym.json()['status'] == 1:
                return ym.json()['regeocode']['formatted_address']
            else:
                return "重庆市江津区圣泉街道重庆工程职业技术学院江津校区-第1教学楼"
        else:
            return "重庆市江津区圣泉街道重庆工程职业技术学院江津校区-第1教学楼"

    def tj(self):
        print(self.tj_heads)
        ym = requests.post(self.tj_url, headers=self.tj_heads, data={
            'phone': self.phone,
            'current': dizhi,
            'sfly': 0,
            'temperature': 0,
            'symptom': 0,
            'remark': '',
            'zgfx': 0,
            'showButton': 0,
            'inzgfx': '',
            'yfy': '',
            'bgszsq': '',
            'hsjc': '',
            'dqdqgl': '',
            'incq': 0,
            'type': 2,
            'userId': self.userid
        })
        if ym.status_code == 200:
            print(ym.json()['msg'])
            if tuisong != "":
                requests.get(tuisong.format(ym.json()['msg']))
        else:
            print("提交失败")


class fz:
    def __init__(self):
        pass

    def jqzf(self, stri, star, end):  # 在字符串中截取字符串star开始，end结束的字符串
        min_1 = stri.find(star)
        max_1 = stri.find(end, min_1)
        if min_1 == -1 or max_1 == -1:
            return "-1"
        return stri[min_1:max_1]


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    cs = gctd()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
