from firebase_services import FirebaseServices
import os

class DiseasePredictor:

    def __init__(self, image_URL):
        self.image_URL = image_URL

    def predict_disease(self, model):

        firebase = FirebaseServices()

        # DOWNLOAD IMAGE FROM FIREBASE STORAGE
        file_path = firebase.download_image(self.image_URL)

        # PREDICT DISEASE
        prediction = model.classify(file_path)
        os.remove(file_path)

        # UPLOAD PLOTTED IMAGE TO FIREBASE STORAGE
        # plotted_image = plot_image(file_name)
        # image_URL = firebase.upload_image(plotted_image)
        image_URL = self.image_URL

        # RETURN IMAGE LINK AND PREDICTED RESULT
        return {
            "status":"SUCCESS",
            "prediction": prediction,
            "image_URL": image_URL
        }