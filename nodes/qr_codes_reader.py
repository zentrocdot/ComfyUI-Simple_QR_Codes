#!/usr/bin/python
'''Simple qr code node.'''
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=no-member
##pylint:#disable=too-many-locals
##pylint:#disable=import-error
##pylint:#disable=line-too-long
##pylint:#disable=too-many-arguments
##pylint:#disable=too-many-positional-arguments
##pylint:#disable=consider-using-from-import
#
# https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/
# https://realpython.com/python-generate-qr-code/
# https://pypi.org/project/qrcode/

# Import the Python modules.
#import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
import torch

# -----------------------
# Tensor to PIL function.
# -----------------------
def tensor2pil(image):
    '''Tensor to PIL image.'''
    # Return PIL image.
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# -------------------------------
# Convert PIL to Tensor function.
# -------------------------------
def pil2tensor(image):
    '''PIL image to tensor.'''
    # Return tensor.
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

# -----------------------
# Function string2tuple()
# -----------------------
def string2tuple(color_string):
    '''String to tuple function.'''
    # Initialise the color tuple.
    color_tuple = (64,64,64)
    # Try to create a color tuple.
    try:
        stripString = str(color_string).replace('(','').replace(')','').strip()
        rgb = stripString.split(",")
        r, g, b = int(rgb[0].strip()), int(rgb[1].strip()), int(rgb[2].strip())
        color_tuple = (r, g, b)
    except:
        print("ERROR. Could not create color tuple!")
        color_tuple = (128,128,128)
    # Return the color tuple
    return color_tuple

# ******************
# Class QRCodeReader
# ******************
class QRCodeReader:
    '''Create a QR code image.'''

    #def __init__(self):
    #    self.channels = ["red", "green", "blue"]
    #    self.basewidth = 100

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("TEXT",)
    FUNCTION = "qr_code_reader"
    CATEGORY = "🍭 QR Code Nodes"
    OUTPUT_NODE = True

    def read_qr_code(self, image):
        '''Read the QR Code image.'''
        # Create a numpy array.
        image = np.array(image)
        # Create the QR code detector.
        qcd = cv2.QRCodeDetector()
        # Read the QR code.
        retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(image)
        print("retval:", retval, decoded_info, points, straight_qrcode)
        # Return the QR code text.
        return decoded_info

    def qr_code_reader(self, image):
        '''Main node function. Read the QR code image.'''
        # Tensor to PIL image.
        image = tensor2pil(image)
        # Read the QR code image.
        text = self.read_qr_code(image)
        # Return the return types.
        return (text,)
