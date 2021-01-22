import random
import hashlib
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.http import HttpResponse
from weasyprint import HTML
from .models import ApplicationForm, FilledApplicationForm
from .forms import GeneralForm, ConfirmationForm


class BaseView(View):

    def get(self, request, *args, **kwargs):
        forms = ApplicationForm.objects.all()
        context = {
            'forms': forms,
        }
        return render(request, 'main/base.html', context)


class FormsView(View):

    def get(self, request, *args, **kwargs):
        stage = kwargs.get('stage')
        slug = kwargs.get('slug')
        form = GeneralForm(slug=slug)
        form_obj = ApplicationForm.objects.get(slug=slug)
        if stage == 'start':
            context = {
                'form': form,
                'form_obj': form_obj,
            }
            return render(request, 'main/forms.html', context)
        elif stage == 'confirmation':
            context = {
                'form': ConfirmationForm(),
                'form_obj': form_obj,
            }
            return render(request, 'main/confirmation.html', context)
        elif stage == 'document':
            if request.session.get('confirmed'):
                form_obj = ApplicationForm.objects.get(slug=slug)
                code = request.session.get('code')
                string = (str(code) + form_obj.document.text).encode('utf-8')
                string_hash = hashlib.sha1(string)
                request.session['signature'] = string_hash.hexdigest()
                main_form = request.session.get('main_form')

                kw_arguments = {
                    'signature': request.session.get('signature'),
                }
                for key, value in main_form.items():
                    kw_arguments[key] = value
                document = form_obj.document.text.format(**kw_arguments)
                request.session['document'] = document
                context = {
                    'form_obj': form_obj,
                    'document': document,
                }
                return render(request, 'main/document.html', context)
            else:
                messages.add_message(request, messages.WARNING, 'Введен неправильный код')
                return HttpResponseRedirect(f'/forms/{slug}/confirmation')
        elif stage == 'end':
            values = dict()
            main_form = request.session.get('main_form')
            for field in form_obj.form.fields.all():
                values[field.slug] = main_form.get(field.slug)
            new_filled = FilledApplicationForm.objects.create(
                application_form=form_obj,
                email=main_form.get('email'),
                code=request.session.get('code'),
                signification=request.session.get('signature'),
                values=values,
            )
            kw_arguments = {
                'key': request.session.get('code'),
                'signature': request.session.get('signature'),
            }
            for key, value in main_form.items():
                kw_arguments[key] = value
            end_page = form_obj.end_page.html_text.format(**kw_arguments)
            context = {
                'form_obj': form_obj,
                'email': main_form.get('email'),
                'end_page': end_page,
            }
            return render(request, 'main/end_page.html', context)
        elif stage == 'download_pdf':
            html_string = request.session['document']
            file_name = form_obj.document.file_name.replace(' ', '_')
            html = HTML(string=html_string)
            html.write_pdf(target=f'tmp/{file_name}.pdf')
            with open(f'tmp/{file_name}.pdf', 'rb') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
                return response
        elif stage == 'confirm_url':
            request.session['confirmed'] = True
            return HttpResponseRedirect(f'/forms/{slug}/document')

    def post(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        stage = kwargs.get('stage')
        if stage == 'send_form':
            main_form = GeneralForm(request.POST or None, slug=slug)
            if main_form.is_valid():
                request.session['main_form'] = main_form.cleaned_data
                form_obj = ApplicationForm.objects.get(slug=slug)
                code = random.randint(1000, 9999)
                request.session['code'] = code
                text = form_obj.message.text
                confirm_url = (settings.SITE_URI + 'forms/{slug}/confirm_url').format(slug=slug)
                if 'link' in text:
                    html_text = text.format(key=code, link=confirm_url)
                else:
                    html_text = text.format(key=code)
                print(html_text)
                print(type(html_text))
                msg = EmailMessage(form_obj.message.topic, html_text, to=[main_form.cleaned_data['email']])
                msg.content_subtype = "html"
                msg.send(fail_silently=False)
                return HttpResponseRedirect(f'/forms/{slug}/confirmation')
            return HttpResponseRedirect(f'forms/{slug}/start')
        elif stage == 'send_code':
            slug = kwargs.get('slug')
            stage = kwargs.get('stage')
            if stage == 'send_code':
                code_form = ConfirmationForm(request.POST or None)
                if code_form.is_valid():
                    code = code_form.cleaned_data['code']
                    if code.isdigit():
                        if request.session.get('code') == int(code):
                            request.session['confirmed'] = True
                            return HttpResponseRedirect(f'/forms/{slug}/document')
                        else:
                            messages.add_message(request, messages.WARNING, 'Введен неправильный код')
                            return HttpResponseRedirect(f'/forms/{slug}/confirmation')
                    messages.add_message(request, messages.WARNING, 'Введите код')
                    return HttpResponseRedirect(f'/forms/{slug}/confirmation')
                return HttpResponseRedirect(f'/forms/{slug}/confirmation')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/')






