#! /usr/bin/env python
# encoding=utf8

import tweepy as tp
from time import sleep
import random
import requests
from os import listdir
from os.path import isfile, join

count = 0


class Bot:
        def __init__(self):
                credentials = []
                infile = open("credentials","rb")
                for line in infile:
                        credentials.append(line)
                infile.close()
                
                self.DONT_TWEET = False
                self.KEYWORD = ['urban planning','sustainable','sustainability','urban policy', 'sustainable urban', 
                'environmental policy', 'environmental planning', 'food systems planning', 'environmental design', 
                'city planning', 'regional planning', 'metropolitan planning', 'rural planning', 'new urbanism']
                
                self.GREETING = ['Good job!','Awesome!','Cool!', 'Amazing!', 'Lovely!', 'Nice work!', 'Wow! Amazing!', 
                'Really interesting','You’ve got to check this out', 'Awesome','I love it!','Great project!',
                'Love to learn more about this','GOAT!','So lit!','So Gucci!', 'Love this project', 
                'I did something just like this in grad school! Love it!', 'I worked on something similar at my old job. Very cool.']
                
                self.GREET_QUERY = ['research','project', 'gorgeous', 'lovely','interesting', 'amazing', 
                'honor', 'honored', 'glad', 'happy', 'impressive', 'impressed', 'good work', 'encouraged', 
                'fascinating', 'fascinated', 'love','joy', 'great', 'delighted','delight']
                
                self.GREET_NON_REPLY = ['Interesting', 'Nice', "That's cool", 'Really interesting' , 
                'hmmm...']
                
                self.IMAGE_DESCRIPTION = ["Interesting, ","You've got to see this: ", "Love this stuff! ", 
                "Not what I expected: ", "Fun: ", "Lovely! ", "Have you seen this? ", "You've got to see this! ", 
                'Wow! ', 'OK… ', 'Oh… ', 'Not what I expected.  ', 'Can you believe it? ', 'Not really what it seems. ', 
                 'Appearances can be deceiving. ', "You can't look away. ", 'Try to look away. ', 'Makes you wonder… ', 
                 'Why not? ', 'Can you see that? ', 'Look at this! ']
                
                self.SAD_QUERY = ['poor', 'unfortunate','irresponsible','bad','sad', 'evil', 'destroy']    
                
                self.SAD_REPLY = ["That's sad", "That's unfortunate", "Sad", "Too bad"]
                
                self.AVOID_WORDS = ['conservative', 'liberal', 'republican', 'democrat', 'progressive', 'alt-right', 
                'right-wing', 'left-wing', 'far right', 'leftist', 'trump', 'trumpian', 'politics', 'political', 
                'jesus', 'slavery', 'marxist', 'lenin', 'slave', 'christ', 'religious', 'religion', 'devil', 'satan', 
                'pagan', 'anal', 'anus','arse','ass','ballsack','balls','bastard','bitch','biatch','bloody','blowjob',
                "blow job","bollock","bollok","boner",'boob',"bugger","bum","butt",'buttplug','clitoris','cock','coon',
                'crap','cunt','damn','dick','dildo','dyke','fag','feck','fellate','fellatio','felching','fuck','f u c k',
                'fudgepacker','fudge packer','flange','Goddamn','God damn','hell','homo','jerk','jizz','knobend',
                'knob end','labia','lmao','lmfao','muff','nigger','nigga','omg','penis','piss','poop','prick','pube',
                'pussy','queer','scrotum','sex','shit','s hit','sh1t','slut','smegma','spunk','tit','tosser','turd','twat',
                'vagina','wank','whore','wtf']
                
                self.follow_count = 0;
                self.CONSUMER_KEY = credentials[0].rstrip()
                self.CONSUMER_KEY_SECRET = credentials[1].rstrip()
                self.ACCESS_TOKEN = credentials[2].rstrip()
                self.ACCESS_TOKEN_SECRET = credentials[3].rstrip()
                self.api = self.authenticate()
                self.subscription_key = "a93af90b5b03496ebb9d3032e567dde3"
                self.vision_base_url = "https://eastus.api.cognitive.microsoft.com/vision/v2.0/"
                self.images_path = "/home/ubuntu/TwitterBot/TwitterBot-for-Urban-Attitudes-Lab/images/"
                self.image_directory_names=["urban/", "people/","Design/","environment/", "FinancialPlanning/",
                "food/", "metropolitan/", "policydebate/", "sustainability/", "urban/", "urban_planning/"]
                
        def authenticate(self):
                auth = tp.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_KEY_SECRET)
                auth.set_access_token(self.ACCESS_TOKEN, self.ACCESS_TOKEN_SECRET)
                api = tp.API(auth)
                
                try:
                        api.verify_credentials()
                
                except:
                        print "Unable to authenticate"
                        
                else:
                        print "Authenticated"
                        return api
                        
        def analyze_image(self):
                assert(self.subscription_key)
                analyze_url = self.vision_base_url+"analyze"
                directory = self.image_directory_names[random.randint(0,len(self.image_directory_names)-1)]
                path = self.images_path + directory
                image_array = [f for f in listdir(path) if isfile(join(path, f))]
                chosen_image = image_array[random.randint(0,len(image_array)-1)]
                chosen_image = path + chosen_image
                
                image_data = open(chosen_image, "rb").read()
                headers    = {'Ocp-Apim-Subscription-Key': self.subscription_key,
                              'Content-Type': 'application/octet-stream'}
                params     = {'visualFeatures': 'Categories,Description,Color'}
                response = requests.post(
                    analyze_url, headers=headers, params=params, data=image_data)
                response.raise_for_status()
                
                analysis = response.json()
                image_caption = analysis["description"]["captions"][0]["text"].capitalize()
                
                return chosen_image, image_caption
                
                
                
                        
                        
        
        def retweet_keyword(self):
                followed = False
                picture_posted = False
                global count
                key_index = random.randint(0,len(self.KEYWORD)-1)
                
                image, description = self.analyze_image()
                message = self.IMAGE_DESCRIPTION[random.randint(0,len(self.IMAGE_DESCRIPTION)-1)] + description + "."
                self.api.update_with_media(image, status=message)
                sleep(14400)
                for tweet in tp.Cursor(self.api.search, q=self.KEYWORD[key_index], tweet_mode = 'extended').items(15):
                        try:                                                                        
                                if not tweet.favorited:
                                        tweet.favorite()
                                
                                if self.follow_count >=3:
                                        if not followed:
                                                if not tweet.user.following:
                                                        tweet.user.follow()
                                                        self.follow_count = 0;
                                                        followed = True
                                
                                tweet_content = tweet.full_text
                                tweet_content = tweet_content.lower()
                                
                                greet_index = random.randint(0,len(self.GREETING)-1)
                                
                                if not tweet.retweeted:                                        
                                        found = False
                                        
                                        for word in self.BAD_WORD:
                                                if tweet_content.find(word) != -1:
                                                        self.DONT_TWEET = True
                                        
                                        if not self.DONT_TWEET:
                                                for word in self.GREET_QUERY:
                                                        if tweet_content.find(word) != -1:
                                                                count = count + 1
                                                                reply = self.GREETING[greet_index] + ' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                self.api.update_status(status = reply)
                                                                found = True
                                                                break
                                                
                                                if not found:
                                                        if count < 3:
                                                                sad_index = random.randint(0,len(self.SAD_REPLY)-1)
                                                                for sad_word in self.SAD_QUERY:
                                                                        if tweet_content.find(sad_word) != -1:
                                                                                reply = self.SAD_REPLY[sad_index] + ' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                                self.api.update_status(status = reply)
                                                                                break
                                                if not found:                                                                                               
                                                        if count < 2:
                                                                if greet_index%6 == 0:
                                                                        non_greet_index = random.randint(0,len(self.GREET_NON_REPLY)-1)
                                                                        rep = self.GREET_NON_REPLY[non_greet_index]+' https://twitter.com/'+tweet.user.screen_name+'/status/'+tweet.id_str
                                                                        self.api.update_status(status = rep)
                                                                        count = count + 1
                                                                else:
                                                                        tweet.retweet()
                                                                
                                                        else:
                                                                tweet.retweet()
                                        
                                        self.DONT_TWEET = False
                                sleep(14400)
                                
                        except tp.TweepError as e:
                                print(e.reason)
                        
                self.follow_count+=1;
                        
mybot = Bot()
while True:
        mybot.retweet_keyword()
        count = 0
        sleep(36000)















'''
credentials = []
inFile = open("credentials","r")
for line in inFile:
        credentials.append(line)

        
for x in credentials:
        print x
'''
