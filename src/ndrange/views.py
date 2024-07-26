from django.shortcuts import render, redirect
from .forms import NDRangeFrom
from django.http import HttpResponse

# Create your views here.
class NdRangeStrategy:
    def __init__(self, from_date, to_date, exit_time, symbol, x, y) -> None:
        self.from_date = from_date
        self.to_date = to_date
        self.exit_time = exit_time
        self.symbol = symbol
        self.x = x
        self.y = y
    def execute_strategy(self):
        self.data = {'from_date': self.from_date, 'to_date': self.to_date, 's_type': 'NDRANGE'}
        return self.data
    
def execute(request):
    form = NDRangeFrom(request.POST)
    if form.is_valid():
        from_date = (form.cleaned_data['from_date']).strftime('%Y-%m-%d')
        to_date = (form.cleaned_data['to_date']).strftime('%Y-%m-%d')
        exit_time = form.cleaned_data['exit_time']
        symbol = form.cleaned_data['symbol']
        nd_range = form.cleaned_data['nd_range']
        ist_form_value = int(form.cleaned_data['initial_stop_loss'])
        x = int(form.cleaned_data['x'])
        y = int(form.cleaned_data['y'])
        nd_range_strategy = NdRangeStrategy(from_date, to_date, exit_time, symbol, x, y)
        data = nd_range_strategy.execute_strategy()
        return render(request, 'baseapp/trades.html', {'data': data})
        # return redirect('baseapp:trades', data=data)
    return render(request, 'ndrange/nd_range_home.html', {'form': form})