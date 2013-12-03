from itertools import izip
from collections import defaultdict
import pickle
"""
tags=defaultdict(int)

q=open("superT.txt","r")
taglines=q.read().split("\n")
for tagline in taglines:
    for tag in tagline.split(" "):
        tags[tag]+=1
q.close()
sort_tags=sorted(tags.items(),key=lambda (k,v):v,reverse=True)
toptags=[tag[0] for tag in sort_tags]
"""
top834=pickle.load(open('top834.pkl','rb'))
errors=[]

###toptags=['java']##comment out if not working on a single tag

print "SORTED!"
def get_acc(toptags):
    #f=open("Q.txt","r")
    #questions=f.read().split("\n")
    with open("superT.txt","r") as truefile:
        with open("superPT33k-150-20-74.txt","r") as predfile:
            accuracy = 0.0
            count = 0
            count1,count2 = 0,0
            check=[]
            for line1,line2 in izip(truefile,predfile):

                truetags,predtags = [],[]
                for tag in line1.replace('\n',' ').split(" "):

                    if tag in toptags:#this checks for the top tags
                        print line1
                        print line2
                        raw_input("")
                        truetags.append(tag)
            
                for tag in line2.replace('\n',' ').split(" "):
                    predtags.append(tag)
                truetags = [x for x in truetags if x is not ""]
                predtags = [x for x in predtags if x is not ""]
                if(len(truetags) is 0 or len(predtags) is 0):
                    #count+=1 
                    continue
                ###acc = len(list(set(truetags) & set(predtags)))
                
                acc=0
                for tag in truetags:
                    for word in predtags:
                        
                        if len(word)==1 and tag not in ["c#","c","c++"]:
                            #print word,tag
                            #check.append((word,tag))
                            #raw_input("")
                            continue
                        
                        elif word in tag:
                            acc+=1
                            break
                
                acc = float(acc)/len(truetags)
                #print acc
                #print questions[count]  #needs doccount to work
                #print truetags
                #print predtags
                accuracy += acc
                #print count
                count += 1
                #raw_input()
            #print count
            if count==0:
                errors.append(toptags)
                return 0
            accuracy = (float)(accuracy)/count
            #print "Final Accuracy:"
            #print accuracy
    return accuracy
    #f.close()


##accuracies=defaultdict(float)
test=0
top834=['iterator']
for tag in top834:
    ##accuracies[tag]=get_acc([tag])
    test=get_acc([tag])
    ##print tag,accuracies[tag]
    print tag,test

