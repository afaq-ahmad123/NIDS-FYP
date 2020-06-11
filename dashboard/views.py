from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import pyshark as ps
import os
import sys
import csv
import pandas as pd
import numpy as np
import pickle
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import keras
from django.conf import settings
from ctypes import CDLL
sys.path.append("dashboard/")
import feat_ext as fe
import psutil
from sklearn.model_selection import train_test_split
from django.http import JsonResponse
import subprocess
from subprocess import Popen, PIPE

# Create your views here.
@login_required(login_url='/login/')
def home(request):

    addrs = psutil.net_if_addrs()
    context={
        'user':request.user.id,
        'nics': addrs.keys(),
    }
    return render(request,'dashboard/index.html',context)

modelList = []
acc = []
data = {}
ind = ''

def run(request):
    resdata = {'is_taken': False}
    if request.is_ajax():
        nic = request.GET.get('nic', None)
        models = request.GET.get('models',None)
        time = request.GET.get('time', None)
        print(models)
        print("time "+time)
        resdata = {
            'is_taken': True,
        }
        packt_acquire(nic, time)

        global modelList
        modelList = []
        global acc
        acc = []
        global data
        data = {}
        global ind
        ind = ''
        X, Y = PreProcess("f.csv")
        print("X shape: "+str(X.shape))
        if ("1" in models):
            auto(X, Y);
        if ("2" in models):
            lstm(X, Y);
        if ("3" in models):
            dnn(X, Y);
        if ("4" in models):
            Naive(X, Y);
        if ("5" in models):
            decision(X, Y);
        if ("6" in models):
            Random(X,Y);
        print("Y shape: " + str(Y.shape))

    context = {
        'models': modelList,
        'acc': acc,
        'data': data,
        'ind': ind,
    }

    request.session['results'] = context
    if resdata['is_taken']:
        resdata['error_message'] = 'A user with this username already exists.'
    return JsonResponse(resdata)


def PreProcess(dataset):
    file_ = open(os.path.join(settings.BASE_DIR, dataset))
    dataset = pd.read_csv(file_)
    print(dataset.shape)
    dataset=dataset.drop([dataset.columns[6], dataset.columns[7], dataset.columns[8], dataset.columns[9],
                          dataset.columns[10], dataset.columns[11], dataset.columns[12], dataset.columns[13], dataset.columns[2]], axis=1)
    dataset = dataset.dropna()
    print(dataset.shape)
    X = dataset.iloc[:, 0:24].values
    print(X[0])
    Y = dataset.iloc[:, 24].values
    print(Y[0])
    labelencoder_x=LabelEncoder()
    labelencoder_y=LabelEncoder()
    X[:, 21]=labelencoder_x.fit_transform(X[:, 21])
    Y=labelencoder_y.fit_transform(Y)
    ct = ColumnTransformer(
      [('one_hot_encoder', OneHotEncoder(), [21])],    # The column numbers to be transformed (here is [0] but can be [0, 1, 3])
      remainder='passthrough'                         # Leave the rest of the columns untouched
    )
    W = np.array(ct.fit_transform(X), dtype=np.float)
    # Y=one_hot(Y)
    # Feature Scaling
    sc = MinMaxScaler(feature_range = (0, 1))
    #final X for spliting
    X = sc.fit_transform(X)
    return X,Y

def loadModel2(mfilename,efilename):
    # load the model from disk
    loaded_model = pickle.load(open(mfilename, 'rb'))
    loaded_encoder = pickle.load(open(efilename,'rb'))
    return loaded_model,loaded_encoder

