from django import forms

class CPRForm(forms.Form):
    instruments = [('NIFTY', 'NIFTY'), ('BANKNIFTY', 'BANKNIFTY')]
    instrument = forms.ChoiceField(label="Instrument", choices=instruments)

    conditional_trade = forms.BooleanField(label='Conditional Trade', required=False)

    onlongsignals = [('long call', 'long call'), ('short call', 'short call'), ('long put', 'long put'), ('short put', 'short put')]
    onlongsignal = forms.ChoiceField(label="On Long Signal", choices=onlongsignals, required=False)

    # onlongstrikeselections =  [('premium', 'premium'), ('atm', 'atm'), ('greeks', 'greeks')]
    onlongstrikeselections =  [('atm', 'atm')]
    onlongstrikeselection = forms.ChoiceField(label="Strike Selection", choices=onlongstrikeselections, required=False)

    onshortsignals = [('long call', 'long call'), ('short call', 'short call'), ('long put', 'long put'), ('short put', 'short put')]
    onshortsignal = forms.ChoiceField(label="On Short Signal", choices=onshortsignals, required=False)

    # onshortstrikeselections =  [('premium', 'premium'), ('atm', 'atm'), ('greeks', 'greeks')]
    onshortstrikeselections =  [('atm', 'atm')]
    onshortstrikeselection = forms.ChoiceField(label="Strike Selection", choices=onshortstrikeselections, required=False)

    # cpr fields
    from_date = forms.DateField(label="From Date", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    to_date = forms.DateField(label="To Date", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    cpr_range = forms.FloatField(label="CPR Range", required=False, initial=0.00388)
    cpr_optimize = forms.BooleanField(label='Optimize', required=False, disabled=True)
    cpr_min = forms.IntegerField(label="Min", required=False)
    cpr_max = forms.IntegerField(label="Max", required=False)
    cpr_step = forms.IntegerField(label="Step", required=False)
    exit_type = forms.ChoiceField(label="Exit Type", choices=[("time price", "time price"), ("action", "action")], required=False)

    trailing_types = [('points', 'points'), ('percentage', 'percentage'), ('structural', 'structural')]
    trailing_type = forms.ChoiceField(label="Trailing Type", choices=trailing_types, required=False)
