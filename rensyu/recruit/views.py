from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Recruit
from .forms import PersonalInfoForm, ProgressForm, InterviewReportForm, OfferReportForm

def get_form_by_type(form_type, data=None, instance=None):
    """フォームタイプに応じたフォームを返す"""
    form_classes = {
        'personal': PersonalInfoForm,
        'progress': ProgressForm,
        'interview': InterviewReportForm,
        'offer': OfferReportForm
    }
    form_class = form_classes.get(form_type, PersonalInfoForm)
    return form_class(data=data, instance=instance)

def recruit_list(request):
    recruits = Recruit.objects.all().order_by('-entry_day')
    return render(request, 'recruit/index.html', {'recruits': recruits})

def recruit_create(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'personal')
        form = get_form_by_type(form_type, data=request.POST)
        
        if form.is_valid():
            recruit = form.save(commit=False)
            if not recruit.entry_day:
                recruit.entry_day = timezone.now().date()
            recruit.save()
            messages.success(request, '応募者情報を登録しました。')
            return redirect('recruit_list')
        messages.error(request, '入力内容に誤りがあります。')
    else:
        form = PersonalInfoForm()
        form_type = 'personal'
    
    return render(request, 'recruit/recruit_form.html', {
        'form': form,
        'form_type': form_type,
        'is_edit': False
    })

def recruit_edit(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    form_type = request.GET.get('form_type', 'personal')
    
    if request.method == 'POST':
        form = get_form_by_type(form_type, data=request.POST, instance=recruit)
        if form.is_valid():
            form.save()
            messages.success(request, '応募者情報を更新しました。')
            return redirect('recruit_list')
        messages.error(request, '入力内容に誤りがあります。')
    else:
        form = get_form_by_type(form_type, instance=recruit)
    
    return render(request, 'recruit/recruit_form.html', {
        'form': form,
        'recruit': recruit,
        'is_edit': True,
        'form_type': form_type
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
