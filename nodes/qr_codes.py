#!/usr/bin/python
'''Simple qr code node.'''
# pylint: disable=too-many-locals
# pylint: disable=invalid-name
# pylint: disable=import-error
# pylint: disable=line-too-long
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=bare-except
# pylint: disable=consider-using-from-import
#
# https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/
# https://realpython.com/python-generate-qr-code/
# https://pypi.org/project/qrcode/

# Import the Python modules.
from PIL import Image, ImageDraw
import numpy as np
import torch
import qrcode
import torchvision.transforms as transforms

# Set the error correction.
ERROR_CORRECT = {"ERROR_CORRECT_L": qrcode.constants.ERROR_CORRECT_L,
                 "ERROR_CORRECT_M": qrcode.constants.ERROR_CORRECT_M,
                 "ERROR_CORRECT_Q": qrcode.constants.ERROR_CORRECT_Q,
                 "ERROR_CORRECT_H": qrcode.constants.ERROR_CORRECT_H}

# Get key word list.
ERR_CORR = list(ERROR_CORRECT.keys())

# Create version list.
VERSION = list(range(1, 41))

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

# *****************
# Class QRCodesLogo
# *****************
class QRCodesLogo:
    '''Create a QR code image.'''

    def __init__(self):
        self.channels = ["red", "green", "blue"]
        self.basewidth = 100

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "bg_color": ("STRING", {"multiline": False, "default": "(0, 0, 0)"}),
                "fg_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "error_correct": (ERR_CORR, {}),
                "version": (VERSION, {}),
                "box_size": ("INT", {"default": 10, "min": 0, "max": 8192}),
                "border": ("INT", {"default": 4, "min": 0, "max": 8192}),
                "color": (["red", "green", "blue"], {}),
            },
            "optional": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("IMAGE", "MASK", "INVERTED_MASK",)
    FUNCTION = "qr_code_creation"
    CATEGORY = "🍭 QR Code Nodes"
    OUTPUT_NODE = True

    def create_qr_code(self, text, bg_color, fg_color, error_correct,
                       version, box_size, border, image):
        '''Create the QR Code image.'''
        # Create the color tuples.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        # Set the logo image.
        logo = image
        # Adjust the logo image size.
        w_percent = self.basewidth / float(logo.size[0])
        h_size = int((float(logo.size[1]) * float(w_percent)))
        logo = logo.resize((self.basewidth, h_size), resample=3)
        # Create the QR code.
        err_corr = ERROR_CORRECT[error_correct]
        QRcode = qrcode.QRCode(
            version=version,
            error_correction=err_corr,
            box_size=box_size,
            border=border,
        )
        # Adding text to the new QR code.
        QRcode.add_data(text)
        # Generating the QR code.
        QRcode.make()
        # Adding the color to the QR code.
        QRimg = QRcode.make_image(
            fill_color=fg_color, back_color=bg_color
        ).convert('RGB')
        # Set the size of the QR code.
        pos = (
               (QRimg.size[0] - logo.size[0]) // 2,
               (QRimg.size[1] - logo.size[1]) // 2
        )
        # Add logo to QR code.
        QRimg.paste(logo, pos)
        # Create return image.
        qrcode_image = QRimg
        # Return the qr code image.
        return qrcode_image

    def qr_code_creation(self, text, width, height, bg_color,
                         fg_color, error_correct, version,
                         box_size, border, color, image=None):
        '''Main node function. Create a QR code image.'''
        if image is not None:
            # Create a tensor from the image.
            image = tensor2pil(image)
        else:
            col = string2tuple(fg_color)
            n,m = 100,100
            image = Image.new('RGB', (n, m), col)
        # Create the QR code from the text.
        qrcode_image = self.create_qr_code(text, bg_color, fg_color,
                                           error_correct, version,
                                           box_size, border, image)
        # Resize the image.
        qrcode_image = qrcode_image.resize((width, height), resample=3)
        # Convert the PIL images to Torch tensors.
        image_out = pil2tensor(qrcode_image)
        maskImage = pil2tensor(qrcode_image)
        # Create the masks.
        idx = self.channels.index(color)
        invertedmask = maskImage[:, :, :, idx]
        mask = 1 - invertedmask
        # Return the return types.
        return (image_out, mask, invertedmask)

