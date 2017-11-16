#! /usr/bin/env python
# -*- coding: utf-8 -*-
#python get_score.py --key putkeyInHere --secret PutSecreteKeyHere --name content.txt
#
import argparse
import json
import random
import re

import requests
from os.path import isfile, join


def v(verbose, text):
    if verbose:
        print text


class Receptiviti():
    def __init__(self, server, api_key, api_secret, verbose=False):
        """
        initialise a Receptiviti object

        :type server: str
        :type api_key: str
        :type api_secret: str
        """

        self.server = server
        self.api_key = api_key
        self.api_secret = api_secret
        self.verbose = verbose

    def get_person_id(self, person):
        v(self.verbose, 'getting person: {}'.format(person))
        headers = self._create_headers()
        params = {
            'person_handle': person
        }
        response = requests.get('{}/v2/api/person'.format(self.server), headers=headers, params=params)
        
        if response.status_code == 200:
            matches = response.json()
            if len(matches) > 0:
                return matches[0]['_id']
        return None

    def _create_headers(self, more_headers={}):
        headers = dict()
        headers.update(more_headers)
        headers['X-API-KEY'] = self.api_key
        headers['X-API-SECRET-KEY'] = self.api_secret
        return headers

    def create_person(self, person):
        v(self.verbose, 'creating person: {}'.format(person))
        headers = self._create_headers({'Content-Type': 'application/json', 'Accept': 'application/json'})
        data = {
            'name': person,
            'person_handle': person,
            'gender': 0
        }
        response = requests.post('{}/v2/api/person'.format(self.server), headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print (response.status_code)
            v(self.verbose, 'Http Response: {}'.format(response))
            raise Exception("Creating person failed!")

        return response.json()['_id']

    def add_content(self, person_id, content):
        v(self.verbose, 'add content for {}'.format(person_id))
        headers = self._create_headers({'Content-Type': 'application/json', 'Accept': 'application/json'})
        data = {
            'language_content': content,
            'content_source': 8
        }
        response = requests.post('{}/v2/api/person/{}/contents'.format(self.server, person_id), headers=headers,
                                 data=json.dumps(data))

        if response.status_code != 200:
            print (response.status_code)
            raise Exception("Adding content failed!")

        return response.json()['_id']

    def get_profile(self, person_id):
        v(self.verbose, 'get profile for {}'.format(person_id))

        headers = self._create_headers({'Accept': 'application/json'})
        response = requests.get('{}/v2/api/person/{}/profile'.format(self.server, person_id), headers=headers)
        
        # Here is where to get those score
        # print(response.json())
        
        s2 = json.loads(response.content)
        #print( s2['receptiviti_scores']['percentiles']['cheerful'])
        #print( s2['receptiviti_scores']['percentiles']['happiness'])
        #print( s2['receptiviti_scores']['percentiles']['depression'])
        #print( s2['receptiviti_scores']['percentiles']['stressed'])

        pos = float(s2['receptiviti_scores']['percentiles']['cheerful']) + float(s2['receptiviti_scores']['percentiles']['happiness'])
        #print ('The positive index is {}'.format(pos/2))
        neg = float(s2['receptiviti_scores']['percentiles']['depression']) + float(s2['receptiviti_scores']['percentiles']['stressed'])
        #print ('The negative index is {}'.format(neg/2))

        #(1) --------------------------------------This function is for outputing the .txt   
        '''pos_string = 'The negative index is {}\n'.format(pos/2)
        f.write(pos_string) 
        neg_string = 'The negative index is {} \n'.format(neg/2)
        f.write(neg_string) 
        f.write('\n') '''

        #json.dump(s2['receptiviti_scores']['percentiles'], fp, indent=4)

       
        if response.status_code != 200:
            raise Exception("Get profile failed!")
        return response.json()

    def get_content(self, content_id):
        v(self.verbose, 'get profile for {}'.format(content_id))
        headers = self._create_headers({'Accept': 'application/json'})
        response = requests.get('{}/v2/api/content/'.format(self.server, content_id), headers=headers)
        print(response)
        if response.status_code != 200:
            raise Exception("Get profile failed!")
        return response.json()


    def get_liwc_score(self, person_name, person_contents):
        person_id = self.get_person_id(person_name)
        if person_id is None:
            
            person_id = self.create_person(person_name)
        for content in person_contents:
            self.add_content(person_id, content)
            
        return self.get_profile(person_id)


# -------------------------------------- This is to read an .txt file and interpret the result
'''def get_person_contents():
    dir_path = os.path.join(os.path.dirname(__file__), 'content')
    content_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(".txt")]
    person_contents = []
    for content_file in content_files:
        with open(content_file, "r") as the_file:
            person_contents.append(the_file.readlines())

    return person_contents'''

def get_tweet_content(content):
    tweet_contents = []
    tweet_contents.append(content)

    return tweet_contents



if __name__ == '__main__':
    import os
    from os import listdir

    description = '''Get the Communication Recommendation for a Person.'''

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--server', type=str, help='server to use for analysis', default='https://app.receptiviti.com')
    parser.add_argument('--verbose', '-v', help='verbose output', action='store_true')
    parser.add_argument('--key', type=str, help='API key')
    parser.add_argument('--secret', type=str, help='API secret key')
    parser.add_argument('--name', type=str, help='Person name', default="Justin Chen")

    args = parser.parse_args()

    args.key = 'paste your key here'
    args.secret = 'paste your secret key here'
    
    
    tweets = []
    receptiviti = Receptiviti(args.server, args.key, args.secret, args.verbose)
    x =0
    

    # (1) -------------------------------------- This function is for outputing the .txt  
    '''f = file('result.txt','w')
    with open('tweet.txt', "r") as my_file:
        for line in my_file:
            x = x+1
            print(x)
            f.write('{}'.format(line))             
            receptiviti.get_liwc_score(args.name, get_tweet_content(line))'''

    

    with open('library1.json', 'w') as fp:
        fp.write('[')
        with open('library1.txt', 'r') as my_file:
            for line in my_file:
            
                x = receptiviti.get_liwc_score(args.name, get_tweet_content(line))
        
            # Here I add the original tweet into json  
                x['receptiviti_scores']['percentiles']['tweet'] = line
                json.dump( x['receptiviti_scores']['percentiles'], fp, indent=4)
                fp.write(',')
            #print x['receptiviti_scores']['percentiles']['cheerful']
            #print x['receptiviti_scores']['percentiles']['happiness']
            #print x['receptiviti_scores']['percentiles']['depression']
            #print x['receptiviti_scores']['percentiles']['stressed']
                pos = x['receptiviti_scores']['percentiles']['cheerful'] + x['receptiviti_scores']['percentiles']['happiness']
                print ('The positive index is {}'.format(pos/2))
                neg = x['receptiviti_scores']['percentiles']['depression'] + x['receptiviti_scores']['percentiles']['stressed']
                print ('The negative index is {}\n'.format(neg/2))

    with open('library1.json', 'rb+') as filehandle:
            filehandle.seek(-1, os.SEEK_END)
            filehandle.truncate()
            filehandle.write(']')     
            

    my_file.close() 
        
    
    
        

    




    