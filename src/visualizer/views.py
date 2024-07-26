from django.shortcuts import render
import json
from datetime import datetime, timedelta
import pandas as pd
from utilities.visualizer import plotting_chart
from plotly import graph_objects as go
import os

# handle the trade when user click on trade row
def handle_trade(request, filepath, datetime):
    future_chart, options_chart, trade = plotting_chart.filter_trade(filepath, datetime)
    return render(request, 'visualizer/plot_chart.html', context={'futures_chart':future_chart,  'options_chart': options_chart, 'trade': trade})


from django.shortcuts import render, redirect
from .forms import FileForm
from .models import File

def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()
            data = get_extended_report_data(file_instance.file.path)
            return render(request, 'visualizer/trade_table.html', {'data': data, 'file_path': file_instance.file.path})
    else:
        form = FileForm()
    return render(request, 'visualizer/upload.html', {'form': form})

def file_list(request):
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})

def get_extended_report_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data
