from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .models import Invitation

def invite_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        token = uuid.uuid4()
        invitation = Invitation.objects.create(email=email, token=token)
        invitation.save()

        invite_link = request.build_absolute_uri(reverse('accept_invitation', args=[token]))
        send_mail(
            'You are invited to join our site',
            f'Please accept your invitation by clicking the following link: {invite_link}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return redirect('invitation_sent')
    return render(request, 'invite_user.html')

def accept_invitation(request, token):
    try:
        invitation = Invitation.objects.get(token=token)
    except Invitation.DoesNotExist:
        return render(request, 'invitation_invalid.html')

    if invitation.accepted:
        return render(request, 'invitation_already_accepted.html')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            invitation.accepted = True
            invitation.save()

            login(request, user)
            return redirect('home')

    form = UserCreationForm()
    return render(request, 'accept_invitation.html', {'form': form})

