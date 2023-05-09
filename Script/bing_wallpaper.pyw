import requests
import random
import re
import os
import datetime
import time

file_dir  =  os.path.dirname(os.path.abspath(__file__))+"/"


def get_image():
	user_agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",]
	headers = {'User-Agent': random.choice(user_agent)}
	
	#format (非必需)返回数据格式，不存在返回xml格式 js (一般使用这个，返回json格式) xml(返回xml格式)
	#idx (非必需) 请求图片截止天数 0 今天 -1 截止中明天(预准备的) 1 截止至昨天，类推(目前最多获取到7天前的图片)
	#n (必需) 1-8 返回请求数量，目前最多一次获取8张
	#mkt (非必需) 地区 zh-CN ...
	#https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN


	url_api="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
	r = requests.get(url_api)
	image_name_base = r.json()["images"][0]["urlbase"]
	image_info = r.json()["images"][0]["copyright"]
	
	image_name_uhd  = image_name_base + "_UHD.jpg"
	image_name_1080 = image_name_base + "_1920x1080.jpg"
	
	utc_today_o = datetime.datetime.utcnow()+datetime.timedelta(hours=8) 
	utc_today = utc_today_o.strftime("%Y-%m-%d")
	#print(utc_today)
	
	url_uhd = "https://cn.bing.com"+image_name_uhd
	print(url_uhd)
	# img_save_path=file_dir+"images_download/"+utc_today+re.findall(r'id=(.*?jpg)',image_name_uhd)[0]
	img_save_path=file_dir+utc_today+'.jpg'
	# 提取地名
	img_fromwhere = []
	img_fromwhere = [s for str in image_info.split(",") for s in str.split("，")]  # this line was written via GPT
	img_fromwhere = img_fromwhere[0]
	img_save_path2=file_dir+utc_today+'-'+img_fromwhere+'.jpg'
	print(img_save_path)
	
	img = requests.get(url_uhd)
	with open(img_save_path2, "wb") as fwi:
		fwi.write(img.content)
		print(img_save_path + "下载成功")
    
	print(image_info)
	re_res = re.findall("^(.*?)\s\(©\s(.*?)\)$",image_info)
	print(re_res)

	# cmd = "%s %s %s %s"%("exiftool","-overwrite_original","-artist=\"%s\""%re_res[0][1],"\"%s\""%img_save_path)
	# print(cmd)
	# print(os.popen(cmd))
	# time.sleep(1)
	# cmd = "%s %s %s %s"%("exiftool","-overwrite_original","-usercomment=\"%s\""%re_res[0][0],"\"%s\""%img_save_path)
	# print(cmd)
	# print(os.popen(cmd))
	
	data=utc_today_o.strftime("%Y.%m.%d : ")+image_info+"\n"
	print(data)
	
	with open(file_dir+"file_log.txt","a",encoding='utf-8') as fwi:
		fwi.write(data)


if __name__ == '__main__':
    while(1):
	    try:
    		get_image()
    		print("download success...")
    		break
	    except Exception as e:
	    	print(e)
	    	print("try again...")
