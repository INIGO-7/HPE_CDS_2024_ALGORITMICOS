from fastai.vision.all import *
from fastai.learner import load_learner
import PIL
import os

class ImageClassifier():

    def __init__(self):

        RES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res')
        MODELS_PATH = os.path.join(RES_PATH, "models")
        self.IMGS_PATH = os.path.join(RES_PATH, "img")
        self.RESNET_MODEL_PATH = os.path.join(MODELS_PATH, os.path.join("resnet", "model.pkl"))
        
    def classify_img(self, img_name):
        img = os.path.join(self.IMGS_PATH, img_name)

        learn = load_learner(self.RESNET_MODEL_PATH)
        img = PILImage.create(img)  # Load the image
        img_resized = img.resize((224, 224), Image.BILINEAR)  # Resize the image to match the input size expected by the model

        return learn.predict(img)

    def classify_and_display(self, img_name):

        pred_class, pred_idx, outputs = self.classify_img(img_name)

        # Display the image with the predicted class label
        plt.imshow(img)
        plt.title(f'Predicted Class: {pred_class}')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    img_classifier = ImageClassifier()
    img_classifier.classify_and_display('moraton.jpeg')