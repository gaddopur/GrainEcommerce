from django.contrib.auth import login, logout
from django.shortcuts import render
from . import forms
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.http import HttpResponse
from django.core.mail import EmailMessage

# Create your views here.
def signup_views(request):
    templates = 'accounts/signup.html'
    if request.method == "POST":
        user_form = forms.RegisterForm(request.POST)
        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.active = False
            user.save()

            current_site = get_current_site(request)

            mail_subject = 'Activate your AmanCo account.'
            message = render_to_string('accounts/activate_email.html', {
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        user_form = forms.RegisterForm()
    context = {'user_form': user_form}
    return render(request, templates, context)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
