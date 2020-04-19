#### 功能简介
- 查询上海公交的到站时间，支持多条线路，同时可以语音提醒。
![](https://pz-common.oss-cn-qingdao.aliyuncs.com/junqing.ren/1587290683850.jpg "")

![](https://pz-common.oss-cn-qingdao.aliyuncs.com/junqing.ren/1587290608256.jpg "")

![](https://pz-common.oss-cn-qingdao.aliyuncs.com/junqing.ren/1587290639693.jpg "")

![](https://pz-common.oss-cn-qingdao.aliyuncs.com/junqing.ren/1587290563218.jpg "")

安卓体验版：http://pz-common.oss-cn-qingdao.aliyuncs.com/H5387A906_0507223016.apk

#### 项目说明

- 服务端使用Python语言，基于https://github.com/ark930/shanghai-bus 做的二次开发，特此感谢。 原项目没有语音提醒，仅查询功能。语音功能调[用百度语音API](https://ai.baidu.com/tech/speech/tts_online)。 启动项目：`python ./service/router.py`。

- 客户端是vue单页，使用[dcloud](https://www.dcloud.io/) 打包的hybrid应用。
