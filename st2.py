import argparse
import time
import sys
parser = argparse.ArgumentParser(description="使用方法：")
parser.add_argument("-s","--sample",help="获取样例数据，每个文件10条")
parser.add_argument("-w","--watch",help="查看目录文件")
parser.add_argument("-k","--keyword",help="正常输入关键字，用;进行分隔")
parser.add_argument("-kl","--keylist",help="用一个文件输入用;分隔的关键字列表")
parser.add_argument('-d','--database',help='用;分隔要使用的数据库列表，包括netease,gongan,leakmember和一个all')
parser.add_argument('-o','--outfile',help='输出文件')
parser.add_argument('-c','--clean',help='在其它流程完成后，去除目标文件中重复数据')

args = parser.parse_args()
catalog_file='./storage_catalog.txt'

time_all=0
def spsearch(keylist,fn,outf):
	time_start=time.time()
	rsf=open(outf,'w+',encoding='utf8')
	with open(fn,encoding='utf8',errors='ignore') as f:
		print('[*]Start Search for : ',fn)
		data=f.readlines(1000000000)#每次最多读1000M大小数据(似乎要除以50是内存占用量)
		i=1
		while(data!=[]):
			for line in data:
				for key in keylist:
					if(key in line):
						print('[+]Find a line include keyword:',line.strip('\n'))
						rsf.write(line)
			if(i%20000==0):#每20000batch输出一次统计
				time_end=time.time()
				print('[*]Next Search start,time cost:',time_end-time_start)
			i+=1
			data=f.readlines(100000)

	rsf.close()
	print('[*]SEARCH OVER')
	time_end=time.time()
	time_dura=time_end-time_start
	time_all+=time_dura
	print('[*]Time cost:',time_dura)

def sample_get(fn):#获取样例数据
	print('[+]文件数据样例：',fn)
	with open(fn,encoding='utf8',errors='ignore') as f:
		i=0
		while i<5:
			i+=1
			print(f.readline().strip())
	print('-----------------------')

def clean(fn):#清理重复数据
	newlines=[]
	with open(fn, 'r',encoding='utf8') as fo:
		for line in fo.readlines():
			if line not in newlines:
				newlines.append(line)
	with open(fn, 'w',encoding='utf8') as fo:
		for line in newlines:
			fo.write(line)
	print('清理完成：',fn)

def create_dict():#创建目录文件字典
	cdict = {}
	with open(catalog_file, 'r',encoding='utf8') as fo:
		for line in fo.readlines():
			line = line.strip('\n')
			line = line.strip()
			did=line.split(',')[0]
			dpath=line.split(',')[2]
			cdict[did]=dpath
	return cdict

def watch_catalog():
	fo = open(catalog_file, 'r',encoding='utf8')
	for line in fo.readlines():
		line = line.strip()
		print(line)
	fo.close()

#获取交互数据：关键字
if(args.keyword):
	keylist=args.keyword.split(';')
elif(args.keylist):
	kf = open(args.keylist,encoding='utf8')
	keylist=kf.readlines().split(';')
else:
	print('没有关键字，不会进行搜索')

#获取交互数据：数据集
dbpath=[]
if(args.database):
	dblog=[]#从目录获取的db集合
	pathlog=create_dict()#目录获取的path与id字典
	dblist=args.database.split(';')
	if 'all' in dblist:
		dblist=pathlog.keys()
	for dbid in dblist:
		dbpath.append(pathlog[dbid])
else:
	dblog=[]#从目录获取的db集合
	pathlog=create_dict()#目录获取的path与id字典
	dblist=pathlog.keys()
	for dbid in dblist:
		dbpath.append(pathlog[dbid])

#获取交互数据：输出文件

outf='./result.txt'
if(args.outfile):
	outf=args.outfile
else:
	pass

#此处显示目录
if(args.watch):
	watch_catalog()

#此处获取sample
if(args.sample):
	for fpath in dbpath:
		sample_get(fpath)
#此处进行搜索
if(args.keyword or args.keylist):
	for fpath in dbpath:
		spsearch(keylist,fpath,outf)
	print('[*]Time cost totally:',time_all)
#此处进行重复数据清理
if(args.clean):
	clean(outf)