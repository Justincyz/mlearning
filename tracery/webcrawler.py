#Copyright 2017, Yuzhuang Chen
#yuzhuangchen1@gmail.com	


import sys
import urllib2
import re
import os
from bs4 import BeautifulSoup
import subprocess
import robotparser
import urlparse

	
def first_level():
	url = "file:///Users/yuzhuangchen/Desktop/tweet.htm" 
	info = urllib2.urlopen(url).read()

	if user_agent:
		headers['User-agent'] = 'BadCrawler'
	soup = BeautifulSoup(info,'lxml')
	for link in soup.find_all(name="div"):
		if 'class' in  link.attrs:
			temp_name = str(link.contents)
			f.write(str('{}\n'.format(temp_name.rstrip("'']").lstrip("[u'"))))
			

user_agent =''
f = file('result.txt','w')

first_level()
f.close()	


