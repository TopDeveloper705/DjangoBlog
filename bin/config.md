# 主要功能配置介绍:

## 缓存：
缓存默认使用`memcache`缓存，如果你没有`memcache`环境，则将`settings.py`中的`locmemcache`改为`default`,并删除默认的`default`配置即可。
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'django_test' if TESTING else 'djangoblog',
        'TIMEOUT': 60 * 60 * 10
    },
    'locmemcache': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 10800,
        'LOCATION': 'unique-snowflake',
    }
}
```
## oauth登录:

现在已经支持微博，Google，GitHub，Facebook登录，需要在其对应的开放平台申请oauth登录权限，然后在  
**后台->Oauth** 配置中新增配置，填写对应的`appkey`和`appsecret`以及回调地址。  



## owntracks：
owntracks是一个位置追踪软件，可以定时的将你的坐标提交到你的服务器上，现在简单的支持owntracks功能，需要安装owntracks的app，然后将api地址设置为:
`你的域名/owntracks/logtracks`就可以了。然后访问`你的域名/owntracks/show_dates`就可以看到有经纬度记录的日期，点击之后就可以看到运动轨迹了。地图是使用高德地图绘制。

## 邮件功能：
同样，将`settings.py`中的`ADMINS = [('liangliang', 'liangliangyy@gmail.com')]`配置为你自己的错误接收邮箱，另外修改:
```python
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = os.environ.get('DJANGO_EMAIL_USER')
```
为你自己的邮箱配置。

## 微信公众号
集成了简单的微信公众号功能，在微信后台将token地址设置为:`你的域名/robot` 即可，默认token为`lylinux`，当然你可以修改为你自己的，在`servermanager/robot.py`中。
然后在**后台->Servermanager->命令**中新增命令，这样就可以使用微信公众号来管理了。  
## 网站配置介绍  
在**后台->BLOG->网站配置**中,可以新增网站配置，比如关键字，描述等，以及谷歌广告，网站统计代码及备案号等等。  
其中的*静态文件保存地址*是保存oauth用户登录的头像路径，填写绝对路径，默认是代码目录。
