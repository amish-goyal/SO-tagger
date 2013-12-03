#!/usr/bin/env python
# http://paste.org/8946 "no" 2009
# Updated by Tero Karvinen http://TeroKarvinen.com

from collections import defaultdict
from itertools import izip
import nltk
import xml.sax.handler
import xml.sax
import sys
import re
import pickle
import numpy
import pylab as pl

parser=handler=outfile=tagfile=qfile=""


class SOHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.errParse = 0
        self.counter = 0
        self.tags_dict=defaultdict(int)
        self.tags=[]
        self.questions=[]
        self.q_with_tags=[]

    def get_question(self, attributes):
        question = attributes['Body'].encode("utf-8").replace('\n'," ")
        #q_with_tags = q_with_tags.encode("utf-8")
		#q_with_tags = q_with_tags.replace('\n'," ")
        return question

    def get_tags(self, attributes):
        try:
            tags=attributes['Tags'].split('><')
            tags[0]=tags[0][1:]
            tags[-1]=tags[-1][:-1]
               
            if self.counter==1:
                raw_input("tags: %s %s" %(tags,tag))
            return tags
        except:
            return []

    def test_out_stuff(self,name,attributes):
        try:
            print name
            print attributes['PostTypeId']
            print type(name)
            print type(attributes['PostTypeId'])
            #print attributes.keys()
            raw_input("testing this shit out!\n")
        except:
            raw_input("dint work this time!\n")

 
    def startElement(self, name, attributes):
        global outfile,qfile,tagfile
       
        if name != "row" or attributes['PostTypeId']!="1":
            try:
                pass
                #print name,attributes['PostTypeId']
            except:
                pass
            #self.test_out_stuff(name,attributes)
        
        else:
            tags=self.get_tags(attributes)
            tags=" ".join(tags).encode("utf-8")
            question=self.get_question(attributes)
            q_with_tags=question+tags
            q_with_tags_sanitized=re.sub(r'<[^<>]+>', '', q_with_tags)
            
            #self.tags.append(tags)
            #self.questions.append(question)
            #self.q_with_tags.append(q_with_tags_sanitized)
                        
            outfile.write(q_with_tags_sanitized)
            outfile.write("\n")
            outfile.flush()

            tagfile.write(tags)
            tagfile.write("\n")
            tagfile.flush()
            
            qfile.write(question)
            qfile.write("\n")
            qfile.flush()
            """
            if self.counter<5:
                print "Tags: "+str(tags)
                print "\nQuestion: "+str(question)
                print "\nQuestion + Tag: "+str(q_with_tags)
                print "\nSanitized:      "+str(q_with_tags_sanitized)
                raw_input("\n")
            """
            self.counter += 1
            if self.counter%10000==0:
                print tags
                print question
                print q_with_tags_sanitized
                print self.counter
            
            #if(self.counter > 1999):
            #    sys.exit()
            
def zipfs_plot():
    tagdict=return_tag_dict()
    print "got tagdict!"
    sortedtags=sorted(tagdict.items(),key=lambda (k,v):v,reverse=True)
    frequencies=[freq for tag,freq in sortedtags]
    x1=numpy.array(range(1,len(sortedtags)+1))
    x1=numpy.log(x1)
    y1=numpy.array(frequencies)
    y1=numpy.log(y1)
    pl.plot(x1,y1)
    pl.xlabel('Log rank')
    pl.ylabel('Log count')
    pl.savefig('zipfs.jpg')

    

def return_tag_dict():
    tag_dict=defaultdict(int) 
    with open("data/alltags.txt","r") as readfile:
        for tags in readfile.read().split("\n"):
            for tag in tags.split(" "):
                tag_dict[tag]+=1
    return tag_dict

def return_tagset():
    taglist=[]
    with open("data/alltags.txt","r") as readfile:
        for tags in readfile.read().split("\n"):
            for tag in tags.split(" "):
                #tag_dict[tag]+=1
                taglist.append(tag)

    return set(taglist)

trainset=defaultdict(int)
top834=pickle.load(open('top834.pkl','rb'))

