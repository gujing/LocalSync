#encoding=utf-8 

import os
import hashlib

def is_file_same(a,b):
	return get_md5(a) == get_md5(b)

def get_md5(file):
	m = hashlib.md5()
	a_file = open(file, 'rb')
	m.update(a_file.read())
	a_file.close()
	return m.hexdigest()

def list_file_folder(path):
	a = []
	res_list = os.walk(path)
	root_path = path  #todo 完善分隔符结尾的情况
	for res in res_list:
		for file_name in res[2]:
			a.append((res[0] + os.sep + file_name)[len(root_path) + 1:])
	return a

def gen_index(path):
	files = list_file_folder(path)
	with open('index.prop','w') as a_file:
		a_file.write('[' + path + ']' + os.linesep)
		for file in files:
			a_file.write(file + ',' + get_md5(path + os.sep + file) + os.linesep)

print is_file_same('tcpScanner.py','tcpScanner.py')
print list_file_folder('/Users/gin/Workspace/PythonProject')
gen_index('/Users/gin/Workspace/PythonProject')