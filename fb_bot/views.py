# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import pprint
import requests
import random

# graph api
PAGE_TOKEN = 'EAAV3aM9dle4BAJ9Tik1qbQLXmZBJK3JUEM9bpG5BaIYTTc4NboTLZAEP3ZAchLMoC4ORzaAj3nxO27IbZADy1Vcg9ra1lfOhisErJT3NOlSt5I1DZAWbWq3MoxWmSFkuY9omDhuBOZB8C3xSVkUQFEkGKNjr4GmMB9ciz1ZCsAfHQZDZD'
VERIFY_TOKEN = 'super-secret'

GAME_STATE = False
ANSWER_MODE = False
ANSWER_INDEX = 999999
question_list = []
with open('fb_bot/questions.json') as data_file:    
    data = json.load(data_file)
for i in data:
	question_list.append(i['question'])


class webhook(generic.View):
    def get(self, request, *args, **kwargs):
    	# To Verify Token
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
            	if 'message' in message:
            		if not ANSWER_MODE:
                		if message['message']['text'] != '/game'and GAME_STATE != True:
                			send_message(message['sender']['id'], message['message']['text'])
                		else:
                			game(message['sender']['id'], message['message']['text'])
	                else:
	                	answer(message['sender']['id'], message['message']['text'])
        return HttpResponse()

def send_message(usr_id, msg):	
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
	response_msg = json.dumps({"recipient":{"id":usr_id}, "message":{"text": translate_word(msg)}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def send_message2(usr_id, msg):	
	post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + PAGE_TOKEN
	response_msg = json.dumps({"recipient":{"id":usr_id}, "message":{"text": msg}})
	status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)

def translate_word(word):
	if not (len(word.split(' ')) > 1):
		url = 'https://api.pearson.com/v2/dictionaries/ldoce5/entries?headword='+ word +'&apikey=D9cmWQXuTuHgxqWxIysJbAONhdd1CyY9'
		results = requests.get(url).json()['results']
		try:
			return results[0]['senses'][0]['definition'][0]
		except (KeyError, IndexError) as e:
			return "I didn't got what you meant?  try another!"
	else:
		return "I didn't got what you meant?  try another!"

def game(usr_id, msg):
	global GAME_STATE,  ANSWER_MODE, ANSWER_INDEX
	print('game function called!')
	GAME_STATE = False
	question = random.choice(question_list)
	for i in data:
		if  i['question'] == question:
			choices = i['choices']
			ANSWER_INDEX = i['correctanswer']
			print(ANSWER_INDEX, type(ANSWER_INDEX))
			break
	choice_str = ''
	for i in choices:
		choice_str += str(choices.index(i)) + ' ' + i + '\n'
	send_message2(usr_id, question + '\n\n' + choice_str)
	ANSWER_MODE = True
	return 0
def answer(user_id, msg):
	global  ANSWER_MODE, ANSWER_INDEX
	print(ANSWER_INDEX, type(ANSWER_INDEX))
	try:
		msg = int(msg)
	except ValueError:
		msg = msg
	print(msg)
	if ANSWER_INDEX in [0,1,2,3]:
		if msg == ANSWER_INDEX:
			send_message2(user_id,'you are correct!!')
		else:
			send_message2(user_id,'your answer was wrong,  correct one is option' + str(ANSWER_INDEX))
		ANSWER_MODE = False
		ANSWER_INDEX = 999999
	else:
		send_message2(user_id,'please type correct options [0,1,2,3]')


# def game_exit():
# 	global 
# 	return 0