def getQ_top834T(qfile,tfile):
    global trainset,top834
    count=0
    doccount=0
    #outq=open('superQother.txt','w')
    #outt=open('superTother.txt','w')
    with open(qfile,"r") as q:
        with open(tfile,"r") as t:
            for question,tagline in izip(q,t):
                doccount+=1
                for tag in tagline.split(" "):
                    if (tag in top834) and (trainset[tag]<40):
                        #outq.write(question)
                        #outt.write(tagline)
                        count+=1
                        trainset[tag]+=1
                        #print question
                        #print "TAG: "+tag
                        #print tagline
                        #raw_input("")
                        if count%1000==0:
                            print count,doccount
                        break
                    #elif (trainset[tag]>=40):
                        #print tag
                if sum([pair[1] for pair in trainset.items()])>33000:
                    break
    #outq.close()
    #outt.close()



def word_topic(topics,words):
    
    tags=[]
    pkl=open('superdata0.05-33k-150-20.pkl','rb')
    topic_dist=pickle.load(pkl)
    phi=pickle.load(pkl)
    voca=pickle.load(pkl)
    pkl.close()
    print "unpickled!"
    tag_dict=defaultdict(int)
    with open("data/tags.txt","r") as readfile:
        for tag in readfile.read().split("\n"):
            tag_dict[tag]+=1  
    print "tag_dict!"
    for i in xrange(topic_dist.shape[0]):
        tags.append([])
        top5 = numpy.argsort(topic_dist[i])
        top5 = top5[len(top5)-topics:len(top5)]   ##5
        for topic in top5:
            wc = 0
            for w in numpy.argsort(-phi[topic]):    ##[:5]:  
                if tag_dict[voca[w]] != 0:
                    if(wc>words):                   ##wc>4
                        break
                    tags[i].append(voca[w])
                    wc += 1
    print "topic_dist!"
    with open("superPT0.05-150-20-"+str(topics)+str(words)+".txt","w") as tag_output:
        for i in xrange(topic_dist.shape[0]):
            for j in xrange(len(tags[i])):
                print >>tag_output, tags[i][j] + " ",
            print >>tag_output, "\n", 
    
def check_sys_args():
    if len(sys.argv) < 2:
        print "Give me an xml file argument!"
        sys.exit(1)

def preprocess(qfile,tfile,ofile):
    postags=['FW','NP','NN',"NNP","NNS","NNPS"]
    ##f=open("data/Q67.txt","w")
    ##q=open("data/T67.txt","w")
    doccount=0
    with open(qfile,"r") as inFile:
        with open(tfile,"r") as tagFile:
            with open(ofile,"w") as outFile:
                count = 0
                for line,tagline in izip(inFile,tagFile):
                    """##
                    if count<250000:
                        count+=1
                        continue

                    if (len(tagline.split(" ")))<5:
                        count+=1
                        continue
                    print count,doccount
                    doccount+=1
                    #print line
                    f.write(line)
                    q.write(tagline)
                    """##
                    line=re.sub(r'<code>(.(?!<code>))*</code>','',line)
                    line=re.sub(r'<[^<>]+>', '', line)
                    line=line.replace('\n',' ')
                    
                    words = nltk.word_tokenize(line)                     
                    
                    words = nltk.pos_tag(words)                          
                    
                    imp_words = " ".join([x[0] for x in words if x[1] in postags])
                    outFile.write(imp_words+' '+tagline)
                    count+=1
                    
                    print count
                    ##if doccount==10000:
                    ##    break
                    
    ##f.close()
    ##q.close()



def main():
    global outfile,parser,handler,tagfile,qfile

    tagfile=open("alltags1.txt","w")
    qfile=open("allquestions1.txt","w")

    parser = xml.sax.make_parser()
    handler = SOHandler()
    parser.setContentHandler(handler)
    
    with open("posts_with_tags1.txt","w") as outfile:
	    parser.parse("stackoverflow.com.7z/Posts.xml")

#if __name__ == "__main__":
#    main()