# *******************
# Class QRCodesSimple
# *******************
class QRCodesSimple:
    '''Create a QR code image.'''

    def __init__(self):
        self.channels = ["red", "green", "blue"]
        self.basewidth = 100

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "bg_color": ("STRING", {"multiline": False, "default": "(0, 0, 0)"}),
                "fg_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "error_correct": (ERR_CORR, {}),
                "version": (VERSION, {}),
                "box_size": ("INT", {"default": 10, "min": 0, "max": 8192}),
                "border": ("INT", {"default": 4, "min": 0, "max": 8192}),
                "radius": ("INT", {"default": 0, "min": 0, "max": 1024}),
                "mask_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("IMAGE", "MASK", "INVERTED_MASK",)
    FUNCTION = "qr_code_creation"
    CATEGORY = "🍭 QR Code Nodes"
    OUTPUT_NODE = True

    def create_qr_code(self, text, bg_color, fg_color, error_correct,
                       version, box_size, border, radius, mask_color):
        '''Create the QR Code image.'''
        # Create the color tuples.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        mask_color = string2tuple(mask_color)
        # Create the QR code.
        err_corr = ERROR_CORRECT[error_correct]
        QRcode = qrcode.QRCode(
            version=version,
            error_correction=err_corr,
            box_size=box_size,
            border=border,
        )
        # Adding text to the new QR code.
        QRcode.add_data(text)
        # Generating the QR code.
        QRcode.make()
        # Adding the color to the QR code.
        QRimg = QRcode.make_image(
            fill_color=fg_color, back_color=bg_color
        ).convert('RGB')
        # Create a mask with rounded corners.
        mask = Image.new("L", QRimg.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, QRimg.size[0], QRimg.size[1]), radius, fill=255)
        # Apply the rounded mask to the image
        QRimg = Image.composite(QRimg, Image.new("RGB", QRimg.size, mask_color), mask)
        # Create return image.
        qrcode_image = QRimg
        # Return the qr code image.
        return qrcode_image

    def qr_code_creation(self, text, width, height, bg_color,
                         fg_color, error_correct, version,
                         box_size, border, radius, mask_color):
        '''Main node function. Create a QR code image.'''
        # Create the QR code from the text.
        qrcode_image = self.create_qr_code(text, bg_color, fg_color,
                                           error_correct, version,
                                           box_size, border, radius,
                                           mask_color)
        # Resize the image.
        qrcode_image = qrcode_image.resize((width, height), resample=3)
        # Convert the PIL images to Torch tensors.
        image_out = pil2tensor(qrcode_image)
        maskImage = pil2tensor(qrcode_image)
        # Create the masks.
        mask_exchange_color = "red"
        idx = self.channels.index(mask_exchange_color)
        invertedmask = maskImage[:, :, :, idx]
        mask = 1 - invertedmask
        # Return the return types.
        return (image_out, mask, invertedmask)

# *********************
# Class QRCodesSimpleBW
# *********************
class QRCodesSimpleBW:
    '''Create a qr code image.'''

    @classmethod
    def INPUT_TYPES(cls):
        '''Define the input types.'''
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": ""}),
                "width": ("INT", {"default": 512, "min": 1, "max": 8192}),
                "height": ("INT", {"default": 512, "min": 1, "max": 8192}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("IMAGE", "MASK", "INVERTED_MASK",)
    FUNCTION = "qr_code_creation"
    CATEGORY = "🍭 QR Code Nodes"
    OUTPUT_NODE = True

    def create_qr_code(self, text):
        '''Create QR code.'''
        # Create the QR code.
        QRimg = qrcode.make(text)
        # Convert to PIL.
        qrcode_image = QRimg.get_image()
        # Return the qr code image.
        return qrcode_image

    def qr_code_creation(self, text, width, height):
        '''Main node function. Create a QR code.'''
        # Create the QR code from the text.
        qrcode_image = self.create_qr_code(text)
        # Resize the QR code.
        qrcode_image = qrcode_image.resize((width, height), resample=3)
        # Define a transform to convert PIL.
        transform = transforms.Compose([
            transforms.PILToTensor()
        ])
        # Convert the image to a Tensor.
        image_out = transform(qrcode_image).to(dtype=torch.float32)
        # Create the masks.
        maskinverted = image_out
        mask = 1 - maskinverted
        # Return the return types.
        return (image_out, mask, maskinverted,)
