from django import forms


class OrderingForm(forms.Form):
    order = forms.ChoiceField(label='Сортировать',
                              choices=[['name', 'по алфавиту (а-я)'],
                                       ['-name', 'по алфавиту (я-а)'],
                                       ['brand', 'по бренду (а-я)'],
                                       ['-brand', 'по бренду (я-а)'],
                                       ['price', 'сначала дешевле'],
                                       ['-price', 'сначала дороже']])
