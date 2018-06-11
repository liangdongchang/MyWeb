'''
@author ldc

'''
import hashlib
import random

import datetime
import time
from pytz import unicode

class GetLetter:
	def getLetter(self,str_input):
		list1 = self.multi_get_letter(str_input)
		res = ''
		for i in list1:
			if type(i).__name__ == 'bytes':
				i = i.decode()
			res = res + i
		return res

	# 获取汉字首字母
	def multi_get_letter(self,str_input):
		if isinstance(str_input, unicode):
			unicode_str = str_input
		else:
			try:
				unicode_str = str_input.decode('utf8')
			except:
				try:
					unicode_str = str_input.decode('gbk')
				except:
					print('unknown coding')
					return
		return_list = []
		for one_unicode in unicode_str:
			return_list.append(self.single_get_first(one_unicode))
		return return_list

	def single_get_first(self,unicode1):
		str1 = unicode1.encode('gbk')
		# print(len(str1))
		try:
			ord(str1)
			return str1
		except:
			asc = str1[0] * 256 + str1[1] - 65536
			# print(asc)
			if asc >= -20319 and asc <= -20284:
				return 'a'
			if asc >= -20283 and asc <= -19776:
				return 'b'
			if asc >= -19775 and asc <= -19219:
				return 'c'
			if asc >= -19218 and asc <= -18711:
				return 'd'
			if asc >= -18710 and asc <= -18527:
				return 'e'
			if asc >= -18526 and asc <= -18240:
				return 'f'
			if asc >= -18239 and asc <= -17923:
				return 'g'
			if asc >= -17922 and asc <= -17418:
				return 'h'
			if asc >= -17417 and asc <= -16475:
				return 'j'
			if asc >= -16474 and asc <= -16213:
				return 'k'
			if asc >= -16212 and asc <= -15641:
				return 'l'
			if asc >= -15640 and asc <= -15166:
				return 'm'
			if asc >= -15165 and asc <= -14923:
				return 'n'
			if asc >= -14922 and asc <= -14915:
				return 'o'
			if asc >= -14914 and asc <= -14631:
				return 'p'
			if asc >= -14630 and asc <= -14150:
				return 'q'
			if asc >= -14149 and asc <= -14091:
				return 'r'
			if asc >= -14090 and asc <= -13119:
				return 's'
			if asc >= -13118 and asc <= -12839:
				return 't'
			if asc >= -12838 and asc <= -12557:
				return 'w'
			if asc >= -12556 and asc <= -11848:
				return 'x'
			if asc >= -11847 and asc <= -11056:
				return 'y'
			if asc >= -11055 and asc <= -10247:
				return 'z'
			return ''
# 获取汉字首字母
def getFirstLetters(str_input):
	return GetLetter().getLetter(str_input)

# 获取随机颜色
def getRandomColor():
	red = random.randint(0,255)
	green = random.randint(0,255)
	blue = random.randint(0,255)
	return (red,green,blue)

# 对输入的字符串生成消息摘要
def useMd5(strInput):
	md5 = hashlib.md5()
	md5.update(strInput.encode('utf-8'))
	return md5.hexdigest()

# 获取用户Ip
def getUserIP(request):
	# 获取客户端IP
	if 'HTTP_X_FORWARDED_FOR' in request.META:
		return request.META['HTTP_X_FORWARDED_FOR']
	else:
		return request.META['REMOTE_ADDR']

# 获取今天的零点和23:59
def getTodayStartAndEnd():
	now = time.time()
	midnight = now - (now % 86400) + time.timezone
	pre_midnight = midnight - 86400
	now_midnight = midnight - 1
	start_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pre_midnight)),
											"%Y-%m-%d %H:%M:%S")
	end_time = datetime.datetime.strptime(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_midnight)),
										  "%Y-%m-%d %H:%M:%S")
	return (start_time,end_time)

# 统计总分数、票数、平均分
def voteCount(voteRecords):
	# 统计投票人数
	if voteRecords:
		num = voteRecords.count()
	else:
		num = 0
	# 统计总分数
	sum = 0
	for voteRecord in voteRecords:
		sum += voteRecord.vPolls
	avg = 0
	if num:
		avg = int(sum / num)
	return {'num': num, 'sum': sum, 'avg': avg}

if __name__ == '__main__':
	pass