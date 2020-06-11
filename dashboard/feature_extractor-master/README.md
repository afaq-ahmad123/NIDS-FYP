# feature_extractor
Flowbased network packet feature extractor in Python

note: I have integrated another tool available online https://github.com/caesar0301/pkt2flow.
So I acknowledge that "pkt2flow" tool is not my work. 
It is preferable to use linux OS to run this tool smoothly.

This tool enables you to extract flow based features from packet capture (pcap file) over a certain amount of time. 
The output of this tools is a csv file that contains one flow per row, in other words it outputs a dataset which can be used
for anomaly detection using Machine Learning/ Deep Learning models. This was created for research purpose i.e University
Final Year Project: "Advanced Network Intrusion Detection System using Deep Learning".

See flow features at : https://github.com/ammarhaiderak/feature_extractor/blob/master/IMG-20200216-WA0000.jpg

Following are instructins to run the tool:
1. install packages by following this link: https://github.com/ammarhaiderak/pkt2flow
2. install tshark package
3. replace the password in variable 'p' at line 25 in file main.py with the password of your root user of linux OS
4. after installing all the required packages run "main.py" file

note: don't change the directories of the files they should be in working directory to run without problem & Linux OS is 
preferable to run this tool.

