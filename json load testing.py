#Earl White
#Data Mining Project, Test File
#1000882451

import json


class Test_junk:
    def __init__(self):
        #Opens every data file and builds a dictionary of dictionaries for each of them. The Business, Reviews, and Users dictionaries have keys equal to their
        #respective ID's. The Tips 
        Businesses={}
        Reviews={}
        Tips={}
        Users={}
        
        #Businesses. "attributes" (A dictionary of a bunch of attributes which may or may not be present), "business_id" (should be key in dictionary)
        #"categories"(set of strings), "city", "full_address" (basically immaterial), "hours"(dictionary with up to 7 day-of-week entries, each of which is a
        #dictionary with "open" and "close" entries), "latitude", "longitude", "name", "neighborhoods" (a set), "open", "review_count", "stars", "state", "type"
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json','r')
        
        #Checkins. "business_id", "checkin_info" (a dictionary consisting of a series of things I don't actually understand, associated with numbers)
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_checkin.json','r')
        #Reviews, almost 1,570,000. "business_id", "date", "review_id" (use as key), "stars" (class variable?), "text", "type", "user_id",
        #"votes" (dictionary with "cool", "funny", "useful" entries)
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json','r')
        #Tips. About 495K entries. "business_id", "date", "likes", "text", "type", "user_id"
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_tip.json','r')
        #Contains user data, about 360K entries. "average_stars", "compliments" (Dictionary), "elite" (set), "fans", "friends" (set), "name", "review_count", "type",
        #"user_id" (should be used as dictionary key), "votes"(dictionary with "cool", "funny", "useful" entries), "yelping_since"
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_user.json','r')
        
        
        
        filestrings=file.readlines()
        #print(filestrings)
        count=0
        for line in filestrings:
            count=count+1
            filedic=json.loads(line)
            if filedic["likes"]>3:#count%1000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))
            #print(str(count) + ',' + json.dumps(filedic))
        

Stuff = Test_junk()

