#Earl White
#Data Mining Project, Test File
#1000882451

import json


class Test_junk:
    def __init__(self):
        #Opens every data file and builds a dictionary of dictionaries for each of them. The Business, Reviews, and Users dictionaries have keys equal to their
        #respective ID's. The Tips have both business and userID and that's it.
        Reviews={}
        Businesses={}
        Users={}
        Tips={}
        Checkins={}

        
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json','r')
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            count=count+1
            filedic=json.loads(line)
            #Only loading about 1/8th of all businesses in database.
            if count<8000:
                Businesses[filedic['business_id']] = filedic
            #Businesses.append(filedic)
            if count%10000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))

        
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json','r')        
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            filedic=json.loads(line)
            #Only add review if about business we're loading.
            #About 160,000 reviews.
            if filedic['business_id'] in Businesses:
                Reviews[filedic['review_id']] = filedic
                count=count+1
            if count%10000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))
       
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_user.json','r')
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            count=count+1
            filedic=json.loads(line)
            #360K users, because can't readily tell if a user has made a review in the subset I picked.
            Users[filedic['user_id']] = filedic
            if count%10000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))
                
                
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_tip.json','r')
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            filedic=json.loads(line)
            #Only adding tips about uploaded businesses.
            #Have about 50K tips from that.
            if filedic['business_id'] in Businesses:
                if filedic['business_id'] not in Tips:
                    Tips[filedic['business_id']] = []
                Tips[filedic['business_id']].append(filedic)
                count=count+1
            #Tips.append(filedic)
            if count%10000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))                
                
                
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_checkin.json','r')
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            filedic=json.loads(line)
            #Checkins only has one entry per business ID.
            #And we only add it if we've uploaded the business.
            if filedic['business_id'] in Businesses:
                Checkins[filedic['business_id']] = filedic
                count=count+1
            if count%10000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))


        #So, I need to build a knowledge base for everything associated with a given review.
        #For not-always-populated fields, I'll have the classifier automatically split off empty values, assuming non-applicability.
        #Review Proper
         #Date (separate by year? Must be split from review date field)
         #Text (must be textually evaluated)
         #Votes (Total, and Cool/Funny/Useful subtotals)
        #Review Business
         #Address State (must be split from business address field)
         #Address Zip (must be split from business address field)
         #Address City (must be split from business address field)
         #hours (not always populated, has per-day subfields. Just make included/not included maybe?)
        #Review User
        
        #User Tips (Organization: By business_id?)
        
        #Business Checkins
         #Count of checkins for a business.
        
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
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_tip.json','r')
        #Contains user data, about 360K entries. "average_stars", "compliments" (Dictionary), "elite" (set), "fans", "friends" (set), "name", "review_count", "type",
        #"user_id" (should be used as dictionary key), "votes"(dictionary with "cool", "funny", "useful" entries), "yelping_since"
        #file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_user.json','r')
        
        
        
        #filestrings=file.readlines()
        #print(filestrings)
        #count=0
        #for line in filestrings:
        #    count=count+1
        #    filedic=json.loads(line)
        #    if count%10000==0: #filedic["likes"]>3:
        #        print(count)
        #        print(json.dumps(filedic,sort_keys=True, indent=3))
            #print(str(count) + ',' + json.dumps(filedic))
        

Stuff = Test_junk()

