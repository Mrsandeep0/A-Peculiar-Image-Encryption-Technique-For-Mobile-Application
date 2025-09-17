# Create your views here.
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from .forms import UserRegistrationForm
from .models import UserRegistrationModel, EncryptionImageModels
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import numpy as np

import string
import random
import os


# Create your views here.
def UserRegisterActions(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            form = UserRegistrationForm()
            return render(request, 'UserRegistrations.html', {'form': form})
        else:
            messages.success(request, 'Email or Mobile Already Existed')
            print("Invalid form")
    else:
        form = UserRegistrationForm()
    return render(request, 'UserRegistrations.html', {'form': form})


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})


def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def UserShareImages(request):
    if request.method == 'POST':
        image_file = request.FILES['file']
        fromUser = request.session['loggeduser']
        toUser = request.POST.get('usr')
        msg = request.POST.get('msg')
        # let's check if it is a csv file
        # if not image_file.name.endswith('.png'):
        #     messages.error(request, 'THIS IS NOT A PNG  FILE')
        fs = FileSystemStorage(location="media/originals/")
        filename = fs.save(image_file.name, image_file)
        outputName = filename.split(".")[0] + ".png"
        # detect_filename = fs.save(image_file.name, image_file)
        input_image = "/media/originals/" + filename  # fs.url(filename)
        output_image = "/media/output/" + outputName
        path1 = os.path.join(settings.MEDIA_ROOT, 'originals', filename)
        path2 = os.path.join(settings.MEDIA_ROOT, 'output', outputName)
        print("Image path ", input_image)
        print("Output Image ", output_image)
        # path1 = os.path.join()
        secretKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print("secret Key:", secretKey)
        from cryptosteganography import CryptoSteganography
        crypto_steganography = CryptoSteganography(secretKey)
        crypto_steganography.hide(path1, path2, msg)
        EncryptionImageModels.objects.create(fromName=fromUser, toName=toUser, secretKey=secretKey, path1=filename,
                                             path2=outputName)

        return render(request, "users/ShareImages_success.html", {'path1': input_image, 'path2': output_image})
    else:
        from django.db.models import Q
        loginid = request.session['loginid']
        users = UserRegistrationModel.objects.filter(~Q(loginid=loginid), ~Q(status='waiting'))
        # users = UserRegistrationModel.objects.exclude(loginid=loginid, status='active')
        return render(request, "users/ShareImages.html", {'users': users})


def UserViewImages(request):
    loginid = request.session['loginid']
    data = EncryptionImageModels.objects.filter(toName=loginid)
    return render(request, "users/ViewImages.html", {'data': data})


def getMessageFromImage(request):
    id = request.GET.get('uid')
    data = EncryptionImageModels.objects.get(id=id)
    outputImage = data.path2
    path2 = os.path.join(settings.MEDIA_ROOT,'output', outputImage)
    from cryptosteganography import CryptoSteganography
    secretKey = data.secretKey
    crypto_steganography = CryptoSteganography(secretKey)
    secret = crypto_steganography.retrieve(path2)
    loginid = request.session['loginid']
    data = EncryptionImageModels.objects.filter(toName=loginid)
    return render(request, "users/ViewImages.html", {'data': data,'msg': secret})

