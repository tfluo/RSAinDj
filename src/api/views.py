# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.


from django.http import HttpResponseNotFound, HttpResponse
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from django.conf import settings
import base64
from django.views.decorators.csrf import csrf_exempt

def crypto(request):
    values = {}
    values['public_key'] = settings.RSA_PUBLIC_KEY
    if request.method == 'GET':
        return render(request, 'crypto.html', values)

    elif request.method == 'POST':
        password_new = request.POST.get('id_password')
        with open('password.txt', 'w') as f:
            f.write(password_new)
        return HttpResponse('OK.')
    else:
        return HttpResponseNotFound('')

def get_pass(request):
    random_gen = Random.new().read
    RSA.generate(1024, random_gen)
    rsakey = RSA.importKey(settings.RSA_PRIVATE_KEY)
    cipher = PKCS1_v1_5.new(rsakey)
    with open('password.txt') as f:
      password_encrypt = f.readline()
    password = cipher.decrypt(base64.b64decode(password_encrypt), random_gen)
    return HttpResponse('password is %s.' % password)
