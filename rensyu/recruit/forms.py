from django import forms
from .models import Recruit

class RecruitForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('新規応募', '新規応募'),
        ('書類選考NG', '書類選考NG'),
        ('面接調整中', '面接調整中'),
        ('面接確定', '面接確定'),
        ('面接NG', '面接NG'),
        ('オファ面調整中', 'オファ面調整中'),
        ('オファ面確定', 'オファ面確定'),
        ('オファ面NG', 'オファ面NG'),
        ('辞退', '辞退'),
    ]

    DOCUMENTS_STATUS_CHOICES = [
        ('提出済み', '提出済み'),
        ('履歴書のみ', '履歴書のみ'),
        ('職務経歴書のみ', '職務経歴書のみ'),
        ('未提出', '未提出'),
    ]

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    documents_status = forms.ChoiceField(
        choices=DOCUMENTS_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Recruit
        fields = ['name', 'status', 'entry_day', 'documents_status']
        widgets = {
            'entry_day': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        } 