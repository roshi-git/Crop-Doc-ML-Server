from firebase_services import FirebaseServices
import os

class DiseasePredictor:

    def __init__(self, image_URL):
        self.image_URL = image_URL

    def predict_disease(self):

        if not os.path.exists('images'):
            os.makedirs('images')
        os.chdir('images')

        firebase = FirebaseServices()

        # DOWNLOAD IMAGE FROM FIREBASE STORAGE
        file_name = firebase.download_image(self.image_URL)

        # PREDICT DISEASE
        prediction = "Yellow Leaf Curl"

        # PLOT DISEASE
        plotted_image = 'eye.png'

        # UPLOAD IMAGE TO FIREBASE STORAGE
        image_URL = firebase.upload_image(plotted_image)

        # RETURN IMAGE LINK AND PREDICTED RESULT
        return {
            "status":"SUCCESS",
            "prediction": prediction,
            "image_URL": image_URL
            }