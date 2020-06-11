#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 23:18:18 2020

@author: ammar
"""
import os
#import subprocess
#import getpass


#import packet_feat_ext as pfe

import feat_ext as fe
#subprocess.call(['tshark','-i','-S','-a'])

#pcapfile=input("Enter path of pcapfile")

dur_of_cap=300
#os.popen("sudo -S tshark -i wlo1 -a duration:3000 > file").write("123812")


def run_sudo_command(command):
    p='123812'
    #getpass.getpass(prompt='Password: ', stream=None) 
    
    os.system('echo %s|sudo -S %s' % (p, command))


basepath='outdir/'
directories=['others','tcp_nosyn','tcp_syn','udp']


command='tshark -i wlo1 -a duration:'+str(dur_of_cap)+' -w capture'


print('Capturing Packets for '+str(dur_of_cap)+' seconds... ')
run_sudo_command(command)


print('Extracting Flows...')
os.system('./pkt2flow-master/pkt2flow -u -v -x -o '+basepath+' capture')


#a,b,c=os.walk(basepath+directories[0])
#print(a,b,c)


i=0     #flow no
for d in range(len(directories)):
    for root, dirs, files in os.walk(basepath+directories[d], topdown=False):
        for name in files:
            full=os.path.join(root, name)
            command2='tshark -r '+str(full)+' -T json > '
            run_sudo_command(command2+'f/'+str(i)+'.json')
            i+=1
            



name=input('Enter the file name: ')


j=0
f,result_writer=fe.ffopen(name,'flowfeats')
print('Creating Dataset...')

while j<i:
    fe.process('f/'+str(j)+'.json',f,result_writer,j)
    j+=1

fe.ffclose(f)




