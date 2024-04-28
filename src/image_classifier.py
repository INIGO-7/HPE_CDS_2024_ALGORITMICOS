from fastai.vision.all import *
from fastai.learner import load_learner
import PIL
import os

class ImageClassifier():

    """
    A classifier for images using a pretrained ResNet model from the fastai library.

    Attributes:
        IMGS_PATH (str): Path where images are stored.
        RESNET_MODEL_PATH (str): Path to the pretrained ResNet model.
    """

    def __init__(self):

        """
        Initializes the ImageClassifier by setting up the path to the image resources and model.
        """

        RES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'res')
        MODELS_PATH = os.path.join(RES_PATH, "models")
        self.IMGS_PATH = os.path.join(RES_PATH, "img")
        self.RESNET_MODEL_PATH = os.path.join(MODELS_PATH, os.path.join("resnet", "model.pkl"))
        
    def classify_img(self, img_name):

        """
        Classifies an image by name using the pretrained ResNet model.

        Args:
            img_name (str): The filename of the image to classify.

        Returns:
            tuple: A tuple containing the predicted class, the index of the predicted class, 
            and the output tensor of class probabilities.
        """

        img = os.path.join(self.IMGS_PATH, img_name)

        learn = load_learner(self.RESNET_MODEL_PATH)
        img = PILImage.create(img)  # Load the image
        img_resized = img.resize((224, 224), Image.BILINEAR)  # Resize the image to match the input size expected by the model

        return learn.predict(img)

    def classify_and_display(self, img_name):

        """
        Classifies an image and displays it with the predicted class label.

        Args:
            img_name (str): The filename of the image to classify and display.
        """

        pred_class, pred_idx, outputs = self.classify_img(img_name)

        # Display the image with the predicted class label
        plt.imshow(img)
        plt.title(f'Predicted Class: {pred_class}')
        plt.axis('off')
        plt.show()

if __name__ == '__main__':
    img_classifier = ImageClassifier()
    img_classifier.classify_and_display('moraton.jpeg')