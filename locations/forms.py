from django import forms


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label='CSV file to import')
    encoding = forms.ChoiceField(label='File encoding',
                                 choices=([(k, k) for k in ('utf-8',
                                                            'iso-8859-15')]))
    delimiter = forms.ChoiceField(label='Column separator',
                                  choices=([(k, k) for k in (';',
                                                             ',')]))
