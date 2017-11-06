#! /usr/bin/env python3

import requests
import json
import SmartQQ

# 获取B站番剧的今日更新
def bilibili_today() :
	try :
		output = ''
		response = requests.get("https://bangumi.bilibili.com/web_api/timeline_global")
		data = response.content.decode('utf-8')
		rjson = json.loads(data)
		for day in rjson['result'] :
			if(day['is_today'] == 1) :
				for item in day['seasons'] :
					output += item['pub_time'] + " : " + item['title'] + "\n"
		return output
	except Exception as e :
		return e
		
def callback(smartqq, pack) :
	if(pack['content'] == "/bilibili") :
		pack['reply'](bilibili_today())
		
qq = SmartQQ.SmartQQ()
qq.login()
qq.start(callback)
