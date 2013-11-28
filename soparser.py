#!/usr/bin/env python
# http://paste.org/8946 "no" 2009
# Updated by Tero Karvinen http://TeroKarvinen.com

from collections import defaultdict
import xml.sax.handler
import xml.sax
import sys
import re

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
            
            
def return_tag_dict():
    tag_dict=defaultdict(int) 
    with open("alltags.txt","r") as readfile:
        for tags in readfile.read().split("\n"):
            for tag in tags.split(" "):
                tag_dict[tag]+=1
    return tag_dict

def check_sys_args():
    if len(sys.argv) < 2:
        print "Give me an xml file argument!"
        sys.exit(1)

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
