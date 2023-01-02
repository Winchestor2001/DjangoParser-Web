from django.shortcuts import render, redirect
from .utils import _24freelance_parserThread, CheckWorksThread, freelancermap_parserThread, freelancer_parserThread, flexjobs_parserThread, fl_parserThread
from .models import Work
from django.core.paginator import Paginator
from django.core.mail import send_mail
from config import settings


def send_to_email(domain, email):
    html = f"<a href='http://{domain}/get_info/65'>LINK</a>"
    send_mail(f'link', 'Message link', settings.EMAIL_HOST_USER, [email,],
                html_message=html,
                fail_silently=True)


def home(request):
    context = {}
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            send_to_email(request.get_host(), email)
        else:
            radio = int(request.POST['rad'])
            return redirect('get_info', radio)
    
    _24freelance_parserThread().start()
    freelancermap_parserThread().start()
    freelancer_parserThread().start()
    flexjobs_parserThread().start()
    fl_parserThread().start()
    # CheckWorksThread().start()
    return render(request, 'index.html', context)


def get_info(request, radio):
    context = {}
    lang = request.LANGUAGE_CODE
    # print(lang)
    works = Work.objects.filter(work_lang=lang)
    if works:
        if radio == 100:
            context['works'] = works
            p = Paginator(works, 10)
            page = request.GET.get('page')
            nums = 'a' * p.get_page(page).paginator.num_pages
            context['paginations'] = p.get_page(page)
            context['nums'] = nums
        else:
            num = (radio * len(works)) // 100
            context['works'] = works[:num]
            p = Paginator(works[:num], 10)
            page = request.GET.get('page')
            nums = 'a' * p.get_page(page).paginator.num_pages
            context['paginations'] = p.get_page(page)
            context['nums'] = nums
    return render(request, 'infos.html', context)
