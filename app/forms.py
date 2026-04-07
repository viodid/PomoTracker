"""Forms for the app."""
from django import forms
import pytz


class ProfileForm(forms.Form):
    """Form for editing user profile."""
    image = forms.ImageField(
        required=False, label='Change profile picture',
        widget=forms.ClearableFileInput(attrs={
            'class': 'settings-file-input', 'accept': 'image/*'
        })
    )
    shortBreak = forms.IntegerField(
        required=False, label='Short break',
        min_value=1, max_value=60, initial=5,
        widget=forms.NumberInput(attrs={
            'class': 'settings-input', 'placeholder': '5'
        })
    )
    longBreak = forms.IntegerField(
        required=False, label='Long break',
        min_value=1, max_value=60, initial=15,
        widget=forms.NumberInput(attrs={
            'class': 'settings-input', 'placeholder': '15'
        })
    )
    theme = forms.ChoiceField(
        required=False, label='Theme',
        choices=[('default', 'Default'),
                 ('white', 'White'),
                 ('forest', 'Forest'),
                 ('aquamarine', 'Aquamarine'),
                 ('garnet', 'Garnet'),
                 ('coral', 'Coral')],
        widget=forms.Select(attrs={
            'class': 'settings-input', 'id': 'theme-select'
        })
    )
    startSound = forms.ChoiceField(
        required=False, label='Focus sound',
        choices=[('#ding', 'Ding'),
                 ('#folks', 'Looney Tunes')],
        widget=forms.Select(attrs={'class': 'settings-input sound-select'})
    )
    stopSound = forms.ChoiceField(
        required=False, label='Break sound',
        choices=[('#whoosh', 'Whoosh'),
                 ('#minion', 'Minion')],
        widget=forms.Select(attrs={'class': 'settings-input sound-select'})
    )
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.common_timezones],
        required=False,
        label='Timezone',
        initial='UTC',
        widget=forms.Select(attrs={
            'class': 'settings-input', 'id': 'timezone-select'
        })
    )
