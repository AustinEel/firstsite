#!/usr/bin/python
"""Converter Tool from txt file to html for BSA"""

from time import localtime, strftime
from unidecode import unidecode
import sys, csv, os
import codecs

def print_error(msg):
	"""
	prints custom error messages

	:input:
		message (string)
	"""
	sys.stderr.write(msg)
	sys.exit(1)

def add_p(msg):
	"""
	returns message wrapped in paragraph tags and adds new lines

	:input:
		message (string)
	"""
	return '<p>{}</p>\n\n'.format(msg)

def print_cover(title, authors, my_date, cov_par):
	"""
	runs front matter to html post

	:input:
		title (string)
		author (currently just one)
		date (gathered from txt doc)
		cover_paragraph (string)
	"""
	body = '---\n'\
			'layout: post\n'\
			'title: \"{}\"\n'\
			'date: {} -0700\n'\
			'authors:\n'.format(title, my_date)
	for author in authors:
		body += '- {}\n'.format(author)

	body += 'categories: jekyll update\n'\
			'excerpt_separator: <!-- end excerpt here -->\n'\
			'excerpt: '
	body += '<center><img class=\"excerptpics\" src =\"/assets/pic_folder/photo\" alt=\"cover photo\"></center>'
	body += '<p>{}</p>\n'.format(cov_par)
	body += '---\n'
	return body


def add_pic(num):
	"""
	adds appropriate picture tags and marks the picture number

	:input:
		picture number (int)
	"""
	return '<figure>\n\t<center><img class=\"excerptpics\" src =\"/assets/pic_folder/pic_{}\" alt=\"picture {}\"><figcaption></figcaption></center>\n</figure>\n\n'.format(num, num)


def main():
	"""
	Converts txt file to html

	:input:
		txt file (file)
		number of pictures (int)
	"""
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
	
	# add cover photo
	body += '<figure>\n\t<center><img class=\"excerptpics\" src =\"/assets/pic_folder/photo\" alt=\"cover photo\"><figcaption></figcaption></center>\n</figure>\n\n'
	# wrap the rest
	for i in range(4, len(content)):
		if content[i]:
			body += add_p(unidecode(content[i]))
	
	# set up picture frames
	num_pics = int(sys.argv[2])
	for i in range(1,num_pics+1):
		body += add_pic(i)

	# write changes to new html file
	out = open('{}.html'.format(file_name),'w')
	out.write(body)

	# close file descriptors
	f.close()
	out.close()
	

if __name__ == '__main__':
	main()