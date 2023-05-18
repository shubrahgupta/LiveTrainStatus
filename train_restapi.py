from bs4 import BeautifulSoup
from flask import Flask, abort, request, jsonify
from requests import get
from json import loads
import pandas as pd
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
	return 'Train Running Status'


@app.errorhandler(404)
def pageNotFound(e):
	print(e)
	return "Error 404, Page not found."


@app.route('/<train>', methods=["GET"])
def train_running_staus(train:str)->str:
	URL = "https://www.ixigo.com/trains/"
	URL += str(train)
	URL += "/running-status"
	webpage = requests.get(URL)

	soup = BeautifulSoup(webpage.content, "html.parser")

	status = soup.find('div', attrs={'class':'overall-delay red'})
	origin = soup.find('div', attrs={'class':'date-item u-ib selected'})
	info = {"train" : None, "origin": None,"status": None}
	if status == None:
		status = "Not started yet"
		info["train"] =  train 
		info["origin"]= origin.text[-10:]
		info["status"]= status
	else:
		info["train"] =  train 
		info["origin"]= origin.text[-10:]
		info["status"]= status.text
		


	return info



if __name__ == '__main__':
	app.run()