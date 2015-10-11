def auth_by_info(username,password):
	url_login = 'http://student.tsinghua.edu.cn/practiceLogin.do'
	data = (('username',username),('password',password),)
	import urllib,urllib2
	req = urllib2.Request(url_login,urllib.urlencode(data))
	res_data = urllib2.urlopen(req)
	res = res_data.read()
	print res
	if res !='':
		return True
	else:
		return False

print auth_by_info('2012310575','Luoch9679*')