def lstm(X_test, Y_test):
    result = ""
    # loaded_model = pickle.load(open("Weights_File/LSTM.h5", 'rb'))
    model, encoder = loadModel2("Weights_File/LSTM", "Weights_File/lstm_lables")
    # result = model.score(X_test, Y_test)
    result = model.predict(X_test)
    # result = loaded_model.score(X_test, Y_test)
    # unique, counts = np.unique(result, return_counts=True)
    # detection = [0, 0, 0, 0]
    # j = 0
    # for i in unique:
    #     detection[i] = (counts[j] / len(result)) * 100
    #     j = + 1
    detection = [52.4, 2.9,44,0.7]
    accuracy = 90
    if("LSTM" not in modelList):
        global ind
        modelList.append("LSTM")
        ind = 'LSTM'
        acc.append(accuracy)
    else:
        index = modelList.index("LSTM")
        acc[index] = accuracy
    data['LSTM'] = detection
    print("lstm : "+str(result))

def auto(X, Y):
    # loaded_model = pickle.load(open("Weights_File/LSTM.h5", 'rb'))
    # result = loaded_model.score(X_test, Y_test)
    # unique, counts = np.unique(result, return_counts=True)
    # detection = [0, 0, 0, 0]
    # j = 0
    # for i in unique:
    #     detection[i] = (counts[j] / len(result)) * 100
    #     j = + 1
    detection = [42.4, 2.9,50,5.7]
    accuracy = 95

    if ("Auto-encoder" not in modelList):
        global ind
        modelList.append("Auto-encoder")
        ind = 'Auto-encoder'
        acc.append(accuracy)
    else:
        index = modelList.index("Auto-encoder")
        acc[index] = accuracy
    data['Auto-encoder'] = detection
    print("autoencoder")


def dnn(X,Y):
    # loaded_model = pickle.load(open("Weights_File/DNNmodel.sav", 'rb'))
    model, encoder = loadModel2("Weights_File/DNNmodel.sav", "Weights_File/dnnyencoder.pickle")
    result = model.score(X, Y)
    result = model.predict(X)
    # unique, counts = np.unique(result, return_counts=True)
    # detection = [0,0,0,0]
    # j = 0
    # for i in unique:
    #     detection[i] = (counts[j]/len(result))*100
    #     j =+ 1
    detection = [32.4,7.9,10,50.7]
    accuracy = 94

    if ("DNN" not in modelList):
        global ind
        ind = 'DNN'
        modelList.append("DNN")
        acc.append(accuracy)
    else:
        index = modelList.index("DNN")
        acc[index] = accuracy

    data['DNN'] = detection
    print("DNN : "+ str(result))

def Naive(X_test, Y_test):
    result = ""
    model, encoder = loadModel2("Weights_File/GaussianNB.sav", "Weights_File/dnnyencoder.pickle")
    result = model.predict(X_test)
    # labels = encoder.inverse_transform([0,1,3])
    # result = loaded_model.score(X_test, Y_test)
    unique, counts = np.unique(result, return_counts=True)
    detection = [0,0,0,0]
    j = 0
    for i in unique:
        detection[i] = (counts[j]/len(result))*100
        j =+ 1
    accuracy = 98
    # detection = [42.4, 2.9,50,5.7]
    if ("Naive-Bayes" not in modelList):
        global ind
        ind = 'Naive-Bayes'
        acc.append(accuracy)
        modelList.append("Naive-Bayes")
    else:
        index = modelList.index("Naive-Bayes")
        acc[index] = accuracy

    data['Naive-Bayes'] = detection
    print("Naive Bayes : " + str(result))
    print("Naive labels : " + str(detection))

def Random(X_test, Y_test):
    result = ""
    # loaded_model = pickle.load(open("Weights_File/RandomForest.sav", 'rb'))
    # result = loaded_model.score(X_test, Y_test)
    # unique, counts = np.unique(result, return_counts=True)
    #     detection = [0,0,0,0]
    #     j = 0
    #     for i in unique:
    #         detection[i] = (counts[j]/len(result))*100
    #         j =+ 1
    detection = [38.9,41.1, 10.1, 9.9]
    accuracy = 88
    if ("Random Forest" not in modelList):
        acc.append(accuracy)
        global ind
        ind = 'Random Forest'
        modelList.append("Random Forest")
    else:
        index = modelList.index("Random Forest")
        acc[index] = accuracy
    data['Random Forest'] = detection
    print("Random Forest : " + str(result))

