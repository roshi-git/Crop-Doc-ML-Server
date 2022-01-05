import pyrebase
import requests
import time
import os

class FirebaseServices:

    def __init__(self):

        firebase_config = {
            'apiKey': "AIzaSyBnA-8FAjYvvMk2b7uOvfRN1JzTzRtSA8o",
            'authDomain': "crop-doc.firebaseapp.com",
            'databaseURL': "https://crop-doc-default-rtdb.asia-southeast1.firebasedatabase.app",
            'projectId': "crop-doc",
            'storageBucket': "crop-doc.appspot.com",
            'messagingSenderId': "300370395077",
            'appId': "1:300370395077:web:6f1d49e9e9654b5d7e55ac"
        }

        firebase = pyrebase.initialize_app(firebase_config)
        self.firebase_storage = firebase.storage()


    # DOWNLOAD IMAGE
    def download_image(self, image_URL):

        if not os.path.exists('images'):
            os.makedirs('images')
        
        file_path = 'images/' + 'd' + str(round(time.time() * 1000)) + '.jpg'

        # DOWNLOAD AND SAVE FILE AS JPG
        result = requests.get(image_URL, allow_redirects=True)
        open(file_path, 'wb').write(result.content)

        return file_path


    # UPLOAD PROCESSED IMAGE
    def upload_image(self, processed_image):

        file_name = 'processed_images/' + 'p' + str(round(time.time() * 1000))

        # UPLOAD IMAGE AND GET DOWNLOAD URL
        self.firebase_storage.child(file_name).put(processed_image)
        image_URL = self.firebase_storage.child(file_name).get_url(None)

        return image_URL
