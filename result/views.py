from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

labels = []
data = {"lstm":[52.4, 2.9,44,0.7],
             "Auto-encoder":[42.4, 2.9,50,5.7],
             "DNN":[32.4,7.9,10,50.7],
             "Naive-Bayes":[42.4, 2.9,50,5.7]
             }
models = ["lstm","Auto-encoder","DNN","Naive-Bayes"]
acc = [90, 95, 94, 98]
ind = 'lstm'


context = {
        'models': models,
        'acc': acc,
        'data': data,
        'ind': ind,

    }

@login_required(login_url='/login/')
def home(request):
    labels = ["Dos", "R2L", "normal", "Probe"]
    pk = request.session.get('results')
    data = pk['data']
    print(data)
    models = pk['models']
    print(models)
    acc = pk['acc']
    print(acc)
    ind = pk['ind']
    print("ind : "+ str(ind))
    return render(request, 'result/charts.html', {
        'labels': labels,
        'data': data,
        'models': models,
        'acc': acc,
        'ind': ind,
    })