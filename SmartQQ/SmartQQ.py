#! /usr/bin/env python3
'''
https://github.com/hubenchang0515
www.kurukurumi.com
hubenchang0515@outlook.com
'''
from PIL import Image
import requests
import time
import json
import random
import re
import threading
import signal
from .smartqq_hash import *

# 下载二维码并获取cookie
def get_qrcode(img) :

	url1 = "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&style=16&" \
		   "mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&" \
		   "s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong"
	url2 = "https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.9142399367333609"
	response = requests.get(url1) 
	cookie = response.cookies

	response = requests.get(url2, cookies=cookie)
	fImage = open(img,"wb")
	fImage.write(response.content)
	fImage.close()

	cookie.update(response.cookies)
	
	return cookie
	
# 在命令行中显示二维码
def show_qrcode(f) :
	qr_img = Image.open(f)
	for y in range(33) :
		for x in range(33) :
			if(qr_img.getpixel((x*5+2,y*5+2)) == 0) :
				print('  ',end='')
			else :
				print('@@',end='')
		print('')
	qr_img.close()
	
# 在cookie中查找数据
def cookie_find(cookie,name) :
	for item in cookie :
		if(item.name == name) :
			return item.value
			
	return None
	
# 解析二维码状态
def state(msg) :
	values = re.findall(r"\((.*)\)",msg)[0]
	s = eval("[" + values + "]")
	return (int(s[0]) , s[2])
	
# 等待扫描二维码,返回cookie
def check_qrcode() :
	cookie = get_qrcode("qr.png")
	show_qrcode("qr.png")
	url = "https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken=" \
	+ str(hash1(cookie_find(cookie,"qrsig"))) \
	+ "&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&u1=" \
	+ "http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%" \
	+ "3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&" \
	+ "fp=loginerroralert&action=0-0-32750&mibao_css=m_webqq&t=undefined&g=" \
	+ "1&js_type=0&js_ver=10197&login_sig=&pt_randsalt=0"
	flag = 0
	print("请扫描二维码登录")
	for i in range(1000) :
		response = requests.get(url, cookies=cookie)
		msg = response.content.decode('utf8')
		if(state(msg)[0] == 0) :    # 登录成功
			cookie.update(response.cookies)
			response = requests.get(state(msg)[1], cookies=cookie, allow_redirects=False)
			cookie.update(response.cookies)
			print("登录成功")
			return cookie
		elif(state(msg)[0] == 65) : # 二维码失效
			print("二维码失效，请重新启动。")
			return None
		elif(state(msg)[0] == 67 and flag == 0) :
			print("扫描成功，请授权登录。")
			flag = 1
		
		time.sleep(1)
		
	return None

# 退出
def mainloop_quit(signum, frame) :
	quit()
	
