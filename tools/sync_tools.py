# coding:utf-8


import os,time,shutil,zipfile


# 同步目录
# src_dir 源目录
# dst_dir 目标目录
# is_recursion 是否递归
# ignores 忽略文件名列表
def sync_dir(src_dir, dst_dir, is_recursion=True, ignores=[]):
	files = os.listdir(src_dir)
	for f in files:

		# 忽略列表
		if f in ignores: continue

		src_path = os.path.join(src_dir, f)
		dst_path = os.path.join(dst_dir, f)

		if os.path.isdir(src_path):
			
			# 是否递归
			if not is_recursion: continue

			# 创建目录
			try:
				os.mkdir(dst_path)
				print "mkdir", dst_path
			except:
				pass
	
			sync_dir(src_path, dst_path, is_recursion, ignores)
		
		else:
			print "copy", src_path, dst_path
			shutil.copyfile(src_path, dst_path)



# 压缩目录
def zip_dir(src_dir, output_file, is_recursion=True, ignores=[]):
	f = zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED)
	_zip(src_dir, f, is_recursion, ignores, src_dir)
	f.close()

def _zip(src_dir, zip_file, is_recursion, ignores, root_path):
	files = os.listdir(src_dir)
	for f in files:

		# 忽略列表
		if f in ignores: continue

		src_path = os.path.join(src_dir, f)
		zip_path = src_path[len(root_path):]

		if os.path.isdir(src_path):
			
			# 是否递归
			if not is_recursion: continue

			# 创建目录
			try:
				zip_file.write(src_path, zip_path)
				print "mkdir", src_path, zip_path
			except:
				pass
	
			_zip(src_path, zip_file, is_recursion, ignores, root_path)
		
		else:
			print "zip", src_path, zip_path
			zip_file.write(src_path, zip_path)



def main():
	print "run -------------------"
	
	# test
	sync_dir('./src', './dst', True, ['svn'])
	zip_dir('./src', './out.zip', True, ['svn'])

	print "over ------------------"



if __name__ == '__main__':
	main()