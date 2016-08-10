#!/usr/bin/python
from __future__ import division
import urllib2
import sys,os,time
import ConfigParser
ISOTIMEFORMART='%Y%m%d %X'
os.remove("log")
log = open("log","a")
failed_list=[]
class readConf(object):
	query_path = ""
	test_host = ""
	test_port = ""
	online_host = ""
	online_port = ""
	def __init__(self,config_path):
		conf = ConfigParser.ConfigParser()
		conf.read(config_path)
		kvs_Global = conf.items("Global")
		kvs_test = conf.items("Test")
		kvs_online = conf.items("Online")
		print "[INFO]\t",getTime(),"[Sogou-Observer,","Items:Global=",kvs_Global,",Test=",kvs_test,",Online=",kvs_online,"]"
		readConf.query_path = conf.get("Global","query_path")
		readConf.test_host = conf.get("Test","test_host")
		readConf.test_port = conf.get("Test","test_port")
		readConf.online_host = conf.get("Online","online_host")
		readConf.online_port = conf.get("Online","online_port")

def makeRequest(query_path,test_host,test_port,online_host,online_port):
	filepath = os.getcwd() + "/" + query_path
	print "[INFO]\t",getTime(),"[Sogou-Observer,query_path=",query_path,"]"
	if os.path.exists(filepath):
		file = open(filepath,'r')
		success = 0
		failed = 0
		total = 0
		for query in file: 
			time.sleep(0.5)
			test_url = getUrl(test_host,test_port,query)
			online_url = getUrl(online_host,online_port,query)
			res_test = sendRequest(test_url)
			res_online = sendRequest(online_url)
			if res_test != res_online:
				failed_list.append(query)
				log.write("\n\n"+"#"*88+"\n\n"+test_url+"\n\n"+res_test+"\n\n"+online_url+"\n\n"+res_online+"\n")
				failed+=1
			else:
				success+=1
		total = failed  + success
		print "Failed:"+str(failed)+"\nSuccess:"+str(success)+"\ntotal:"+str(total)
		
		print "Rate Of Failed:%.4f%%" % (failed*100/total)
		
		print failed_list	
		file.close()
	else:
		print "query file is not exists"
		sys.exit(1)

def getUrl(host,port,query):
	url = "http://" + host + ":" + port + query
	return url

def sendRequest(url):
	req = urllib2.Request(url)
	res_data=urllib2.urlopen(req)
	result = res_data.read()
	return result


def getTime():
	return time.strftime(ISOTIMEFORMART,time.localtime(time.time()))

	

if __name__ == '__main__':
	cfg=readConf("tools.ini")
	makeRequest(cfg.query_path,cfg.test_host,cfg.test_port,cfg.online_host,cfg.online_port)
