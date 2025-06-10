from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Recruit
from .forms import PersonalInfoForm, ProgressForm, InterviewReportForm, OfferReportForm

def recruit_list(request):
    recruits = Recruit.objects.all().order_by('-entry_day')
    return render(request, 'recruit/index.html', {'recruits': recruits})

def recruit_create(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST)
        if form.is_valid():
            recruit = form.save()
            messages.success(request, '応募者情報が正常に登録されました。')
            return redirect('recruit_list')
    else:
        form = PersonalInfoForm()
    return render(request, 'recruit/recruit_form.html', {'form': form, 'is_edit': False})

def recruit_edit(request, pk):
    recruit = get_object_or_404(Recruit, pk=pk)
    form_type = request.GET.get('form_type', 'personal')
    
    if request.method == 'POST':
        if form_type == 'personal':
            form = PersonalInfoForm(request.POST, instance=recruit)
        elif form_type == 'progress':
            form = ProgressForm(request.POST, instance=recruit)
        elif form_type == 'interview':
            form = InterviewReportForm(request.POST, instance=recruit)
        elif form_type == 'offer':
            form = OfferReportForm(request.POST, instance=recruit)
        else:
            form = PersonalInfoForm(request.POST, instance=recruit)
            
        if form.is_valid():
            form.save()
            messages.success(request, '応募者情報が正常に更新されました。')
            return redirect('recruit_list')
    else:
        if form_type == 'personal':
            form = PersonalInfoForm(instance=recruit)
        elif form_type == 'progress':
            form = ProgressForm(instance=recruit)
        elif form_type == 'interview':
            form = InterviewReportForm(instance=recruit)
        elif form_type == 'offer':
            form = OfferReportForm(instance=recruit)
        else:
            form = PersonalInfoForm(instance=recruit)
            
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
    if query:
        recruits = Recruit.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name_kana__icontains=query) |
            Q(first_name_kana__icontains=query)
        ).order_by('-entry_day')
    else:
        recruits = Recruit.objects.all().order_by('-entry_day')
    return render(request, 'recruit/index.html', {'recruits': recruits, 'query': query})
