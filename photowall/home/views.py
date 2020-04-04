from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, View, UpdateView
from .models import Photos, CreatePartyRoom, id_generator, path_and_rename
from .forms import UploadPhotoForm, CreatePartyRoomForm, RegistrationForm
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from zipfile import *
from wsgiref.util import FileWrapper
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import tempfile, zipfile
web_url = settings.WEB_URL

# Create your views here.

class PhotoWallIndex(TemplateView):
    model = Photos
    form_class = UploadPhotoForm
    template_name = "photowall.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        room_code = self.kwargs.get("photo_room")
        

        partyroom = CreatePartyRoom.objects.get(room_code=room_code)
        ctx['query'] = room_code
        ctx['partyroom'] = partyroom
    
        ctx['asdf'] = Photos.objects.filter(partyroom_id=partyroom.pk).order_by('-created_at')
        return ctx


class Photowallslideshow(TemplateView):
    model = Photos
    form_class = UploadPhotoForm
    template_name = "photowallslideshow.html"

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        room_code = self.kwargs.get("photo_room")
        

        partyroom = CreatePartyRoom.objects.get(room_code=room_code)
        ctx['query'] = room_code
        ctx['partyroom'] = partyroom
    
        ctx['asdf'] = Photos.objects.filter(partyroom_id=partyroom.pk).order_by('-created_at')
        return ctx

class UploadPhoto(CreateView):
    model = Photos
    form_class = UploadPhotoForm
    template_name = 'index_upload.html'


    def form_valid(self, form):
        files = self.request.FILES.getlist('photo_room_image')
        print(files)
        if files:

            room_code = self.request.GET.get("photo_room")

            peder = CreatePartyRoom.objects.get(room_code=room_code)
            peder.total_pictures = peder.total_pictures + 1
            peder.save()
            form.instance.partyroom_id = peder.pk
            form = form.save(commit=False)
            form.save()
            return super().form_valid(form)
        else:
            form = UploadPhotoForm()

    def get_success_url(self):
        room_code = self.request.GET.get("photo_room")
        return reverse('home:photo_wall', kwargs={'photo_room': room_code})

class PhotoWall(TemplateView):
    model = Photos
    form_class = UploadPhotoForm
    template_name = 'index.html'

class CreatePhotoRoom(CreateView):
    model = CreatePartyRoom
    form_class = CreatePartyRoomForm
    template_name = 'create_photo_room.html'

    def form_valid(self, form):
        pk = self.request.user.id
        form.instance.user_id = pk
        form.instance.total_pictures = 0
        form = form.save(commit=False)
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home:dashboard')

class SearchPhotoRoom(ListView):
    model = CreatePartyRoom
    context_object_name = "object_list"
    template_name = 'photowall.html'
    paginate_by = 10

    def get_queryset(self):  # new
        query = self.request.GET.get('q')
        try:
            queryset = CreatePartyRoom.objects.filter(
                Q(room_code__exact=query))
        except CreatePartyRoom.DoesNotExists:
            pass
        return queryset

    def render_to_response(self, context,):
        if len(self.object_list) == 0:
            messages.warning(self.request, "Ok Boomer! did not find the party..")
            return redirect('home:indexpage')
        return super().render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        try:
            q = self.request.GET.get('q')
            partyroom = CreatePartyRoom.objects.get(room_code=q)
            ctx['query'] = q
            ctx['partyroom'] = partyroom
            ctx['asdf'] = Photos.objects.filter(partyroom_id=partyroom.pk)
        except:
            pass
        return ctx

        

class Dashboard(TemplateView):
    model = CreatePartyRoom
    template_name = 'dashboard/index.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(
            *args, **kwargs)
        pk = self.request.user.id
        room_codes = CreatePartyRoom.objects.filter(user_id=pk).order_by('-create_at').values_list('room_code', flat=True)
        i = 0
        qr_code = ""
        qr_dict = dict()
        for codes in room_codes:
            qr_code = ("{value}/userpage/indexpage/search/rest_details/").format(value=web_url) + room_codes[i]
            qr_dict = {room_codes[i]:qr_code}
            print(qr_dict.values())
            print(qr_dict.keys())
            i = i + 1
        ctx['qr'] = qr_dict
        ctx['get_party_rooms'] = CreatePartyRoom.objects.filter(user_id=pk).order_by('-create_at')
        return ctx

def register(response):
    if response.method == 'POST':
        form = RegistrationForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = RegistrationForm()
    return render(response, 'register/register.html', {'form': form})



def download_image(request, id):
        """                                                                         
        Create a ZIP file on disk and transmit it in chunks of 8KB,                 
        without loading the whole file into memory. A similar approach can          
        be used for large dynamic PDF files.                                        
        """
        product_image = Photos.objects.filter(partyroom_id=id).values_list('photo_room_image', flat=True)
        print(product_image[0])
        temp = tempfile.TemporaryFile()
        archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        i = 0
        for index in product_image:
            filename = settings.MEDIA_ROOT + "/" +index # Replace by your files here.  
            archive.write(filename, 'file{name}'.format(name=index)) # 'file%d.png' will be the
        archive.close()
        temp.seek(0)
        wrapper = FileWrapper(temp)
        response = HttpResponse(wrapper, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=photos.zip'
        return response