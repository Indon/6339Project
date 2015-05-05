#Earl White
#Data Mining Project, Test File
#1000882451

#Contains code based on code from my assignment 2.

import json
import time
import math
from operator import itemgetter

class Test_junk:
    def __init__(self):
        #Opens every data file and builds a dictionary of dictionaries for each of them. The Business, Reviews, and Users dictionaries have keys equal to their
        #respective ID's. The Tips have both business and userID and that's it.
        self.TrainingReviews={}
        self.TestReviews={}
        self.ValidationReviews={}
        self.Businesses={}
        self.Users={}
        self.Tips={}
        self.Checkins={}
        
        

        
        file=open('J:\School\Data Mining\Project\Files\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json','r')
        filestrings=file.readlines()
        file.close()
        count=0
        for line in filestrings:
            count=count+1
            filedic=json.loads(line)
            #Only loading about 1/8th of all businesses in database.
            if count<8000:
                self.Businesses[filedic['business_id']] = filedic
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
            if filedic['business_id'] in self.Businesses:
                count=count+1
                if count%5==0:
                    #20% of the reviews in the training set; 32,000.
                    self.TrainingReviews[filedic['review_id']] = filedic
                elif count%5==1:
                    #20% more of the reviews in the test set; another 32,000.
                    self.TestReviews[filedic['review_id']] = filedic
                else:
                    #The rest of the reviews in the validation set. 96,000. All these are estimates.
                    self.ValidationReviews[filedic['review_id']] = filedic

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
            self.Users[filedic['user_id']] = filedic
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
            if filedic['business_id'] in self.Businesses:
                if filedic['business_id'] not in self.Tips:
                    self.Tips[filedic['business_id']] = []
                self.Tips[filedic['business_id']].append(filedic)
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
            if filedic['business_id'] in self.Businesses:
                self.Checkins[filedic['business_id']] = filedic
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

        self.Attributes=[]
        #Because state would be a multi-way split and that could present a pretty big time hit, going to put implementing
        #this pretty low on priorities.
        #temp={}
        #temp['Name']='Business State'
        #temp['Location']='business'
        #temp['Existence']=False
        #temp['Count']=False
        #Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Hours'
        temp['Location']='business'
        temp['Existence']=True
        temp['Count']=False
        self.Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Categories'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)        
        
        temp={}
        temp['Name']='Business review_count'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        temp={}
        temp['Name']='Business Stars'
        temp['Location']='business'
        temp['Existence']=False
        temp['Count']=False
        self.Attributes.append(temp)
        
        #Review proper
        temp={}
        temp['Name']='Review Year'
        temp['Location']='review'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        #Writing a text classifier as part of a decision tree might take more time than I have!
        #We'll see if I get to where I can use this field.
        #temp={}
        #temp['Name']='Review Text'
        #temp['Location']='review'
        #temp['Existence']=False
        #temp['Count']=False
        #Attributes.append(temp)        
        
        temp={}
        temp['Name']='Review Votes'
        temp['Location']='review'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        #User
        temp={}
        temp['Name']='User average_stars'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        temp={}
        temp['Name']='User fans'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        temp={}
        temp['Name']='User friends Count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)        
        
        temp={}
        temp['Name']='User review_count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        temp={}
        temp['Name']='User votes Count'
        temp['Location']='user'
        temp['Existence']=False
        temp['Count']=True
        self.Attributes.append(temp)
        
        for item in self.Attributes:
            item['Used']=False
        
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
    
    #This might just be easier to replace with len(dictionary)
    def dictionarytotalcount(self, dictionaryItems):
        returnVal=0
        for key in dictionaryItems:
            returnVal=returnVal+1
        return returnVal
    
    
    def base_tree(self):
        starttime=time.time()
        base_decision_tree=self.build_base_node(self.TrainingReviews)
        endtime=time.time()
        print('Decision tree generated in ' + (str) (endtime-starttime) + ' seconds.')
        starttime=time.time()
        accuracy=self.classify_all(base_decision_tree,self.ValidationReviews)
        endtime=time.time()
        print('Decision tree evaluated in ' + (str) (endtime-starttime) + ' seconds.')
        print('Accuracy rate is  ' + (str)(accuracy) + ' percent.')
        
        return 0
    
    def sorted_tree(self):
        start
        starttime=time.time()
        
    
    #This classification function doesn't output the actual classification, and is purely for use on validation/testing data.
    #Returns a number between 0 and 1 reflecting classification accuracy.
    def classify_all(self, decision_tree, testing_dictionary):
        hits=0
        misses=0
        for key in testing_dictionary:
            guess=self.classify_entry(decision_tree,testing_dictionary[key])
            if guess==testing_dictionary[key]['stars']:
                hits=hits+1
            else:
                misses=misses+1
        return hits/(hits+misses)
    
    #Pass the decision tree and the dictionary for the single review entry being analyzed.
    #Returns an integer representing the review guessed by the tree.
    def classify_entry(self, decision_tree, entry_dictionary):
        if 'Split By' in decision_tree:
            #This is a quick way to grab the single data entry for the thing we're classifying.
            onereviewdictionary={}
            onereviewdictionary[entry_dictionary['review_id']]=entry_dictionary
            classificationcriteria=self.get_attribute_dataset(decision_tree['Split By'],onereviewdictionary)
            if decision_tree['Split By']['Existence']==True:
                if classificationcriteria[0][0]==True:
                    return self.classify_entry(decision_tree['Nodes'][1],entry_dictionary) #Hehe, true entries are 1.
                else:
                    return self.classify_entry(decision_tree['Nodes'][0],entry_dictionary)
            else:
                if classificationcriteria[0][0]>decision_tree['Breakpoint']:
                    return self.classify_entry(decision_tree['Nodes'][1],entry_dictionary)
                else:
                    return self.classify_entry(decision_tree['Nodes'][0],entry_dictionary)
        else:
            return decision_tree['Classification']
        return 0
    
    #Use 0 as initial sort level.
    def build_sorted_node(self, training_dictionary, sort_level):
        #The sort_level is how many layers down the tree the node is at, which dictates what attribute will split the dataset.
        result = {}
        
        #Number between 1 and 5 reflecting review.
        result['Classification']=self.count_most_common_class(training_dictionary)
        
        #Node entropy
        result['Entropy']=self.calculate_node_entropy(training_dictionary)
        currententropy=result['Entropy']
        
        print('Now classifying set of ' + len(training_dictionary) + 'items')
        
        if len(training_dictionary)>5 and sort_level<len(self.Attributes):
            sortingattribute=self.Attributes[sort_level]
            
            workingset = self.get_attribute_dataset(sortingattribute, training_dictionary)
            if sortingattribute['Existence']==False:
                #Numeric variable, going to do a single-point split based on best entropy because it's linear.
                splitdata=self.calculate_best_split(training_dictionary, workingset)
                if splitdata[1]<currententropy:
                    currententropy=splitdata[1]
                    result['Split By']=sortingattribute
                    result['Nodes']=self.split_dictionary(sortingattribute['Existence'],splitdata[0],workingset,training_dictionary)
                    result['Breakpoint']=splitdata[0]
                    for i in range(2):
                        result['Nodes'][i]=self.build_sorted_node(result['Nodes'][i],sort_level+1)
                else:
                    #If this attribute can't improve entropy measure, just build this node with the next attribute in the order.
                    return self.build_sorted_node(training_dictionary, sort_level+1)
            else:
                #Boolean variable. True/False Split.
                tempentropy=self.set_entropy(len([item for item in workingset if workingset[0]==True]),len([item for item in workingset if workingset[0]==False]))
                if tempentropy['Entropy']<currententropy:
                    currententropy=tempentropy['Entropy']
                    result['Split By']=sortingattribute
                    result['Nodes']=self.split_dictionary(sortingattribute['Existence'],0,workingset,training_dictionary)
                    result['Breakpoint']=splitdata[0]
                    for i in range(2):
                        result['Nodes'][i]=self.build_sorted_node(result['Nodes'][i],sort_level+1)
                else:
                    return self.build_sorted_node(training_dictionary, sort_level+1)
        return result
    
    def build_base_node(self, training_dictionary):
        result = {}
        
        #Number between 1 and 5 reflecting review.
        result['Classification']=self.count_most_common_class(training_dictionary)
        
        #Node entropy
        result['Entropy']=self.calculate_node_entropy(training_dictionary)
        
        print('Now classifying set of ' + (str)(len(training_dictionary)) + 'items')
        
        #If there's fewer than a given number of items in the node (let's say 6), we stop splitting.
        #Sparse data risks overtuning.
        if len(training_dictionary)>5:
            currentEntropy=result['Entropy']
            splitAttribute={}
            breakpoint=0 #This statement purely done purely as a coding practice.
            #Parse through evaluating the attributes, determining the lowest-entropy split.
            attributeindex=0
            usedattribute=0
            for item in self.Attributes:
                workingset = self.get_attribute_dataset(item, training_dictionary)
                if item['Used']==False:
                    if item['Existence']==False:
                        #Numeric variable, going to do a single-point split based on best entropy because it's linear.
                        splitdata=self.calculate_best_split(training_dictionary, workingset)
                        if splitdata[1]<currentEntropy:
                            currentEntropy=splitdata[1]
                            splitAttribute=item
                            breakpoint=splitdata[0]
                            usedattribute=attributeindex
                    else:
                        #Boolean variable. True/False Split.
                        truecount=len([item for item in workingset if workingset[0]==True])
                        falsecount=len([item for item in workingset if workingset[0]==False])
                        if truecount>0 and falsecount>0:
                            tempentropy=self.set_entropy([truecount,falsecount])
                            if tempentropy<currentEntropy:
                                currentEntropy=tempentropy
                                splitAttribute=item
                                usedattribute=attributeindex
                attributeindex=attributeindex+1
            #At this point we've iterated through attributes. Let's build the classification system, split the database and
            #build the nodes!
            if 'Name' in splitAttribute:
                result['Split By']=splitAttribute
                result['Nodes']=self.split_dictionary(splitAttribute['Existence'],breakpoint,self.get_attribute_dataset(splitAttribute, training_dictionary),training_dictionary)
                result['Breakpoint']=breakpoint
                self.Attributes[usedattribute]['Used']=True
                for i in range(2):
                    result['Nodes'][i]=self.build_base_node(result['Nodes'][i])
                #for item in result['Nodes']:
                #    item=self.build_base_node(item)
                self.Attributes[usedattribute]['Used']=False
        else:
            #Small nodes don't get split, want to minimize overtuning.
            pass
        return result
    
    
    #Splits a dictionary into two nodes.
    def split_dictionary(self, boolean, breakpoint, dataset, dictionary):
        #Since all my splits are binary for time reasons, going to just have two of these hardcoded.
        #True will be put in highsplit, because I favor the 1=true and 0=false convention and so does Python.
        highsplit={}
        lowsplit={}
        
        if boolean==True:
            #the dataset is [amount,review_id].
            for item in dataset:
                if item[0]==True:
                    highsplit[item[1]]=dictionary[item[1]]
                else:
                    lowsplit[item[1]]=dictionary[item[1]]
        else:
            for item in dataset:
                if item[0]>breakpoint:
                    highsplit[item[1]]=dictionary[item[1]]
                else:
                    lowsplit[item[1]]=dictionary[item[1]]
        #
        return [lowsplit,highsplit]
    
    #Given a sorted set of [value,review_id], returns the best breakpoint and that breakpoint's entropy for a single decision tree split.
    def calculate_best_split(self, dictionary, dataset):
        count=[0,0,0,0,0]
        #does dictionary or list length return faster?
        totalsize=len(dataset)
        class_name='stars'
        count[0]=len([item for item in dictionary if dictionary[item][class_name] == 1])
        count[1]=len([item for item in dictionary if dictionary[item][class_name] == 2])
        count[2]=len([item for item in dictionary if dictionary[item][class_name] == 3])
        count[3]=len([item for item in dictionary if dictionary[item][class_name] == 4])
        count[4]=len([item for item in dictionary if dictionary[item][class_name] == 5])
        #Returns tuples of [Value, ReviewId]. dictionary[item[0]] addresses a given review with the review_id.
        currententropy=self.set_entropy(count)['Entropy']
        currentbreakpoint=0
        secondcount=[0,0,0,0,0]
        
        for item in dataset:
            #Old count minus one for stuff after the classification.
            count[(dictionary[item[1]]['stars']-1)]=count[(dictionary[item[1]]['stars']-1)]-1
            #New count plus one for stuff before that classification.
            secondcount[(dictionary[item[1]]['stars']-1)]=count[(dictionary[item[1]]['stars']-1)]+1
            #Let's calculate the breakpoint and entropy for this split.
            tempbreakpoint=item[0]
            if sum(count)>0 and sum(secondcount)>0:
                tempentropy=self.split_entropy([[self.set_entropy(count)['Entropy'],sum(count)],[self.set_entropy(secondcount)['Entropy'],sum(secondcount)]])
                if tempentropy<currententropy:
                    currententropy=tempentropy
                    currentbreakpoint=tempbreakpoint
        return [currentbreakpoint,currententropy]
    
    #Uses the given attribute (a dictionary entry from Attributes)
    #and extracts the corresponding attribute data
    #first as a list of items in the dictionary format {BusinessID=<business_id> attribute=<content>} if necessary
    #then turns that into a list of [review_id, linkingId, attribute].
    #Then it reduces it and returns [review_id, attribute], sorted.
    def get_attribute_dataset(self, attribute, dictionary):
        returnval=[]
        metaval=[]
        if attribute['Name']=='Business State':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['business_id']] for key in dictionary]
            for item in returnval:
                item.append(Businesses[item[1]][''])
                pass
            
        elif attribute['Name']=='Business Hours':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['business_id']] for key in dictionary]
            for item in returnval:
                if len(self.Businesses[item[1]]['hours'])>0:
                    #Could make this into a count measure of how many days they're open, but since some businesses don't
                    #have hours posted at all, decided to make it into a hours-posted-or-not measure.
                    item.append(True)
                else:
                    item.append(False)
        elif attribute['Name']=='Business Categories':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['business_id']] for key in dictionary]
            for item in returnval:
                item.append(len(self.Businesses[item[1]]['categories']))
        elif attribute['Name']=='Business review_count':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['business_id']] for key in dictionary]
            for item in returnval:
                item.append(self.Businesses[item[1]]['review_count'])
        elif attribute['Name']=='Business Stars':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['business_id']] for key in dictionary]
            for item in returnval:
                item.append(self.Businesses[item[1]]['stars'])
        elif attribute['Name']=='Review Year':
            #Could concatenate review month and day at the end, I suppose? Will think about that.
            returnval=[[dictionary[key]['review_id'], dictionary[key]['review_id'], dictionary[key]['date'][:4]] for key in dictionary]
        elif attribute['Name']=='Review Text':
            #To do: Implement.
            pass
        elif attribute['Name']=='Review Votes':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['review_id'], self.dictionaryitemcount(dictionary[key]['votes'])] for key in dictionary]
        elif attribute['Name']=='User average_stars':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['user_id']] for key in dictionary]
            for item in returnval:
                item.append(self.Users[item[1]]['average_stars'])
        elif attribute['Name']=='User fans':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['user_id']] for key in dictionary]
            for item in returnval:
                item.append(self.Users[item[1]]['fans'])
        elif attribute['Name']=='User friends Count':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['user_id']] for key in dictionary]
            for item in returnval:
                item.append(len(self.Users[item[1]]['friends']))
        elif attribute['Name']=='User review_count':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['user_id']] for key in dictionary]
            for item in returnval:
                item.append(self.Users[item[1]]['review_count'])
        elif attribute['Name']=='User votes Count':
            returnval=[[dictionary[key]['review_id'], dictionary[key]['user_id']] for key in dictionary]
            for item in returnval:
                item.append(self.dictionaryitemcount(self.Users[item[1]]['votes']))
        elif attribute['Name']=='':
            pass
        #Drop the link key, attribute first.
        returnval=[[item[2],item[0]] for item in returnval]
        returnval=sorted(returnval,key=itemgetter(0))
        return returnval
    
    def calculate_node_entropy(self, review_dictionary):
        total_count=len(review_dictionary)
        if total_count==0:
            return 0
        class_name='stars'
        count=[len([item for item in review_dictionary if review_dictionary[item][class_name] == 1]),len([item for item in review_dictionary if review_dictionary[item][class_name] == 2]),len([item for item in review_dictionary if review_dictionary[item][class_name] == 3]),len([item for item in review_dictionary if review_dictionary[item][class_name] == 4]),len([item for item in review_dictionary if review_dictionary[item][class_name] == 5])]
        return self.set_entropy(count)['Entropy']
    
    #Takes reviews, returns a 1-5 reflecting the most common review (with lower review bias for ties).
    def count_most_common_class(self, dictionary):
        class_name='stars'
        highest=1
        count=len([item for item in dictionary if dictionary[item][class_name] == 1])
        for i in range(2,8,1):
            temp=len([item for item in dictionary if dictionary[item][class_name] == i])
            if temp>count:
                count=temp
                highest=i
        return highest
    
    #Pass: List of integers.
    #Returns: A dictionary object.
    #returnval['Entropy']= Entropy for a single set where each of those integers represents the count for one class.
    #returnval['Total']=Total count of items for split entropy calculation.
    def set_entropy(self, countlist):
        total=0
        for item in countlist:
            total=total+item
        #Now total is the total number of items.
        returnval=0
        for item in countlist:
            returnval = returnval + (-(item/total) * self.log2(item/total))
        returns={}
        returns['Entropy']=returnval
        returns['Total']=total
        return returns
    
    #Takes a list of set_entropy objects that contain entropy and total item counts.
    #item[0]=entropy, item[1]=count
    #Returns total entropy.
    def split_entropy(self, entropylist):
        total=0
        entropy=0
        for item in entropylist:
            total=total+item[1]
        for item in entropylist:
            entropy=entropy+(item[0]*(item[1]/total))
        return 0
    
    def log2(self, number):
        if number<=0:
            return 0
        return math.log2(number)    
    
    def classify(self, decision_tree, testing_dictionary):
        return 0
    



Stuff = Test_junk()

#Stuff.base_tree()
Stuff.sorted_tree()