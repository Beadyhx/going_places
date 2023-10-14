import requests
import json
import config
import wget
import os

APIKEY = config.APIKEY

def getphotos(APIKEY, placeid, coords):
	url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}'.format(placeid, APIKEY)
	response = requests.get(url)
	photosjson = json.loads(response.text)
	for result, resultvalues in photosjson['result'].items():
		if result == 'name':
			name = resultvalues
			forbidden = ['<','>',':','"','/','\\','|','&','*']
			for symbol in forbidden:
				name = name.replace(symbol, '')
		if result == 'photos':
			os.mkdir('./{}/{}'.format(coords,name))
			n = 1
			photocounter = 0
			for photo in resultvalues:
				photocounter += 1
			print('Found {} photos of {}, downloading...'.format(photocounter, name))
			for photo in resultvalues:
				maxwidth = photo['width']
				photoref = photo['photo_reference']
				url = 'https://maps.googleapis.com/maps/api/place/photo?maxwidth={}&photoreference={}&sensor=true&key={}'.format(maxwidth, photoref, APIKEY)
				wget.download(url, './{}/{}/{}_{}.jpeg'.format(coords, name, name, n))
				print('\n {} of {} photos downloaded........'.format(n,photocounter), end='\r')
				n += 1


def getplaces(APIKEY, respjson, coords):
	try:
		if respjson['status'] == 'ZERO_RESULTS':
			print('ZERO_RESULTS')
		elif respjson['status'] == 'INVALID_REQUEST':
			print('Invalid request, check your coordinates, it must be in google format, like 12.12345678, 12.87654321')
		else:
			print('Found places:')
			for i in respjson['results']:
				isphotos = False
				name = i['name']
				if 'photos' in i:
					isphotos = True;
				if isphotos == True:
					print(i['name'])
				else:
					print(i['name']+' (NO PHOTOS)')
			for i in respjson['results']:
				placeid = i['place_id']
				getphotos(APIKEY, placeid, coords)
	except KeyError:
		print('Some really strange error happened while handling Google json response')


def getjson(APIKEY, coords, radius):
	os.mkdir('./{}'.format(coords))
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={}&radius={}&fields=photo&key={}'.format(coords, radius, APIKEY)
	response = requests.get(url)
	respjson = json.loads(response.text)
	getplaces(APIKEY, respjson, coords)

print('Hello! I will find for you photos of places from Google maps. All you need is to specify coordinates in "Google" format (for example, 12.12345678, 12.8765432) and radius of search (use with caution in large cities)\n')
coords = input('Give me coordinates: ').replace(' ', '')
radius = input('Now specify search radius: ')
getjson(APIKEY, coords, radius)
