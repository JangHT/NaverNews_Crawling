#-*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import pandas as pd
import csv

class Crawling:
	def __init__ (self):
		self.search_keyword = '부동산'
		
		url = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query={self.search_keyword}'

		#url = f'https://search.naver.com/search.naver?&where=news&query=%EB%B6%80%EB%8F%99%EC%82%B0&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=193&start=21&refresh_start=0'
		r = requests.get(url)
		self.soup = BeautifulSoup(r.text, 'html.parser')

	def get_next_page(self, pars):
		for item in self.soup.select(pars):
			url = f'https://search.naver.com/search.naver' + item['href']
			r = requests.get(url)
			self.soup = BeautifulSoup(r.text, 'html.parser')

			return url
	#기사 제목
	def title(self):
		result = []
		news_titles = self.soup.select('.news .type01 li dt a[title]')
		for title in news_titles:
			result.append(title['title'])
			print("기사제목 :", title['title'])	
		return result


	#기사 Body
	def body(self):
		result = []
		for item in self.soup.findAll('dd'):
			[tag.extract() for tag in item.findAll(class_="relation_lst")]
			[tag.extract() for tag in item.findAll(class_="newr_more")]
			if "strong class" in str(item):
				#newtext = item.replace("&nbsp", "")
				#item.replace_with(newtext)
				result.append(str(item.text.replace(u'\xa0', u' ').\
						replace(u'\u2022', u' ').\
						replace(u'\u2027', u' ')))
				
				#result.append(str(item.text.replace(r"^[\w\s\"\',]", '')))
				print("기사내용 :", str(item.text.replace(u'\xa0', u' ')))
		return result

	#회사 이름
	def company(self):
		result = []
		for item in self.soup.findAll('span',{'class':'_sp_each_source'}):
			[tag.extract() for tag in item.findAll(class_="sprenew api_ico_pick")]
			result.append(item.text)
			print("회사이름 :", item.text)
		return result
	# url
	def url(self):
		result = []
		items = self.soup.select('.news .type01 li dt a[href]')
		for url in items:
			result.append(url['href'])
			print("URL :", url['href'])	
		return result
			
		
	#기사 날짜
	def date(self, nowDatetime):
		result = []
		
		for item in self.soup.findAll('dd',{'class':'txt_inline'}):

			if re.compile('[0-9]*초 전').search(item.get_text()):
				index = re.compile('[0-9]*초 전').search(item.get_text())
				substr = item.get_text()[index.span()[0]:index.span()[1]]
				number = int(re.findall("\d+", substr)[0])
				opday = nowDatetime - timedelta(seconds=number) # 날자계산
			elif re.compile('[0-9]*분 전').search(item.get_text()):
				index = re.compile('[0-9]*분 전').search(item.get_text())
				substr = item.get_text()[index.span()[0]:index.span()[1]]
				number = int(re.findall("\d+", substr)[0])
				opday = nowDatetime - timedelta(minutes=number) # 날자계산
			elif re.compile('[0-9]*시간 전').search(item.get_text()):
				index = re.compile('[0-9]*시간 전').search(item.get_text())
				substr = item.get_text()[index.span()[0]:index.span()[1]]
				number = int(re.findall("\d+", substr)[0])
				opday = nowDatetime - timedelta(hours=number) # 날자계산
			elif re.compile('[0-9]*일 전').search(item.get_text()):
				index = re.compile('[0-9]*일 전').search(item.get_text())
				substr = item.get_text()[index.span()[0]:index.span()[1]]
				number = int(re.findall("\d+", substr)[0])
				opday = nowDatetime - timedelta(days=number) # 날자계산
			else : # DATE
				match = re.search(r'\d{4}.\d{2}.\d{2}', text)
				if index :
					opday = datetime.strptime(match.group(), '%Y-%m-%d').date()
				else :
					continue;
			opday = opday.strftime('%Y-%m-%d %H:%M:%S')
			result.append(opday)
			print(item.get_text(), opday)
		return result
		
	def file_write(self, i, insert_data):
		
		rowdata = {}
		length = [len(insert_data['title']), len(insert_data['body']), 
			len(insert_data['company']), len(insert_data['date']), 
			len(insert_data['url'])]
		length.sort()
		
		f = open('mycsvfile.txt', 'a', newline='\n')
		w = csv.DictWriter(f, rowdata.keys())
			
		#w.writeheader()
		
		for i in range(length[0]):
			rowdata['title'] = insert_data['title'][i]
			rowdata['body'] = insert_data['body'][i]
			rowdata['company'] = insert_data['company'][i]
			rowdata['date'] = insert_data['date'][i]
			rowdata['url'] = insert_data['url'][i]
			
			#print(rowdata)
			print(len(insert_data['title']))
			print(len(insert_data['body']))
			print(len(insert_data['company']))
			print(len(insert_data['date']))
			print(len(insert_data['url']))
			print(insert_data['body'][i])
			w.writerow(rowdata)
		f.close()
		'''
		with open('news_data.csv', 'a') as outfile:
				
			writer = csv.writer(outfile)
			writer.writerow(insert_data.keys())
			writer.writerows(zip(*insert_data.values()))
			outfile.close()
		'''

		
if __name__ == '__main__':
	input_file = csv.DictReader(open("mycsvfile.txt"))
	for row in input_file:
		print(row['url'])
'''
	f = open('mycsvfile.csv', 'r')
	rdr = csv.reader(f)
	for line in rdr:
		print(line)
	f.close()    
'''
'''
	craw = Crawling()	
	nowDatetime = datetime.now()
	insert_data = {}
	n = 20
	for i in range(n): #n번째 Page에 있는 뉴스까지 보겠다 (개수 : n * 10)
		insert_data['title'] = craw.title()
		insert_data['body'] = craw.body()
		insert_data['company'] = craw.company()
		insert_data['date'] = craw.date(nowDatetime)
		insert_data['url'] = craw.url()
		
		craw.get_next_page('.news .paging .next')
	#print(insert_data['title'][0])
		print(i)
		craw.file_write(i, insert_data)
	print('Process Time : ' + datetime.now() - nowDatetime)
'''
