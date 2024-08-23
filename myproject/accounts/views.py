import random
import string


from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from .forms import PasswordResetForm, RegistrationForm
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import make_password


User = get_user_model()


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False 
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Подтверждение регистрации'
        message = render_to_string('registration/activation_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        send_mail(subject, message, 'admin@example.com', [user.email])

        return redirect('registration_success')
    

    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('activation_success')
        else:
            return render(request, 'activation_invalid.html')
        

class CustomLoginView(LoginView):
    template_name = 'login.html'


class PasswordResetView(FormView):
    template_name = 'password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = make_password(new_password)
            user.save()

            send_mail(
                'Ваш новый пароль',
                f'Ваш новый пароль: {new_password}',
                'admin@example.com',
                [user.email],
            )

        return redirect('password_reset_done')