# SmartQQ类
class SmartQQ(object) :

	# 获取关键参数并完成登录
	def login(self) :
		cookie = check_qrcode()
		if(cookie == None) :
			return False
	
		ptwebqq = cookie_find(cookie,"ptwebqq") 
	
		# 获取vfwebqq
		url = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq=" + ptwebqq \
		+ "&clientid=53999199&psessionid=&t=1488053293431"
		param = {"Referer" : "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"}
		response = requests.post(url, headers=param, cookies=cookie)
		vfwebqq = eval(response.content)["result"]["vfwebqq"]
	
		# 获取psessionid
		url = "http://d1.web2.qq.com/channel/login2"
		PostParam = {'r': '{"ptwebqq":"%s","clientid":53999199,"psessionid":"","status":"online"}' % (ptwebqq)}
		header = { 'Host': 'd1.web2.qq.com',
		'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
		'Origin':'http://d1.web2.qq.com'}
		response = requests.post(url, headers=header, data=PostParam, cookies=cookie)
		psessionid = eval(response.content)['result']['psessionid']
	
		# 登录
		url = "http://d1.web2.qq.com/channel/get_online_buddies2?" \
		+ "vfwebqq=%s&clientid=53999199&psessionid=%s&t=1488268527333" % (vfwebqq,psessionid)
		header = {'Host':'d1.web2.qq.com',
		'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'}
		response = requests.get(url, headers=header, cookies=cookie)
	
		# qq号码
		self.qq = int(cookie_find(cookie,"uin")[1:])
		
		# 保存属性
		self.cookie     = cookie
		self.ptwebqq    = ptwebqq
		self.vfwebqq    = vfwebqq
		self.psessionid = psessionid

	# 向群发送消息
	def send_to_group(self, gin, msg) :
	
		PostParam = {'r':'{"group_uin":%d,"content":"[\\"%s\\",[\\"font\\",' \
		'{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]",' \
		'"face":525,"clientid":53999199,"msg_id":%d,"psessionid":"%s"}' \
		% (gin,msg,random.randint(10000000,99999999),self.psessionid)}

		header = {'origin':'https://d1.web2.qq.com',
		'referer':'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1',
		'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}
		send_group_url = "https://d1.web2.qq.com/channel/send_qun_msg2"
		response = requests.post(send_group_url, headers=header, data=PostParam, cookies=self.cookie)

	# 向好友发送消息
	def send_to_friend(self, uin, msg) :
	
		PostParam = {'r':'{"to":%d,"content":"[\\"%s\\",[\\"font\\",' \
		'{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]",' \
		'"face":0,"clientid":53999199,"msg_id":%d,"psessionid":"%s"}' \
		% (uin,msg,random.randint(10000000,99999999),self.psessionid)}
	
		header = {'origin':'https://d1.web2.qq.com',
		'referer':'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1',
		'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'}
	
		send_friend_url = "https://d1.web2.qq.com/channel/send_buddy_msg2"
		response = requests.post(send_friend_url, headers=header, data=PostParam, cookies=self.cookie)

	# 获取群组列表
	def group_list(self) :
		url = "https://s.web2.qq.com/api/get_group_name_list_mask2"
		PostParam = {"r":'{"vfwebqq":"%s","hash":"%s"}' % (self.vfwebqq,hash2(self.qq, self.ptwebqq))}
		header = {"origin":"https://s.web2.qq.com",
			"referer":"https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1",
			"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"}
		response = requests.post(url, headers=header, data=PostParam, cookies=self.cookie)
		rjson = json.loads(response.content.decode("utf8"))
		return rjson['result']['gnamelist']

	# 通过gin查gcode,在某些请求中需要
	def group_code(self,glist, gin) :
		for g in glist :
			if(g['gid'] == gin) :
				return g['code']
		return None
	
	# 通过gin查群名称
	def group_name(self,glist, gin) :
		for g in glist :
			if(g['gid'] == gin) :
				return g['name']
		return None

	# 获取群成员信息列表
	def group_member_list(self, gcode) :
		url = "https://s.web2.qq.com/api/get_group_info_ext2?" \
		"gcode=%s&vfwebqq=%s&t=1509848166519" % (gcode, self.vfwebqq)
		header = {"referer":"https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"}
		response = requests.get(url,headers=header,cookies=self.cookie)
		rjson = json.loads(response.content.decode("utf8"))
		return rjson['result']['minfo']

	# 查询群组成员名称
	def group_member_name(self,mlist, uin) :
		for member in mlist :
			if(member['uin'] == uin) :
				return member['nick']
		return None
	
	# 获取好友列表
	def friend_list(self) : 
		url = "https://s.web2.qq.com/api/get_user_friends2"
		header = {"origin":"https://s.web2.qq.com",
			"referer":"https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1",
			"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"}
		PostParam = {"r":'{"vfwebqq":"%s","hash":"%s"}' % (self.vfwebqq, hash2(self.qq, self.ptwebqq))}
		response = requests.post(url, headers=header, data=PostParam, cookies=self.cookie)
		rjson = json.loads(response.content.decode("utf8"))
		return rjson['result']['info']

	# 获取好友信息
	def friend_info(self, uin) :
		url = "https://s.web2.qq.com/api/get_friend_info2?tuin=%d&vfwebqq=%s" \
		"&clientid=53999199&psessionid=%s&t=1509850702128" % (uin, self.vfwebqq, self.psessionid)
		header = {"referer":"https://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1",
			"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36"}
		response = requests.get(url, headers=header, cookies=self.cookie)
		rjson = json.loads(response.content.decode("utf8"))
		return rjson['result']
	
	# 获取好友名称
	def friend_name(self, uin) :
		return self.friend_info(uin)['nick']
	

	# 获取消息并响应
	def start(self, callback, DEBUG=False) :
		signal.signal(signal.SIGINT, mainloop_quit) # 按Ctrl+C退出
		psessionid = self.psessionid
		cookie = self.cookie
		url = "http://d1.web2.qq.com/channel/poll2"
		header = {'Host':'d1.web2.qq.com',
		'Referer':'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2'}
		PostParam = {'r' : '{"ptwebqq":"","clientid":53999199,"psessionid":"%s","key":""}' % (psessionid)}
	
		if(DEBUG) :
			print("[DEBUG] 正在拉取好友列表")
			friends = self.friend_list()
			print("[DEBUG] 正在拉取群列表")
			groups  = self.group_list()
		
			group_member_lists = {}
			for group in groups :
				print("[DEBUG] 正在拉取群组",group['name'],"的成员列表")
				group_member_lists[group['gid']] = self.group_member_list(group['code'])
			print("[DEBUG] 拉取完毕")
	
		while True :
			try :
				# 设置10s超时，防止掉线
				response = requests.post(url, headers=header, data=PostParam, cookies=self.cookie, timeout=10) 
				rjson = json.loads(response.content.decode("utf8"))
				pack = {}
			
				# 来源的uin，群或好友
				pack['from_uin'] = rjson['result'][0]['value']['from_uin']
			
				# 消息内容
				pack['content']  = ''
				for i in rjson['result'][0]['value']['content'][1:] :
					if(isinstance(i,str)) :
						pack['content'] += i
			
				# 消息类型
				pack['type'] = rjson['result'][0]['poll_type']
			
				# 发送者的uin
				if(pack['type'] == "group_message") :
					pack['send_uin'] = rjson['result'][0]['value']['send_uin']
				else :
					pack['send_uin'] = pack['from_uin']
				
				# 回答
				def reply(message) :
					uin = pack['from_uin']
					if(pack['type'] == "message") :
						self.send_to_friend(uin, message)
					elif(pack['type'] == "group_message") :
						self.send_to_group(uin, message)
					else :
						print("暂不支持好友和群组以外的对话")
				pack['reply'] = reply
				
				# 回调
				if(callback != None) :
					threading.Thread(target=callback, args=(self, pack)).start()
				
				# 打印调试信息
				if(DEBUG) :
					if(pack['content'] == "") :
						pack['content'] = "不支持的消息类型。"
					
					print('[DEBUG]',time.strftime("%Y-%m-%d %H:%M:%S \n", time.localtime()),end="")
				
					if(pack['type'] == 'message') :
						print("来自好友",self.friend_name(pack['from_uin']),"的消息")
					elif(pack['type'] == 'group_message') :
						print("来自群组",self.group_name(groups,pack['from_uin']),"的成员",
							self.group_member_name(group_member_lists[pack['from_uin']],pack['send_uin']),
							"的消息")
					print(pack['content'],"\n")
			
			except requests.exceptions.ConnectTimeout as e :
				print("网络连接中断。")
				return 1
			except requests.exceptions.ReadTimeout as e : # 防止掉线
				pass
			except Exception as e :
				print("异常",e)
			#time.sleep(1)



# 测试程序，人类的本质就是一台复读机
if __name__ == "__main__" :
	
	def the_essence_of_human_is_a_repeater(smartqq, pack) :
		if(pack['type'] == 'group_message' and pack['send_uin'] != smartqq.qq) :
			qq.send_to_group(pack['from_uin'], pack['content'])
		if(pack['type'] == 'message' and pack['from_uin'] != smartqq.qq) :
			qq.send_to_friend(pack['from_uin'], pack['content'])
	
	qq = SmartQQ()
	qq.login()
	qq.start(the_essence_of_human_is_a_repeater,True)
	
	

	
	
	
	
	
	
	
	
	
	
	
	
