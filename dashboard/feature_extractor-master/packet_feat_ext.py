#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 00:18:42 2020

@author: ammar
"""

import json
import csv



#print(type(packets))
#print(packets)
unique_feats=[]
collabels=None

def recprintvals(obj,features,features2,key=None):    #recursive function to extract features
  global unique_feats
  if type(obj) is not dict:               #base case  
    if key not in unique_feats:
      unique_feats.append(key)
    #print(key,':',obj)
    features.append({key:obj})
    features2[key]=obj

  if type(obj) is dict:                   #recursive case
    for x in obj.keys():
      recprintvals(obj[x],features,features2,x)


def getlabels(featurs):
  temp=[]
  for f in featurs:
    temp.append(list(f.keys())[0])
  return temp



def getRefFeats():
    reader=[]
    #f=open('reffeats','r')
    #reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    
    with open('reffeats','r') as f:
        for l in f:
            reader.append(str(l[0:l.find(',')]))
    
    
    reader=list(reader)
    return reader
    
    

def printlabels(result_writer):
    global collabels
    collabels=getRefFeats()
    #getlabels(packetlist[maxxind])
    
    '''
    if 'tcp.payload' in collabels:
        collabels.remove('tcp.payload')
    if 'tls.app_data' in collabels:
        collabels.remove('tls.app_data')
    
    print(collabels)
    '''
    
    result_writer.writerow(collabels)
    


def ffopen(outputfile):
    f2=open(outputfile,'a+')
    result_writer = csv.writer(f2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    printlabels(result_writer)
    
    
    return f2,result_writer



def ffclose(f):
    f.close()
    



#print(getRefFeats())
def process(packetsfile,f2,result_writer,flowno):#processes 1 flow at a time
    global collabels
    packets=''
    
    filename=packetsfile
    
    with open(filename,'r') as f:
      for l in f:
        packets=packets+l
    
    
    packets = (json.loads(packets))
    #first=True
    #collabels=[]              #column labels
    
    #maxx=0
    #maxxind=0
    packetlist=[]
    #i=0
    
    inter_pkt_arrival=0
    urgent_count=0
    wrong_frags=0
    
    for packet in packets:      #iterates of n packets in the flow
      vals=packet['_source']['layers']
      #headings=packet['_source']['layers'].keys()
      
      features=[]
      features2={}
      recprintvals(vals,features,features2)
      features.append({'flow_no':flowno})   #every packet of this flow will have same flowno
      #packetlist.append(features)  
      features2['flow_no']=flowno
      #print(features2)
      packetlist.append(features2)
      
      
      inter_pkt_arrival+=float(features2.get('frame.time_delta'))
      
      if features2.get('tcp.urgent_pointer') is not None:
          if int(features2.get('tcp.urgent_pointer')) == 1 :
              urgent_count+=1
          
      if features2.get('ip.frag_offset') is not None and features2.get('ip.flags.mf') is not None:      
          if int(features2.get('ip.frag_offset')) < 0 or int(features2.get('ip.flags.mf')) != 1:
              wrong_frags+=1
      
     
    inter_pkt_arrival/=len(packets)
    
    
    
       
    

    
    
    
    
    for p in packetlist:
        rowtowrite=['']*len(collabels)
        #print(p)
        for c in collabels:
            v=p.get(c)
            rowtowrite[collabels.index(c)]=v
            rowtowrite[collabels.index('inter_pkt_arrival')]=inter_pkt_arrival
            rowtowrite[collabels.index('duration')]=packetlist[len(packetlist)-1].get('frame.time_relative')
            rowtowrite[collabels.index('src_bytes')]=packetlist[len(packetlist)-1].get('tcp.ack_raw')
            rowtowrite[collabels.index('dst_bytes')]=packetlist[len(packetlist)-1].get('tcp.seq_raw')
            rowtowrite[collabels.index('no_of_urgent')]=urgent_count
            rowtowrite[collabels.index('no_of_wrong_frags')]=wrong_frags
            
        result_writer.writerow(rowtowrite)
    

    '''        
    for p in packetlist:
      rowtowrite=['']*len(collabels)
      #p=packetlist[0]
      for pp in p:   #pp is features array
        feat_name=list(pp.keys())[0]
        if feat_name in collabels:
          rowtowrite[collabels.index(feat_name)]=list(pp.values())[0]
      result_writer.writerow(rowtowrite)
      #print(rowtowrite)
      #print(rowtowrite)
     '''
    #    f2.close()


#process('file.json','f.csv')
    
    
 
