from django.shortcuts import render
from django.http import HttpResponseRedirect
from lipApp.models import AppImage
from lipApp.forms import UploadFileForm
from lipsite.settings import BASE_DIR
from skimage.io import imsave
from lip import LIPImage
from lip.image_api import *

current_image = None

def with_image(function):
    global current_image
    def wrapper(*args, **kwargs):
        if current_image == None:
            return HttpResponseRedirect('/')
        return function(*args, **kwargs)
    return wrapper
    
def index(request):
    return render(request, '../templates/home.html')

@with_image
def vlac(request, op):
    global current_image
    context = { }

    image_path = None
    try:
        image_path = current_image.paths[op]
    except:
        dic = globals()
        image_path = dic[op](current_image.img, current_image.folder)

    context['Image'] = image_path
    return render(request, '../templates/lac.html', context)

@with_image
def vlmc(request, op):
    global current_image
    context = { }

    image_path = None
    try:
        image_path = current_image.paths[op]
    except:
        dic = globals()
        image_path = dic[op](current_image.img, current_image.folder)

    context['Image'] = image_path
    return render(request, '../templates/lmc.html', context)

def upload(request):
    global current_image
    query = ""
    context = {}
    context['error'] = ''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fd = form.cleaned_data['uploaded_file']
            name = form.cleaned_data['uploaded_file']._name
            size = form.cleaned_data['uploaded_file'].size

            def copy():
                import os
                global current_image
                pth = ''.join([BASE_DIR, '/imgs/'])
                folder = pth + name.split('.')[0] + '/'
                try:
                    os.mkdir(pth)
                except:
                    pass

                try:
                    os.mkdir(folder)
                except:
                    current_image = AppImage(name, folder)
                    return HttpResponseRedirect('/')

                wf = open(folder + name, 'wb')
                while 1:
                    data = fd.read(50*1024*1024)
                    if len(data) == 0:
                        break
                    wf.write(data)
                wf.close()

                current_image = AppImage(name, folder)
                return HttpResponseRedirect('/')
            copy()
    else:
        query = request.GET.get('search_box', "")

    form = UploadFileForm()
    context['form'] = form
    context['query'] = query
    return render(request, '../templates/upload.html', context)