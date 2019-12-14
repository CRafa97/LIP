from django.shortcuts import render
from django.http import HttpResponseRedirect
from lipApp.models import AppImage
from lipApp.forms import UploadFileForm
from lipsite.settings import BASE_DIR
from skimage.io import imsave
from lip import LIPImage
from lip.image_api import *
from re import match

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
def contrast_ops(request, op):
    global current_image
    context = { }

    image_path = None
    try:
        image_name = current_image.paths[op]
    except:
        dic = globals()
        image_name = dic[op](current_image.img, current_image.sfolder)

    context['Image'] = current_image.folder + image_name
    return render(request, '../templates/im_show.html', context)

def select(request, fldname):
    if fldname in folders():
       global current_image
       current_image = AppImage(fldname + '.jpg', 'imgs/' + fldname + '/')
       return HttpResponseRedirect('/load/')
    return HttpResponseRedirect('/')

def upload(request):
    global current_image
    query = ""
    context = {}
    context['error'] = ''
    flds = folders()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fd = form.cleaned_data['uploaded_file']
            name = form.cleaned_data['uploaded_file']._name
            size = form.cleaned_data['uploaded_file'].size

            def copy():
                import os
                global current_image
                pth = ''.join([BASE_DIR, '/static/imgs/'])
                sfolder = pth + name.split('.')[0] + '/'
                folder =  'imgs/' + name.split('.')[0] + '/'

                try:
                    os.mkdir(pth)
                except:
                    pass

                try:
                    os.mkdir(sfolder)
                except:
                    current_image = AppImage(name, folder)
                    return HttpResponseRedirect('/')

                wf = open(sfolder + name, 'wb')
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
        # get all images
        flds = [f for f in folders() if match(query.lower(), f.lower())]

    form = UploadFileForm()
    context['form'] = form
    context['query'] = query
    context['Folders'] = flds
    return render(request, '../templates/upload.html', context)

def folders():
    import os
    l = os.listdir('static/imgs/')
    return l
