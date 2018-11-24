# 使用的api网站

https://openweathermap.org/api
google, bing 搜索"weather api"第一结果
免费

# 用到的功能

## 实时天气

### 请求
GET api.openweathermap.org/data/2.5/weather?id=658225&APPID=a9a1b6701177be507491fdd6c47e9fb3

### 说明
- id=658225 是 Helsinki
- id=660158 是 Espoo
- APPID=a9a1b6701177be507491fdd6c47e9fb3 是 李鑫 注册账号下面的api key

### 返回
{"coord":{"lon":24.94,"lat":60.17},"weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],"base":"stations","main":{"temp":274.15,"pressure":1015,"humidity":80,"temp_min":274.15,"temp_max":274.15},"visibility":10000,"wind":{"speed":6.7,"deg":270},"clouds":{"all":75},"dt":1542999000,"sys":{"type":1,"id":5019,"message":0.0042,"country":"FI","sunrise":1542955220,"sunset":1542979963},"id":658225,"name":"Helsinki","cod":200}


## 紫外线指数 UV Index
## 空气污染(api网站标记此功能为beta版)

# 暂未用到的功能

- 5日天气预报
- 16日天气预报
- 历史数据
- 天气地图
。。。


# How to start

- Sign up/ Sign in (gmail)
- Get API key
a9a1b6701177be507491fdd6c47e9fb3

- 缓存

no more than one time every 10 minutes for one location

一个城市只需请求一次，就缓存下来，直到过期

免费账户限制10分钟请求1次

有可能请求失败，需要等待10分钟

- 服务器地址
api.openweathermap.org

- 城市id

{
    "id": 658225,
    "name": "Helsinki",
    "country": "FI",
    "coord": {
      "lon": 24.93545,
      "lat": 60.169521
    }
  },

 {
    "id": 660158,
    "name": "Espoo",
    "country": "FI",
    "coord": {
      "lon": 24.652201,ß
      "lat": 60.2052
    }
  }
