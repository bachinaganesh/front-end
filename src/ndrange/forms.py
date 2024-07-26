from django import forms

class NDRangeFrom(forms.Form):
    from_date = forms.DateField(label="From Date", widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(label="To Date", widget=forms.DateInput(attrs={'type': 'date'}))
    exit_time = forms.TimeField(label="Exit Time", widget=forms.TimeInput(attrs={'type': 'time'}))
    symbols = [('NIFTY', 'NIFTY'), ('BANKNIFTY', 'BANKNIFTY')]
    symbol = forms.ChoiceField(label="Symbol", choices=symbols)
    nd_range_values = [('2', 2), ('3', 3), ('4', 4)]
    nd_range = forms.ChoiceField(label="Nd_range", choices=nd_range_values)
    initial_stop_loss = forms.IntegerField(label="Initial Stop Loss")
    x = forms.IntegerField(label="X")
    y = forms.IntegerField(label="Y")