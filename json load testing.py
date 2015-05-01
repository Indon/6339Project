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
            if count%1000==0:
                print(count)
                print(json.dumps(filedic,sort_keys=True, indent=3))


        #So, I need to build a knowledge base for everything associated with a given review.
        #For not-always-populated fields, I'll have the classifier automatically split off empty values, assuming non-applicability.
        #Review Business (8K loaded)
         #Address State (must be split from business address field) - Barely.
         #Address Zip (must be split from business address field) - Probably not. Grouping a multi-split field would...
         #Address City (must be split from business address field) - ...be too time-consuming in this algorithm, methinks.
         #hours (not always populated, has per-day subfields. Just make included/not included maybe?)
         #Business name? Probably not, would need clustering measures.
         #Given attributes existing/true/false? This might simply take too long in the given algorithm considering how many of them there are.
         #Price Range? Listed under attributes. :(
         #Categories? Maybe simplify it into a count of number of categories.
         #review_count
         #stars? Do I want average stars for a business to be an evaluation factor? Hrm.
         #type doesn't seem helpful.
        #Review Proper (160K loaded)
         #Date (separate by year? Must be split from review date field)
         #Text (must be textually evaluated)
         #Votes (Total, and Cool/Funny/Useful subtotals)
        #Review User (All loaded, no way to really avoid it)
         #average_stars seems useful!
         #compliments count?
         #fans count?
         #friends count
         #review_count
         #votes count
        #User Tips (Organization: By business_id.)
         #text? Seems redundant with stars honestly. It's an option but I'll put it pretty far back.
         #Count of tips for a business
        #Business Checkins
         #Count of checkins for a business.
         
         
         
         #Format for these things is below.
         #Name: Obvious.
         #Location: Some fields are derived from linked 'tables'. The location dictates where the attribute comes from.
          #Options include: "Review" for unlinked thing, "User", "Business", "Tip", and "Checkin".
         #Existence: This field is a binary split; the criteria is that either the attribute is present or it is not. Boolean.
         #Count: This field is a counting field, with a single split. Boolean. If true describes either a summation field or an integer. Not sure if I'm going to go with a separate summation field.
         #temp['Name']=''
         #temp['Location']=''
         #temp['Existence']=False
         #temp['Count']=False

        Attributes=[]
        temp={}
        temp['Name']='Business State'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=False
        Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Hours'
        temp['Location']='business'
        temp['Existence']=True
        temp['Count']=False
        Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Categories'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)        
        
        temp={}
        temp['Name']='Business review_count'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Stars'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=False
        Attributes.append(temp)
        
        #Review proper
        temp={}
        temp['Name']='Review Year'
        temp['Location']='review'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)

        temp={}
        temp['Name']='Review Text'
        temp['Location']='review'
        temp['Existence']=False
        temp['Count']=False
        Attributes.append(temp)        
        
        temp={}
        temp['Name']='Review Votes'
        temp['Location']='review'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
        #User
        temp={}
        temp['Name']='User average_stars'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
        temp={}
        temp['Name']='User fans'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
        temp={}
        temp['Name']='User friends Count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)        
        
        temp={}
        temp['Name']='User review_count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
        temp={}
        temp['Name']='User votes Count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        Attributes.append(temp)
        
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
    
    #For counting things like votes.
    def dictionaryitemcount(self, dictionaryItems):
        returnVal=0
        for key in dictionaryItems:
            returnVal=returnVal+dictionaryItems[key]
        return returnVal
    
    def dictionarytotalcount(self, dictionaryItems):
        returnVal=0
        for key in dictionaryItems:
            returnVal=returnVal+1
        return returnVal
    
    



Stuff = Test_junk()

