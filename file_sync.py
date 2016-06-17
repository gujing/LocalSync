#encoding=utf-8 

import os
import hashlib
import shutil

index_file_path = 'D:\\index.prop'

def is_file_same(a,b):
	return get_md5(a) == get_md5(b)

def is_file_modify(a,md5):
	print get_md5(a), md5
	return get_md5(a) != md5

def a_notin_b(a,b):
	return [i for i in a if i not in b]

def a_in_b(a,b):
	return [i for i in a if i in b]

def get_md5(file):
	m = hashlib.md5()
	a_file = open(file, 'rb')
	m.update(a_file.read())
	a_file.close()
	return m.hexdigest()

def safe_get_dict(dic,key):
	return dic[key] if key in dic else None

def list_file_folder(path):
	a = []
	res_list = os.walk(path)
	root_path = path  #todo 完善分隔符结尾的情况
	for res in res_list:
		for file_name in res[2]:
			a.append((res[0] + os.sep + file_name)[len(root_path) + 1:])
	return a

def gen_index(path,rule_name):
	files = list_file_folder(path)
	with open(index_file_path,'w') as a_file:
		a_file.write('[' + rule_name + ']' + os.linesep)
		for file in files:
			a_file.write(file + ',' + get_md5(path + os.sep + file) + os.linesep)

def get_index():
	folder_indexs = {}
	current_folder = ''
	with open(index_file_path,'r') as a_file:
		for line in a_file:
			rline = line.rstrip()
			if rline[0] == '[' and rline[-1] == ']':
				current_folder = rline[1:-1]
				folder_indexs[current_folder]={}
			else:
				data = rline.split(',')
				folder_indexs[current_folder][data[0]] = data[1]
	return folder_indexs

def copy_file(src,target):
	target_folder = target[:target.rindex(os.sep)]
	if os.path.exists(target_folder):
		pass
	else:
		os.makedirs(target_folder)
	shutil.copyfile(src,target)

def copy_diff_files(path_from,path_to):
	local_diff_files = a_notin_b(list_file_folder(path_from) ,list_file_folder(path_to))
	print local_diff_files
	for file in local_diff_files:
		copy_file(os.path.join(path_from,file),os.path.join(path_to,file))

def start_sync(local_path,remote_path,md5_info):
	local_path_files = list_file_folder(local_path)
	index_files = md5_info.keys()
	print local_path_files
	print index_files
	# copy_diff_files(local_path ,remote_path)
	for file in a_notin_b(index_files,local_path_files):
		if os.path.isfile(os.path.join(remote_path,file)):
			os.remove(os.path.join(remote_path,file))
	for file in local_path_files:
		if is_file_modify(os.path.join(local_path,file),safe_get_dict(md5_info,file)):
			copy_file(os.path.join(local_path,file),os.path.join(remote_path,file))
			
	# copy_diff_files(set(remote_path_files) ,set(local_path_files))
	
#local_path = '/Users/gin/Workspace/PythonProject'
rule_name = 'test'
local_path = 'D:\\Workspace\\ToolBox'
remote_path = 'D:\\Workspace\\ToolBoxBak'

# print is_file_same('tcpScanner.py','tcpScanner.py')
# print list_file_folder(local_path)
gen_index(remote_path,rule_name)
# copy_file(local_path + '\\combineFile.py',remote_path + '\\xx\\combineFile.py')
folder_md5_index = get_index()
his_md5 = folder_md5_index[rule_name]
# print his_md5
start_sync(local_path,remote_path,his_md5)