# SmartQQ
通过SmartQQ(网页版QQ)的接口收发消息的API

# 警告
**这个库可能随时失效。**

## 依赖
```Python
from PIL import Image
import requests
import time
import json
import random
import re
import threading
import signal
```

## Demo
```Python
#! /usr/bin/env python3
import SmartQQ

# 人类的本质就是一台复读机
def the_essence_of_human_is_a_repeater(smartqq, pack) :
	if(pack['type'] == 'group_message' and pack['send_uin'] != smartqq.qq) :
		qq.send_to_group(pack['from_uin'], pack['content'])
	if(pack['type'] == 'message' and pack['from_uin'] != smartqq.qq) :
		qq.send_to_friend(pack['from_uin'], pack['content'])

qq = SmartQQ.SmartQQ()
qq.login()
qq.start(the_essence_of_human_is_a_repeater,True)
```

## 说明

### uin、gin、gcode
``uin``是标识QQ用户的编号，类似QQ号码，但与QQ号码的值不同  
``gin``是标识QQ群组的编号，类似群号码，但与群号码的值不同  
``gcode``是标识QQ群组的另一个编号，仅在查询群组成员列表时使用  
* 无法获得自己的uin，当自己发出消息时，也会收到该消息，其中发送者uin的值为自己的QQ号码而不是uin

### 创建对象、登录和主循环
```Python
import SmartQQ
qq = SmartQQ.SmartQQ  # 创建对象
qq.login()            # 登录，会在控制台上打印出二维码
qq.start(None,True)   # 启动主循环
```

### SmartQQ.start
```Python
def start(self, callback, DEBUG=False)
```
* ``callback`` - 回调函数，每次收到消息时调用该函数
* ``DEBUG`` - 表示是否打印收到的消息进行调试，会拉取好友，群组和所有群组成员的列表

### 回调函数
在SmartQQ的主循环中，每次收到消息都会把SmartQQ对象本身和包装好的消息数学作为参数调用回调函数
```Python
def callback(smartqq, pack)
```
* ``smartqq`` - SmartQQ对象  
* ``pack`` - 包含收到的消息的相关数据
  * ``pack['type']`` - 消息类型'message'表示好友消息，'group_message'表示群消息
  * ``pack['from_uin']`` - 消息来源的uin(好友的uin或群组的gin)，自己发出消息时这个值为自己的QQ号码而不是uin
  * ``pack['send_uin']`` - 消息发送者(好友或群成员)的uin
  * ``pack['content']`` - 消息的内容
  * ``pack['reply']`` - 函数，向消息来回回发消息，仅需要一个参数表示回复消息的内容

### SmartQQ.qq
登录成功后，这个值为自己的QQ号码，可以用来分辨消息是否是自己发出的

### SmartQQ.send_to_friend
向好友发送消息
```Python
def send_to_friend(self, uin, msg)
```
``uin`` - 好友的uin
``msg`` - 消息内容

### SmartQQ.send_to_group
```Python
def send_to_group(self, gin, msg)
```
``gin`` - 群组的gin
``msg`` - 消息内容

### SmartQQ.group_list
获取群组列表
```Python
def group_list(self)
```

### SmartQQ.group_name
获取群组的名称
```Python
def group_name(self, glist, gin)
```
``glist`` - 群组列表
``gin`` - 群组的gin

### SmartQQ.group_code
获取群组的gcode值，仅在获取群组成员时有用
```Python
def group_code(self, glist, gin)
```
``glist`` - 群组列表
``gin`` - 群组的gin

### SmartQQ.group_member_list
获取群组的成员列表
```Python
def group_member_list(self, gcode)
```
``gcode`` - 群组的gcode

### SmartQQ.group_member_name
获取群组成员的名字
```Python
def group_member_name(self,mlist, uin)
```
``mlist`` - 群组成员列表
``uin`` - 群组成员的uin

### SmartQQ.friend_list
获取好友列表
```Python
def friend_list(self)
```

### SmartQQ.friend_info
获取好友信息
```Python
def friend_info(self, uin)
```
``uin`` - 好友的uin

## SmartQQ.friend_name
获取好友的名字
```Python
def friend_name(self, uin)
```
``uin`` - 好友的uin
