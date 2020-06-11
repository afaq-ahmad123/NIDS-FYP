from django.shortcuts import render
import csv

#import django_pandas as pd
import pandas as pd
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    return render(request,'tables/tables.html')


@login_required(login_url='/login/')
def show(request):
    file_ = open(os.path.join(settings.BASE_DIR, 'f.csv'))
    data = list(csv.reader(file_))
    #csvfile = request.FILES['csv_file']
    #csvfile.name
    #data = pd.read_csv(file_)
    #data_html = data.to_html()
    context = {'loaded_data': data}
    return render(request, "tables/tables.html", context)