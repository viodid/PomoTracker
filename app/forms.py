# forms.py
from django import forms


class ProfileForm(forms.Form):
    image = forms.ImageField(required=False, label='Change profile picture')
    shortBreak = forms.IntegerField(required=False, label='Short break time',
                                    min_value=1, max_value=60, initial=5)
    longBreak = forms.IntegerField(required=False, label='Long break time',
                                   min_value=1, max_value=60, initial=15)
    # focusColor = forms.ChoiceField(required=False, label='Theme color',
    #                               choices=[('#f1c232', 'Yellow'),
    #                                   ('#ADFF2F', 'Green'),
    #                                   ('#FF6347', 'Red'),
    #                                   ('#00BFFF', 'Blue'),
    #                                   ('#FFD700', 'Gold'),
    #                                   ('#FF69B4', 'Pink'),
    #                                   ('#FFA500', 'Orange')])
    startSound = forms.ChoiceField(required=False, label='Focus sound',
                                   choices=[('#ding', 'Ding'),
                                       ('#folks', 'Looney Tunes')])
    stopSound = forms.ChoiceField(required=False, label='Break sound',
                                  choices=[('#whoosh', 'Whoosh'),
                                      ('#minion', 'Minion')])