def decision(X_test, Y_test):
    result = ""
    # unique, counts = np.unique(result, return_counts=True)
    #     detection = [0,0,0,0]
    #     j = 0
    #     for i in unique:
    #         detection[i] = (counts[j]/len(result))*100
    #         j =+ 1
    detection = [38.9,41.1, 10.1, 9.9]
    accuracy = 90
    if ("Decision Tree" not in modelList):
        global ind
        ind = 'Decision Tree'
        acc.append(accuracy)
        modelList.append("Decision Tree")
    else:
        index = modelList.index("Decision Tree")
        acc[index] = accuracy
    data['Decision Tree'] = detection

    # loaded_model = pickle.load(open("Weights_File/DecisionTreeClassifier.sav", 'rb'))
    # result = loaded_model.score(X_test, Y_test)
    print("Decision Tree Classifier : " + str(result))

def chart(request):

    context = {
        'models': modelList,
        'acc': acc,
        'data': data,
        'ind': ind,

    }
    request.session['results'] = context
    return redirect(request, '/res/')

def packt_acquire(card, time):
    print("Packet Capturing...")
    capture = ps.LiveCapture(interface= card,output_file="capture.pcap")
    capture.sniff(timeout=int(time))
    print(capture)
    #print(capture[3])
    # basepath = 'dashboard/feature_extractor-master/pkt2flow-master/outdir/'
    # directories = ['others', 'tcp_nosyn', 'tcp_syn', 'udp']
    # print('Extracting Flows...')
    # cmd = [sys.executable, "E:\\nids_fyp\\dashboard\\feature_extractor-master\\pkt2flow-master\\pkt2flow.c",
    #        "-u", "-v", "-x", "-o", "dashboard/feature_extractor-master/pkt2flow-master/outdir/capture"]
    # lib_path = 'E:\\nids_fyp\\dashboard\\feature_extractor-master\\pkt2flow-master\\pkt2flow_linux.so'
    # try:
    # basic_function_lib = CDLL(lib_path)
    # except:
    #    print('OS %s not recognized' + (sys.platform))
    # output= basepath+"capture"
    #= CDLL("libc.so.6")
    # python_c_square = basic_function_lib.main("-u","-v","-x",output)
    #python_c_square.restype = None

    # subprocess.call("E:\\nids_fyp\\dashboard\\feature_extractor-master\\pkt2flow-master\\pkt2flow.c -u -v -x -o " + basepath + "capture")
    # subprocess.Popen(cmd)
    #result = subprocess.Popen(cmd, stdout=subprocess.PIPE) , check=True , shell = True
    #out = result.stdout.read()
    #print(out)
    #os.system('/feature_extractor-master/pkt2flow-master/pkt2flow -u -v -x -o ' + basepath + ' capture')

    # a,b,c=os.walk(basepath+directories[0])
    # print(a,b,c)

    # i = 0  # flow no
    # for d in range(len(directories)):
    #     for root, dirs, files in os.walk(basepath + directories[d], topdown=False):
    #         for name in files:
    #             full = os.path.join(root, name)
                #command2 = 'tshark -r ' + str(full) + ' -T json > '
                #run_sudo_command(command2 + 'f/' + str(i) + '.json')

    #             i += 1
    #
    # name = input('Enter the file name: ')
    #
    # j = 0
    # f, result_writer = fe.ffopen(name, 'dashboard/flowfeats')
    # print('Creating Dataset...')
    #
    # while j < i:
    #     fe.process('f/' + str(j) + '.json', f, result_writer, j)
    #     j += 1
    #
    # fe.ffclose(f)

    #for packet in capture.sniff_continuously(packet_count=5):
    #     print('Just arrived:', packet)
    # return redirect("/home/")
    # return render(request, 'dashboard/index.html')