from itertools import izip
from collections import defaultdict

tags=defaultdict(int)

q=open("superT.txt","r")
taglines=q.read().split("\n")
for tagline in taglines:
    for tag in tagline.split(" "):
        tags[tag]+=1
q.close()
sort_tags=sorted(tags.items(),key=lambda (k,v):v,reverse=True)#[:834]
toptags=[tag[0] for tag in sort_tags]
print "SORTED!"

f=open("Q.txt","r")
questions=f.read().split("\n")
with open("superT.txt","r") as truefile:
    with open("superPT0.05-150-20-55.txt","r") as predfile:
        accuracy = 0.0
        count = 0
        count1,count2 = 0,0
        #for line in truefile:
        #    count1 +=1 
        #for line in predfile:
        #    count2 += 1
        #print count1,count2
        #sys.exit()
        check=[]
        for line1,line2 in izip(truefile,predfile):

            truetags,predtags = [],[]
            for tag in line1.replace('\n',' ').split(" "):
                if tag in toptags:#this checks for the top tags
                    truetags.append(tag)
            for tag in line2.replace('\n',' ').split(" "):
                predtags.append(tag)
            truetags = [x for x in truetags if x is not ""]
            predtags = [x for x in predtags if x is not ""]
            if(len(truetags) is 0 or len(predtags) is 0):
                #count+=1 
                continue
            #acc = len(list(set(truetags) & set(predtags)))
            
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
            print count
            count += 1
            #raw_input()
        print count
        accuracy = (float)(accuracy)/count
        print "Final Accuracy:"
        print accuracy
f.close()
