from django.shortcuts import render, redirect
from .forms import StrategyListForm
# Create your views here.

class Visualizer:
    @staticmethod
    def home_page(request):
        if request.method == 'POST':
            form = StrategyListForm(request.POST)
            if form.is_valid():
                selected_strategy = form.cleaned_data['strategy']
                if selected_strategy == 'ndrange':
                    return redirect('ndrange/')
                elif selected_strategy == 'cpr':
                    return redirect('cpr/')
        else:
            form = StrategyListForm()
            return render(request, 'baseapp/home.html', {'form': form})
    @staticmethod
    def display_trades(request, data):
        return render(request, 'baseapp/trades.html', {'data': data})
