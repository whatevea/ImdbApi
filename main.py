import requests
from bs4 import BeautifulSoup as bs 
from flask import Flask,jsonify,request
posterHeight=1000
posterWidth=675
def episodesOf(imdbcode,season):
	url=f"https://www.imdb.com/title/{imdbcode}/episodes?season={season}"
	html=requests.get(url).text
	soup=bs(html,'html.parser')
	divs=soup.find_all('div',{'class':'list_item'})
	Fullresult=[]
	for item in divs:
		image=item.img['src']
		title=item.img['alt']
		info=item.find('div',{'class':'item_description'}).text
		result={"image":image,"title":title,"info":info}
		Fullresult.append(result)
	return Fullresult
def addHeaders(response):
	response.headers.add('Access-Control-Allow-Origin', '*')
	response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
	response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
	return response
def getItems(imdbcode):
	html=requests.get(f'https://www.imdb.com/title/{imdbcode}/').text
	soup=bs(html,'html.parser')
	imgLink=(soup.find('div',{'class':'poster'})).img['src'].split('_V1_')[0]+f"_V1_SY{posterHeight}_SX{posterWidth}_AL_.jpg"
	nameYear=(soup.find('div',{'class':'title_wrapper'}).h1.text).replace('\\xa0'," ")
	plot=soup.find('div',{'class':"summary_text"}).text
	latestSeason=soup.find('div',{'class':'seasons-and-year-nav'})
	rating=soup.find('span',{'itemprop':'ratingValue'}).text
	print(latestSeason)
	if latestSeason==None:
		latestSeason=False
	else:
		latestSeason=latestSeason.a.text
	return {"Image":imgLink,"nameYear":nameYear,"plot":plot,"latestSeason":latestSeason,"rating":rating}

def search(query):
	url=f'https://v2.sg.media-imdb.com/suggestion/{str.lower(query[0])}/{query}.json'
	items=requests.get(url).json()['d']
	Fullresult=[]
	for item in items:
		result={}
		try:
			result.update({'image':item['i']['imageUrl']})
			result.update({'imdbcode':item['id']})
			result.update({'title':item['l']})
			result.update({'year':item['y']})
			result.update({'starring':item['s']})
			Fullresult.append(result)
		except:
			pass
	return Fullresult

app=Flask(__name__)
@app.route('/')
def start():
	return "hello world"

#                Series/movies details
@app.route('/details',methods=['POST','GET'])
def imdb():
	if request.method=='POST':
		return "get methods"
	if request.method=="GET":
		imdbcode=request.args['imdbcode']
		response= addHeaders(jsonify(getItems(imdbcode)))
		return response

@app.route('/episodes')
def episodes():
	imdbcode=request.args['imdbcode']
	season=request.args['season']
	return addHeaders(jsonify(episodesOf(imdbcode,season)))

# search result
@app.route('/search')
def search_function():
	query=request.args['query']
	response=jsonify(search(query))
	return(addHeaders(response))
app.run(debug=True,port=8080)
