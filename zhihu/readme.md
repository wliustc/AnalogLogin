## 模拟知乎登录 ##

**应用环境**

 1. python3.6
 2. pycharm
 3. windows7
 4. requests


----------


## 过程分析 ##

----------


首先请求一下'https://www.zhihu.com/signup?next=%2F'
输入账号密码查看登录请求要携带的参数

            链接: 'https://www.zhihu.com/api/v3/oauth/sign_in'
            client_id = c3cef7c66a1843f8b3a9e6a1e3160e20 
            grant_type = password 登录的格式
            timestamp = 时间戳
            source = com.zhihu.web
            signature = 2c48ba8e56a9b511961e33af3b9b06190e005e98
            username = 用户名
            password = 密码
            captcha = 验证码
            lange = en
            ref_source = homepage
            utm_source = '' 

要获取的就是 signature
在谷歌的开发者工具中按 ctrl+shift+f进行搜索
先搜索值 搜索不到就是生成的
js文件为https://static.zhihu.com/heifetz/main.app.51ca10ea844d4b93dbfd.js
signature ：

                r = new a.a("SHA-1", "TEXT");
                return r.setHMACKey("d1b964811afb40118a12068ff74a12f4", "TEXT"),
                r.update(e),
                r.update(i.a),
                r.update("com.zhihu.web"),
                r.update(String(n)),
                s({
                    clientId: i.a,
                    grantType: e,
                    timestamp: n,
                    source: "com.zhihu.web",
                    signature: r.getHMAC("HEX")
                },
            t)
signature生产方法：

    import hmac
        def _get_signature(self, timestamp):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = 'password'
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        source = 'com.zhihu.web'
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()
        


----------
**准备登录**
在登录之前要请求一次验证码
captchaurl = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
返回True的时候输入验证码 False 直接登录

**登录**

    post_data = {
        'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',
        'grant_type':'password',
        'timestamp':get_time(),
        'source':'com.zhihu.web',
        'signature':_get_signurate(get_time()),
        'username':你的用户名,
        'password':你的密码,
        'captcha':'',
        'lang':'cn',
        'ref_source':'homepage',
        'utm_source':'',
    }
    loginUrl = 'https://www.zhihu.com/api/v3/oauth/sign_in'
    res = s.post(loginUrl,data=post_data,headers=headers)
    
**判断是否登录成功**
通过能否获取用户信息判断是否登录成功
‘https://www.zhihu.com/api/v4/me?include=visits_count0’
返回值为

    {
        uid: 60780879806464,
        follow_notifications_count: 0,
        user_type: "people",
        editor_info: [ ],
        default_notifications_count: 1,
        url_token: "wang-ming-ming-30-72",
        id: "006f4574c6ed1ef3cc6fe7f95b678a74",
        messages_count: 1,
        name: "你的用户名",
        is_advertiser: false,
        url: "http://www.zhihu.com/api/v4/people/006f4574c6ed1ef3cc6fe7f95b678a74",
        badge: [ ],
        visits_count: 179,
        headline: "",
        avatar_url: "https://pic4.zhimg.com/v2-2e3731109a61363db1c7026ccb3a95f8_is.jpg",
        is_org: false,
        gender: 1,
        type: "people",
        vote_thank_notifications_count: 0,
    }
