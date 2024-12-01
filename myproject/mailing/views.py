from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import MailingForm, MessageForm
from .models import MailingStat, Recipient, Message, Mailing

def recipient_list(request):
    recipients = Recipient.objects.all()
    return render(request, 'mailing/recipient_list.html', {'recipients': recipients})

def recipient_detail(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)
    return render(request, 'mailing/recipient_detail.html', {'recipient': recipient})


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'mailing_service/message_list.html', {'messages': messages})

def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'mailing_service/message_detail.html', {'message': message})

def message_create(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'mailing_service/message_form.html', {'form': form})

def message_edit(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_detail', pk=pk)
    else:
        form = MessageForm(instance=message)
    return render(request, 'mailing_service/message_form.html', {'form': form})

def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'mailing_service/message_confirm_delete.html', {'message': message})


def mailing_list(request):
    mailings = Mailing.objects.all()
    return render(request, 'mailing_service/mailing_list.html', {'mailings': mailings})

def mailing_detail(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    return render(request, 'mailing_service/mailing_detail.html', {'mailing': mailing})

def mailing_create(request):
    if request.method == 'POST':
        form = MailingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mailing_list')
    else:
        form = MailingForm()
    return render(request, 'mailing_service/mailing_form.html', {'form': form})

def mailing_edit(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect('mailing_detail', pk=pk)
    else:
        form = MailingForm(instance=mailing)
    return render(request, 'mailing_service/mailing_form.html', {'form': form})

def mailing_delete(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == 'POST':
        mailing.delete()
        return redirect('mailing_list')
    return render(request, 'mailing_service/mailing_confirm_delete.html', {'mailing': mailing})


def user_statistics(request):
    stats = MailingStat.objects.get(user=request.user)
    return render(request, 'stats/user_stats.html', {'stats': stats})


@login_required
def manage_mailings(request):
    if request.user.groups.filter(name='Manager').exists():
        mailings = Mailing.objects.all() 
    else:
        mailings = Mailing.objects.filter(user=request.user) 
    
    return render(request, 'mailings/mailing_list.html', {'mailings': mailings})