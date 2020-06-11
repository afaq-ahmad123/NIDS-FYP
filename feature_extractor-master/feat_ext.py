#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 00:18:42 2020

@author: ammar
"""

import json
import csv
import math


#print(type(packets))
#print(packets)
unique_feats=[]
collabels=None

def recprintvals(obj,features,key=None):    #recursive function to extract features
  global unique_feats
  if type(obj) is not dict:               #base case  
    if key not in unique_feats:
      unique_feats.append(key)
    features[key]=obj

  if type(obj) is dict:                   #recursive case
    for x in obj.keys():
      recprintvals(obj[x],features,x)


def getlabels(featurs):
  temp=[]
  for f in featurs:
    temp.append(list(f.keys())[0])
  return temp



def getRefFeats(featfile):
    reader=[]
 
    with open(featfile,'r') as f:
        for l in f:
            reader.append(str(l[0:l.find(',')]))
    
    
    reader=list(reader)
    return reader
    
    
def converttodict(lst):
    temp={}
    for x in lst:
        temp[x]=0
    
    return temp



def printlabels(result_writer,featfile):
    global collabels
    collabels=getRefFeats(featfile)  
    result_writer.writerow(collabels)
    


def ffopen(outputfile,featfile):
    f2=open(outputfile,'w+')
    result_writer = csv.writer(f2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    printlabels(result_writer,featfile)
    
    
    return f2,result_writer



def ffclose(f):
    f.close()
    


def process(packetsfile,f2,result_writer,flowno):#processes 1 flow at a time
    global collabels
    packets=''
    
    filename=packetsfile
    
    with open(filename,'r') as f:
      for l in f:
        packets=packets+l
    
    
    packets = (json.loads(packets))

    packetlist=[]
    
        
    flowfeats={}
    l=getRefFeats('flowfeats')
    flowfeats=converttodict(l)
    
    flowfeats['minbiat']=9999
    flowfeats['minfiat']=9999
    flowfeats['minfpktl']=999999
    flowfeats['minbpktl']=999999
    #flowfeats['maxbiat']=-9999
    #flowfeats['maxfiat']=-9999
    #flowfeats['maxfpktl']=-9999
    #flowfeats['maxbpktl']=-9999
    
    
    
    
    
    srcip=None
    dstip=None
    
    fiats=[]
    biats=[]
    flens=[]
    blens=[]
    
    itr=0
    
    for packet in packets:
      vals=packet['_source']['layers']
  
      features={}
      recprintvals(vals,features)
      features['flow_no']=flowno
      
      packetlist.append(features)
      
      
      flowfeats['inter_pkt_arrival']+=float(features.get('frame.time_delta'))
      
      flowfeats['flow_no']=flowno
      
      
      
      if itr==0:            #setting the source and destination using first packet of the flow
          srcip=features.get('ip.src')
          dstip=features.get('ip.dst')
          flowfeats['protocol']=features.get('frame.protocols')
          flowfeats['src_ip']=srcip
          flowfeats['dst_ip']=dstip
          
          flowfeats['src_port']=features.get('tcp.srcport')
          flowfeats['dst_port']=features.get('tcp.dstport')
          if features.get('tcp.srcport') is None:
              flowfeats['src_port']=features.get('udp.srcport')
              flowfeats['dst_port']=features.get('udp.dstport')
          
            
          if flowfeats['src_port']!=0 and flowfeats['dst_port']!=0:
              if flowfeats['src_port']==flowfeats['dst_port'] and flowfeats['src_ip']==flowfeats['dst_ip']:
                  flowfeats['land']=1
            
            
          flowfeats['src_mac']=features.get('eth.src')
          flowfeats['dst_mac']=features.get('eth.dst')
              
              
              
      itr+=1   
        
      if srcip==features.get('ip.src'):             #forward packets calculations
          if features.get('frame.len') is not None:
              if flowfeats.get('minfpktl') > int(features.get('frame.len')):
                 flowfeats['minfpktl']=int(features.get('frame.len'))
              if flowfeats.get('maxfpktl') < int(features.get('frame.len')):
                 flowfeats['maxfpktl']=int(features.get('frame.len'))
              
              flens.append(int(features.get('frame.len')))  
              flowfeats['meanfpktl']+=int(features.get('frame.len'))         

          if features.get('frame.time_delta') is not None:                
              if flowfeats.get('minfiat') > float(features.get('frame.time_delta')):
                 flowfeats['minfiat']=float(features.get('frame.time_delta'))
              if flowfeats.get('maxfiat') < float(features.get('frame.time_delta')):
                 flowfeats['maxfiat']=float(features.get('frame.time_delta'))              
              
              fiats.append(float(features.get('frame.time_delta')))  
              flowfeats['meanfiat']+=float(features.get('frame.time_delta'))


          flowfeats['fpackets']+=1
              
              
              
      if dstip==features.get('ip.src'):             #backward packets calculations
          if features.get('frame.len') is not None:
              if flowfeats.get('minbpktl') > int(features.get('frame.len')):
                 flowfeats['minbpktl']=int(features.get('frame.len'))
              if flowfeats.get('maxbpktl') < int(features.get('frame.len')):
                 flowfeats['maxbpktl']=int(features.get('frame.len'))
              
              blens.append(int(features.get('frame.len')))
              flowfeats['meanbpktl']+=int(features.get('frame.len'))         
              
            
          if features.get('frame.time_delta') is not None:
              if flowfeats.get('minbiat') > float(features.get('frame.time_delta')):
                 flowfeats['minbiat']=float(features.get('frame.time_delta'))
              if flowfeats.get('maxbiat') < float(features.get('frame.time_delta')):
                 flowfeats['maxbiat']=float(features.get('frame.time_delta'))
                 
              biats.append(float(features.get('frame.time_delta')))
              flowfeats['meanbiat']+=float(features.get('frame.time_delta'))
              
          
          flowfeats['bpackets']+=1
        
        
        
      
      if features.get('tcp.urgent_pointer') is not None:
          if int(features.get('tcp.urgent_pointer')) == 1 :
              flowfeats['no_of_urgent']+=1
          
      if features.get('ip.frag_offset') is not None and features.get('ip.flags.mf') is not None:      
          if int(features.get('ip.frag_offset')) < 0 or int(features.get('ip.flags.mf')) != 1:
              flowfeats['no_of_wrong_frags']+=1
      
     
    flowfeats['inter_pkt_arrival']/=len(packets)
    
       
    if int(flowfeats['fpackets'])>0:    
        for i in range(len(fiats)):
            flowfeats['stdfiat']+=((flowfeats['meanfiat']-fiats[i])**2)/int(flowfeats['fpackets'])
            flowfeats['stdfpktl']+=((flowfeats['meanfpktl']-flens[i])**2)/int(flowfeats['fpackets'])
        
        flowfeats['meanfpktl']/=flowfeats['fpackets']
        flowfeats['stdfiat']=math.sqrt(flowfeats['stdfiat'])
        flowfeats['meanfiat']/=flowfeats['fpackets']
    
    if int(flowfeats['bpackets'])>0:
        for i in range(len(biats)):
            flowfeats['stdbiat']+=((flowfeats['meanbiat']-biats[i])**2)/flowfeats['bpackets']
            flowfeats['stdbpktl']+=((flowfeats['meanbpktl']-blens[i])**2)/flowfeats['bpackets']
            
        flowfeats['stdbiat']=math.sqrt(flowfeats['stdbiat'])
        flowfeats['meanbpktl']/=flowfeats['bpackets']
        flowfeats['meanbiat']/=flowfeats['bpackets']
    
    
    
    
    flowfeats['duration']=packetlist[len(packetlist)-1].get('frame.time_relative')
    flowfeats['src_bytes']=packetlist[len(packetlist)-1].get('tcp.ack_raw')
    flowfeats['dst_bytes']=packetlist[len(packetlist)-1].get('tcp.seq_raw')
    
    
    #print(flowfeats)
    
    rowtowrite=['']*len(collabels)
    for k in flowfeats:
        rowtowrite[collabels.index(k)]=flowfeats.get(k)
    
    result_writer.writerow(rowtowrite)
    
    '''
    
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

'''
j=0
f,result_writer=ffopen('finalflowbased.csv','flowfeats')

while j<199:
    process('f/'+str(j)+'.json',f,result_writer,j)
    j+=1

ffclose(f)

'''