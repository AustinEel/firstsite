#!/usr/bin/python
from time import localtime, strftime
from unidecode import unidecode
import sys, csv, os
import codecs

def print_error(msg):
	sys.stderr.write(msg)
	sys.exit(1)

def add_p(msg):
	return '<p>{}</p>\n\n'.format(msg)

def print_cover(title, author, my_date, cov_par):
	body = '---\nlayout: post\ntitle: '
	body += '\"{}\"\ndate: {} -0700\nauthor: {}\n'.format(title,my_date,author)
	body += 'categories: jekyll update\nexcerpt_separator: <!-- end excerpt here -->\nexcerpt: '
	body += '<center><img class=\"excerptpics\" src =\"/assets/pic_folder/photo\" alt=\"cover photo\"></center>'
	body += '<p>{}</p>\n'.format(cov_par)
	body += '---\n'
	body += '<figure>\n\t<center><img class=\"excerptpics\" src =\"/assets/pic_folder/photo\" alt=\"cover photo\"><figcaption></figcaption></center>\n</figure>\n\n'
	return body


def add_pic(num):
	return '<figure>\n\t<center><img class=\"excerptpics\" src =\"/assets/pic_folder/pic_{}\" alt=\"picture {}\"><figcaption></figcaption></center>\n</figure>\n\n'.format(num, num)


def main():
	if (len(sys.argv) != 3):
		print_error("Incorrect number of arguments\n")

	# read in unicode
	with codecs.open(sys.argv[1],'r','utf-8') as f:
		content = f.readlines()
	content = [x.strip() for x in content] # get rid of \n
	content[0] = content[0].replace(u'\ufeff','') # get rid of \ufeff
	
	title = content[0].split("Title: ",1)[1]
	author = content[1].split("Author: ",1)[1]
	my_date = strftime("%Y-%m-%d %H:%M:%S", localtime())
	file_name = f.name.split(".txt",1)[0]
	# get cover paragraph
	for i in range(3, len(content)):
		if content[i]:
			cov_par = unidecode(content[i])
			break

	body = print_cover(title, author, my_date, cov_par)
	
	# wrap the rest
	for i in range(4, len(content)):
		if content[i]:
			body += add_p(unidecode(content[i]))
	
	# set up picture frames
	num_pics = int(sys.argv[2])
	for i in range(num_pics):
		body += add_pic(i+1)

	# write changes to new html file
	out = open('{}.html'.format(file_name),'w')
	out.write(body)

	# close file descriptors
	f.close()
	out.close()
	

if __name__ == '__main__':
	main()