#!/usr/bin/env python3
import os
import shutil
import subprocess
from datetime import datetime
from PIL import Image

class PhotoOrganizer:
    extensions = ['.jpg', '.jpeg', '.heic', '.nef', '.mov', '.mp4', '.JPG', '.JPEG', '.HEIC', '.NEF', '.MOV', '.MP4']

    def folder_path_from_photo_date(self, file):
        date = self.photo_shooting_date(file)
        return date.strftime('%Y') + '/' + date.strftime('%Y-%m-%d')
    
    def get_photo_date_taken(self,file):
        return datetime.fromtimestamp(os.path.getmtime(file))
                
    def photo_shooting_date(self, file):

        if file.endswith('.HEIC') or file.endswith('.heic') or file.endswith('.nef') or file.endswith('.NEF') or file.endswith('.mov') or file.endswith('.MOV') or file.endswith('.mp4') or file.endswith('.MP4'):
            return self.get_photo_date_taken(file)

        photo = Image.open(file)
        info = photo._getexif()
        date = datetime.fromtimestamp(os.path.getmtime(file))
        if info:
            if 36867 in info:
                date = info[36867]
                date = datetime.strptime(date, '%Y:%m:%d %H:%M:%S')
        return date

    def move_photo(self, file):
        new_folder = self.folder_path_from_photo_date(file)
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        shutil.move(file, new_folder + '/' + file)

    def organize(self):
        photos = [
            filename for filename in os.listdir('.') if any(filename.endswith(ext) for ext in self.extensions)
        ]
        for filename in photos:
            self.move_photo(filename)


PO = PhotoOrganizer()
PO.organize()