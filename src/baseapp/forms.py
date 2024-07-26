from django import forms

class StrategyListForm(forms.Form):
    STRATEGY_CHOICES = [
        ('ndrange', 'ndrange'),
        ('cpr', 'cpr'),
    ]
    strategy = forms.ChoiceField(choices=STRATEGY_CHOICES)