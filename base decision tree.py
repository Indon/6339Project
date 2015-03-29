#Earl White
#Data Mining Project, Baseline Decision Tree
#1000882451

import os
import math
import string
from operator import itemgetter

class Hunt_tree:
    def __init__(self):
        trainingData={}
        testingData={}
        finalData={}
        #Open the training file.
        file = open('train.csv', "r")
        filelines = file.readlines()
        file.close
        self.names=[]
        self.types={}
        for line in filelines:
            singleline=line.split(",")
            if singleline[0]=="Id":
                self.names=singleline #Keep the top line, use to name stuff.
                #We then take that top line and use it to construct a dictionary, correlating the names of our attributes with
                #their datatypes. This lets us do things like iterate through 
                for itemNum in range(0,len(singleline),1):
                    if itemNum==0:
                        self.types[self.names[itemNum]]='ID'
                    elif itemNum<11:
                        self.types[self.names[itemNum]]='int'
                    elif itemNum<55:
                        self.types[self.names[itemNum]]='boolean'
                    else:
                        self.types[self.names[itemNum]]='class'
                #print(self.types)
            else:
                #Process data here.
                #Do I want a list of lists, or a list of dictionaries?
                #Hmm. Dictionaries, I think. More versatility with list comphrensions. In fact,
                #Why not a dictionary of dictionaries? It's a bit slower yeah, but I'm not optimizing this for speed.
                workingdata={}
                #0=id. Convert to int, then drop after splitting into testing or training.
                #1-10=Ratio values, convert to int.
                #11-54 = Boolean values.
                #55 = The classification variable, an ordinal from 1-7.
                for itemNum in range(0,len(singleline),1):
                    if itemNum<11:
                        workingdata[self.names[itemNum]]=int(singleline[itemNum])
                    elif itemNum<55:
                        temp=False
                        if singleline[itemNum]=="1":
                            temp=True
                        workingdata[self.names[itemNum]]=temp
                    else:
                        #This case should cover our class, and our class alone.
                        workingdata[self.names[itemNum]]=int(singleline[itemNum])
                #print(workingdata)
                #Do I want to use this method? I could also randomly determine the split, but that would produce not-exactly-duplicatable results.
                if workingdata['Id']<=4000:
                    temp=workingdata[self.names[0]]
                    testingData[temp]=workingdata
                    #testingData.append(workingdata) #Put in testing data.
                else:
                    temp=workingdata[self.names[0]]
                    trainingData[temp]=workingdata
                    #trainingData.append(workingdata) #Put in training data.
        
        decision_tree=self.build_node(trainingData)
        #print(decision_tree)
        
        #Classify the testing data with the constructed decision tree.
        self.classify(decision_tree,testingData,True)
        
        #Now let's upload test.csv!
        file = open('test.csv', "r")
        filelines = file.readlines()
        file.close 
        for line in filelines:
            singleline=line.split(",")
            if singleline[0]=="Id":
                self.names=singleline #Keep the top line, use to name stuff.
                self.names[len(self.names)-1]='Soil_Type40' #This is to fix a silly newline quirk I don't have time to research how to actually fix.
                #We then take that top line and use it to construct a dictionary, correlating the names of our attributes with
                #their datatypes. This lets us do things like iterate through 
                for itemNum in range(0,len(singleline),1):
                    pass
                #print(self.types)
            else:
                #Process data here.
                workingdata={}
                #0=id. Convert to int, then drop after splitting into testing or training.
                #1-10=Ratio values, convert to int.
                #11-54 = Boolean values.
                #55 = The classification variable, an ordinal from 1-7.
                for itemNum in range(0,len(singleline),1):
                    if itemNum<11:
                        workingdata[self.names[itemNum]]=int(singleline[itemNum])
                    elif itemNum<55:
                        temp=False
                        if singleline[itemNum]=="1":
                            temp=True
                        workingdata[self.names[itemNum]]=temp
                temp=workingdata[self.names[0]]
                finalData[temp]=workingdata
                #trainingData.append(workingdata) #Put in training data.
        final_data=self.classify(decision_tree,finalData,False)
        final_output = open('result.csv', "w")
        final_output.write('Id,Cover_Type\n')
        for line in final_data:
            #print(line)
            final_output.write(str(line[0])+','+str(line[1])+'\n')
        final_output.close
        #And with this, we are done.
    
    #Classifies a testing_dictionary based on a decision_tree as built by self.build_node.
    #If isTesting is true, 
    def classify(self, decision_tree, testing_dictionary, isTesting):
        #The result will be a list of ID's and classification variables.
        result=[]
        ID=self.names[0]#'id'
        if isTesting:
            class_name=self.names[55]
        else:
            class_name=''
        hits=0
        misses=0
        #For each item in the testing_dictionary, we're going to run it through the classification tree.
        for key in testing_dictionary:
            #print(testing_dictionary[key])
            classify_line=[testing_dictionary[key][ID],self.node_classify(decision_tree,testing_dictionary[key])]
            #print(classify_line)
            if isTesting:
                if classify_line[1]==testing_dictionary[key][class_name]:
                    hits=hits+1
                else:
                    misses=misses+1
            result.append(classify_line)
        if isTesting:
            print('Hits: ' + str(hits) + ' Misses: ' + str(misses) + ' Ratio: ' + str(hits/(hits+misses)))
        return result
    
    #Recursively searches the decision tree and returns a class variable value.
    def node_classify(self, decision_tree_section, testing_dictionary_item):
        result=decision_tree_section['Classification']
        #Can't get better than 0 entropy.
        if decision_tree_section['Entropy']<=0 or decision_tree_section['Split By']=='':
            #No split, no recursing.
            return result
        #A child node might have a better classification. Let's see what child node applies.
        classifier=decision_tree_section['Split By']
        #print(classifier)
        classifier_type=self.types[classifier]
        #print(classifier_type)
        if classifier_type=='boolean':
            if testing_dictionary_item[classifier]:
                result=self.node_classify(decision_tree_section['Nodes']['True'], testing_dictionary_item)
            else:
                result=self.node_classify(decision_tree_section['Nodes']['False'], testing_dictionary_item)
        elif classifier_type=='int':
            #We get the breakpoint for the integer classifier.
            breakpoint=[key for key in decision_tree_section['Nodes'] if key>-100000][0]
            #print(breakpoint)
            #This section currently exploits that my int breaks are two-way only.
            if testing_dictionary_item[classifier]>breakpoint:
                if len(decision_tree_section['Nodes'][breakpoint])>0:
                    result=self.node_classify(decision_tree_section['Nodes'][breakpoint],testing_dictionary_item)
            else:
                if len(decision_tree_section['Nodes'][-100000])>0:
                    result=self.node_classify(decision_tree_section['Nodes'][-100000],testing_dictionary_item)
        return result
    
    #Takes a dictionary of data items (which may be a subdictionary) and builds a node using Hunt's Algorithm.
    #Will recursively take subdictionaries from the given list and use them to build additional nodes attached to this node.
    #The result will be a recursively built dictionary of dictionaries (in turn, containing dictionaries, yo dawg) that represents the decision tree.
    def build_node(self,training_dictionary):
        #Since a multi-way numeric split would take significantly longer than calculating a single split (like, orders-of-time larger), I will be limiting analysis
        #in this decision tree to binary splits (since the evaluation values are all either numeric or boolean).
        #This means I don't need to calculate gain ratio - I can just iterate through the remaining candidate attributes and select the splitting option that provides the lowest entropy (which maximizes our raw information gain), or not split if there is no gain or attributes.
        result={}
        #We begin by selecting the node's classification, which is the most common class item in the set.
        result['Classification']=self.count_most_common_class(training_dictionary)
        benchmark=self.calculate_entropy(training_dictionary)
        result['Entropy']=benchmark
        length=len(training_dictionary)
        entropy_breakpoint=[0]
        
        attribute=''
        #We access one item in the dictionary to get a list of attributes present in the dictionary.
        entry=next(iter(training_dictionary.values()))
        
        #Here we iterate through those attributes which are present in the dictionary.
        for attribute_name in entry:
            #We need to get the attribute type for attribute_name.
            attribute_type=self.types[attribute_name]
            if attribute_type=='int' or attribute_type=='boolean':
                if attribute_type=='boolean':
                    true_subset={key:training_dictionary[key] for key in training_dictionary if training_dictionary[key][attribute_name]==True}
                    true_subset_length=len(true_subset)
                    false_subset={key:training_dictionary[key] for key in training_dictionary if training_dictionary[key][attribute_name]==False}
                    false_subset_length=len(false_subset)
                    #print(true_subset_length, false_subset_length)
                    candidate_entropy=(true_subset_length/length)*self.calculate_entropy(true_subset)+self.calculate_entropy(false_subset)*(false_subset_length/length)
                else:
                    entropy_values=self.calculate_best_entropy(training_dictionary,attribute_name)
                    candidate_entropy=entropy_values[0]
                if candidate_entropy<benchmark:
                    attribute=attribute_name
                    benchmark=candidate_entropy
                    if attribute_type=='int':
                        entropy_breakpoint=[entropy_values[1]]
        #Done iterating: attribute is now the name of the best attribute. It is blank if no split provides higher entropy (eg if everything is the same class).
        #So if attribute is blank, we do nothing and if it is not blank we split the tree into subsets based on the attribute and generate nodes with the subset.
        if attribute=='':
            #In the event I ever want to do something special to denote a terminal node.
            result['Nodes']=None
            result['Split By']=''
        else:
            Nodes={}
            #print('subdividing dictionary of size ' + str(length) + ' by ' + attribute + ' with a breakpoint of ' + str(entropy_breakpoint))
            Nodes=self.subdivide_dictionary(attribute, entropy_breakpoint, training_dictionary)
            for key in Nodes:
                if len(Nodes[key])>0:
                    Nodes[key]=self.build_node(Nodes[key])
                else:
                    #Shouldn't this code never execute with binary splits? Hrm.
                    #del Nodes[key]
                    pass
            result['Nodes']=Nodes
            result['Split By']=attribute
        return result
        #Aaaand we're done!

    
    #Calculates the entropy of a dictionary of data items.
    def calculate_entropy(self, dictionary):
        total_count=len(dictionary)
        if total_count==0:
            return 0
        class_name=self.names[55] #Hardcoded. Hope I don't have to reuse this code!
        #This is an ugly brute force when instead I should construct a pretty, generic loop+sum setup.
        count_1=len([item for item in dictionary if dictionary[item][class_name] == 1])/total_count
        count_1=-(count_1)*self.log2(count_1)
        count_2=len([item for item in dictionary if dictionary[item][class_name] == 2])/total_count
        count_2=-(count_2)*self.log2(count_2)
        count_3=len([item for item in dictionary if dictionary[item][class_name] == 3])/total_count
        count_3=-(count_3)*self.log2(count_3)
        count_4=len([item for item in dictionary if dictionary[item][class_name] == 4])/total_count
        count_4=-(count_4)*self.log2(count_4)
        count_5=len([item for item in dictionary if dictionary[item][class_name] == 5])/total_count
        count_5=-(count_5)*self.log2(count_5)
        count_6=len([item for item in dictionary if dictionary[item][class_name] == 6])/total_count
        count_6=-(count_6)*self.log2(count_6)
        count_7=len([item for item in dictionary if dictionary[item][class_name] == 7])/total_count
        count_7=-(count_7)*self.log2(count_7)
        #print(count_1,'+',count_2,'+',count_3,'+',count_4,'+',count_5,'+',count_6,'+',count_7)
        #print(count_1+count_2+count_3+count_4+count_5+count_6+count_7)
        return count_1+count_2+count_3+count_4+count_5+count_6+count_7
    
    def count_most_common_class(self, dictionary):
        class_name=self.names[55] #Hardcoded. Hope I don't have to reuse this code!
        item=1
        count=len([item for item in dictionary if dictionary[item][class_name] == 1])
        for i in range(2,8,1):
            temp=len([item for item in dictionary if dictionary[item][class_name] == i])
            if temp>count:
                count=temp
                item=i
        return item

    #Okay. Given a dictionary and a numeric variable, this function will return the
    #entropy for the ideal splitting point and the value of that splitting point as a point
    #that should have everything less than or equal in one and everything greater-than in another.
    #A single point thus generated should work fine when passed to subdivide_dictionary.
    def calculate_best_entropy(self, dictionary, attribute_name):
            total_count=len(dictionary)
            if total_count==0:
                return 0
            class_name=self.names[55] #Hardcoded. Hope I don't have to reuse this code!
            #This is an ugly brute force when instead I should construct a pretty, generic loop+sum setup.
            count=[0,0,0,0,0,0,0]
            count[0]=len([item for item in dictionary if dictionary[item][class_name] == 1])#/total_count
            #count[0]=-(count[0])*math.log2(count[0])
            count[1]=len([item for item in dictionary if dictionary[item][class_name] == 2])#/total_count
            #count[1]=-(count[1])*math.log2(count[1])
            count[2]=len([item for item in dictionary if dictionary[item][class_name] == 3])#/total_count
            #count[2]=-(count[2])*math.log2(count[2])
            count[3]=len([item for item in dictionary if dictionary[item][class_name] == 4])#/total_count
            #count[3]=-(count[3])*math.log2(count[3])
            count[4]=len([item for item in dictionary if dictionary[item][class_name] == 5])#/total_count
            #count[4]=-(count[4])*math.log2(count[4])
            count[5]=len([item for item in dictionary if dictionary[item][class_name] == 6])#/total_count
            #count[5]=-(count[5])*math.log2(count[5])
            count[6]=len([item for item in dictionary if dictionary[item][class_name] == 7])#/total_count
            #print(count)
            #count[6]=-(count[6])*math.log2(count[6])
            #Our smallest entropy. So far.
            tempcount=[item/total_count for item in count]
            temptropy=-(tempcount[0])*self.log2(tempcount[0])-(tempcount[1])*self.log2(tempcount[1])-(tempcount[2])*self.log2(tempcount[2])-(tempcount[3])*self.log2(tempcount[3])-(tempcount[4])*self.log2(tempcount[4])-(tempcount[5])*self.log2(tempcount[5])-(tempcount[6])*self.log2(tempcount[6])
            break_point=0
            #Here we use Magical Python List Comprehension Power to produce a list of attribute and class values, sorted by attribute value.
            superlist= [[dictionary[key][attribute_name], dictionary[key][class_name]] for key in dictionary] #[attribute_name],value[class_name]
            superlist=sorted(superlist,key=itemgetter(0))
            count2=[0,0,0,0,0,0,0]
            tempcount=[0,0,0,0,0,0,0]
            tempcount2=[0,0,0,0,0,0,0]
            for itemnum in range(0,len(superlist),1):
                count[superlist[itemnum][1]-1]=count[superlist[itemnum][1]-1]-1
                #print(count)
                count2[superlist[itemnum][1]-1]=count2[superlist[itemnum][1]-1]+1
                tempcount=[item/total_count for item in count]
                tempcount2=[item/total_count for item in count2]
                contender=((total_count-(itemnum+1))/total_count)*(-(tempcount[0])*self.log2(tempcount[0])-(tempcount[1])*self.log2(tempcount[1])-(tempcount[2])*self.log2(tempcount[2])-(tempcount[3])*self.log2(tempcount[3])-(tempcount[4])*self.log2(tempcount[4])-(tempcount[5])*self.log2(tempcount[5])-(tempcount[6])*self.log2(tempcount[6]))+(-(tempcount2[0])*self.log2(tempcount2[0])-(tempcount2[1])*self.log2(tempcount2[1])-(tempcount2[2])*self.log2(tempcount2[2])-(tempcount2[3])*self.log2(tempcount2[3])-(tempcount2[4])*self.log2(tempcount2[4])-(tempcount2[5])*self.log2(tempcount2[5])-(tempcount2[6])*self.log2(tempcount2[6]))*((itemnum+1)/total_count)
                #print(contender)
                if contender<temptropy:
                    temptropy=contender
                    break_point=superlist[itemnum][0]
            return [temptropy,break_point]

    #The class insists that log2(0) is 0, while python insists it is undefinable.
    def log2(self, number):
        if number<=0:
            return 0
        return math.log2(number)

    #Takes a dictionary, and divides it into a dictionary of dictionaries based on the splitting_groups criteria, if the attribute_name's type
    #is int. (Otherwise splitting_groups is ignored)
    #Splitting_groups is a list of greater-than points of division. It must be given in increasing order.
    #The resulting split data no longer has attribute_name in it.
    def subdivide_dictionary(self, attribute_name, splitting_groups, splittable_dictionary):
        #We first make a bucket for each splitting group - or two buckets if it's a boolean.
        #Then we put each item in the splittable_dictionary into one of them.
        returnValue={}
        if self.types[attribute_name]=='int':
            for item in splitting_groups:
                returnValue[item]={}
            returnValue[-100000]={}
            for item in splittable_dictionary:
                for comparison_item in splitting_groups:
                    if splittable_dictionary[item][attribute_name]>comparison_item:
                        #Don't need this attribute anymore!
                        del splittable_dictionary[item][attribute_name]
                        returnValue[comparison_item][item]=splittable_dictionary[item]
                        #This break leaves the comparison_item loop because we only care about the first
                        #thing the attribute is larger than.
                        break
                else: #Little quirk about python. If a for loop is never broken from, an 'else' block can be executed!
                    #This lets us execute code in the event that the item isn't placed in any other bucket.
                    del splittable_dictionary[item][attribute_name]
                    #The return value here should be the minimum integer value found. Coding this dynamically (and I'm leery about using minInt)
                    #would take too long so terrible hack GO!
                    returnValue[-100000][item]=splittable_dictionary[item]
        else:
            #I might need to put boolean True/False values here instead. We'll see.
            returnValue['True']={}
            returnValue['False']={}
            #This iterates through keys.
            for item in splittable_dictionary:
                if splittable_dictionary[item][attribute_name]==True:
                    del splittable_dictionary[item][attribute_name]
                    returnValue['True'][item]=splittable_dictionary[item]
                else:
                    del splittable_dictionary[item][attribute_name]
                    returnValue['False'][item]=splittable_dictionary[item]
        return returnValue

        
class Node:
    def __init__(self):
        #Terminal, or Decision.
        self.Type='Something'
        #This is the class things that stop at this node shunt into.
        self.Class=0
        #A list of recursively contained nodes.
        self.Nodes=[]

#This by itself should complete the classification on train.csv and produce a classification file for test.csv.
Stuff = Hunt_tree()