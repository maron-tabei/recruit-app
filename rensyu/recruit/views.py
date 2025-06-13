from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError
from .models import Recruit
from .forms import PersonalInfoForm, ProgressForm, InterviewReportForm, OfferReportForm

def recruit_list(request):
    recruits = Recruit.objects.all().order_by('-entry_day')
    return render(request, 'recruit/index.html', {'recruits': recruits})

def recruit_create(request):
    if request.method == 'POST':
        personal_form = PersonalInfoForm(request.POST)
        progress_form = ProgressForm(request.POST)
        interview_form = InterviewReportForm(request.POST)
        offer_form = OfferReportForm(request.POST)
        
        forms_valid = all([
            personal_form.is_valid(),
            progress_form.is_valid(),
            interview_form.is_valid(),
            offer_form.is_valid()
        ])
        
        if forms_valid:
            recruit = personal_form.save(commit=False)
            if not recruit.entry_day:
                recruit.entry_day = date.today()
            recruit.save()
            
            progress_form.instance = recruit
            progress_form.save()
            
            interview_form.instance = recruit
            interview_form.save()
            
            offer_form.instance = recruit
            offer_form.save()
            
            messages.success(request, '応募者情報が正常に登録されました。')
            return redirect('recruit_list')
        else:
            messages.error(request, '入力内容に誤りがあります。フォームを再確認してください。')
    else:
        personal_form = PersonalInfoForm()
        progress_form = ProgressForm()
        interview_form = InterviewReportForm()
        offer_form = OfferReportForm()
    
    return render(request, 'recruit/recruit_form.html', {
        'personal_form': personal_form,
        'progress_form': progress_form,
        'interview_form': interview_form,
        'offer_form': offer_form,
        'is_edit': False
    })

def recruit_edit(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    
    if request.method == 'POST':
        personal_form = PersonalInfoForm(request.POST, instance=recruit)
        progress_form = ProgressForm(request.POST, instance=recruit)
        interview_form = InterviewReportForm(request.POST, instance=recruit)
        offer_form = OfferReportForm(request.POST, instance=recruit)
        
        forms_valid = all([
            personal_form.is_valid(),
            progress_form.is_valid(),
            interview_form.is_valid(),
            offer_form.is_valid()
        ])
        
        if forms_valid:
            personal_form.save()
            progress_form.save()
            interview_form.save()
            offer_form.save()
            
            messages.success(request, '応募者情報が正常に更新されました。')
            return redirect('recruit_list')
        else:
            messages.error(request, '入力内容に誤りがあります。フォームを再確認してください。')
    else:
        personal_form = PersonalInfoForm(instance=recruit)
        progress_form = ProgressForm(instance=recruit)
        interview_form = InterviewReportForm(instance=recruit)
        offer_form = OfferReportForm(instance=recruit)
    
    return render(request, 'recruit/recruit_form.html', {
        'personal_form': personal_form,
        'progress_form': progress_form,
        'interview_form': interview_form,
        'offer_form': offer_form,
        'recruit': recruit,
        'is_edit': True
    })

def recruit_delete(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    if request.method == 'POST':
        recruit.delete()
        messages.success(request, '応募者情報を削除しました。')
        return redirect('recruit_list')
    
    return render(request, 'recruit/recruit_confirm_delete.html', {
        'object': recruit
    })

def recruit_search(request):
    query = request.GET.get('q', '')
    recruits = Recruit.objects.all()
    
    if query:
        recruits = recruits.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name_kana__icontains=query) |
            Q(first_name_kana__icontains=query)
        )
    
    return render(request, 'recruit/index.html', {
        'recruits': recruits.order_by('-entry_day'),
        'query': query
    })
