from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from PIL import Image, ImageOps

from uuslug import uuslug
from uuid import uuid4
import os, piexif
import string
import random

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
        return "".join(random.choice(chars) for x in range(size))

def path_and_rename(instance, filename):
    room_code = instance.partyroom.room_code
    upload_to = 'images/{room_code}'.format(room_code=room_code)
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)
# Create your models here.

class CreatePartyRoom(models.Model):
    name = models.CharField(max_length=60)
    create_at = models.DateTimeField(auto_now_add=True)
    date = models.CharField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_pictures = models.IntegerField()
    room_code = models.CharField(max_length=60, default = id_generator)




class Photos(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    partyroom = models.ForeignKey(CreatePartyRoom, on_delete=models.CASCADE)
    photo_room_image = models.ImageField(upload_to=path_and_rename, validators=[FileExtensionValidator(allowed_extensions=['png','jpeg','jpg'])])


    def __str__(self):
        return self.id + self.partyroom

    def save(self, *args, **kwargs):
        super(Photos, self).save(*args, **kwargs)
        print("partyroom",self.partyroom.room_code)
        #img = Image.open(self.photo_room_image.path)
        img = Image.open(self.photo_room_image.path)
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])

            if piexif.ImageIFD.Orientation in exif_dict["0th"]:
                orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
                exif_bytes = piexif.dump(exif_dict)

                if orientation == 2:
                    img = img.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    img = img.rotate(180)
                elif orientation == 4:
                    img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 5:
                    img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 6:
                    img = img.rotate(-90, expand=True)
                elif orientation == 7:
                    img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 8:
                    img = img.rotate(90, expand=True)

                img.save(self.photo_room_image.path, exif=exif_bytes)
        if img.height > 860 or img.width > 1024:
            output_size = (860,1024)
            img.thumbnail(output_size)
            img.save(self.photo_room_image.path)