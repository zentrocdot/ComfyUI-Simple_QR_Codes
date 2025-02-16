#!/usr/bin/python
'''Simple QR code node for the creation of decorated QR codes.'''
#
# QR Code is a registered trademark of the DENSO WAVE INCORPORATED.
#
# [1] https://www.qrcode.com/en/faq.html
#
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

# Import the Python modules.
from PIL import Image, ImageDraw
import numpy as np
import torch
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    CircleModuleDrawer, SquareModuleDrawer, RoundedModuleDrawer,
    GappedSquareModuleDrawer, VerticalBarsDrawer, HorizontalBarsDrawer
)
from qrcode.image.styles.colormasks import (
    RadialGradiantColorMask, SolidFillColorMask, SquareGradiantColorMask,
    HorizontalGradiantColorMask, VerticalGradiantColorMask
)

# Set the error correction.
ERROR_CORRECT = {"ERROR_CORRECT_L": qrcode.constants.ERROR_CORRECT_L,
                 "ERROR_CORRECT_M": qrcode.constants.ERROR_CORRECT_M,
                 "ERROR_CORRECT_Q": qrcode.constants.ERROR_CORRECT_Q,
                 "ERROR_CORRECT_H": qrcode.constants.ERROR_CORRECT_H}

# Get key word list.
ERR_CORR = list(ERROR_CORRECT.keys())

# Create version list.
VERSION = list(range(1, 41))

# Set the dictionary.
STYLE_DICT = {"CircleModuleDrawer": CircleModuleDrawer(),
              "RoundedModuleDrawer": RoundedModuleDrawer(),
              "SquareModuleDrawer": SquareModuleDrawer(),
              "GappedSquareModuleDrawer": GappedSquareModuleDrawer(),
              "VerticalBarsDrawer": VerticalBarsDrawer(),
              "HorizontalBarsDrawer": HorizontalBarsDrawer(),
}
# Get key word list.
STYLE_LIST = list(STYLE_DICT.keys())

# Set the dictionary.
COLOR_DICT = {"RadialGradiantColorMask": RadialGradiantColorMask(),
              "SolidFillColorMask": SolidFillColorMask(),
              "SquareGradiantColorMask": SquareGradiantColorMask(),
              "HorizontalGradiantColorMask": HorizontalGradiantColorMask(),
              "VerticalGradiantColorMask": VerticalGradiantColorMask()
}

# Get key word list.
COLOR_LIST = list(COLOR_DICT.keys())

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
# Class QRCodesStyle
# ******************
class QRCodesStyle:
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
                "radius": ("INT", {"default": 0, "min": 0, "max": 8192}),
                "style": (STYLE_LIST, {}),
                "color": (COLOR_LIST, {}),
                "color_1st": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "color_2nd": ("STRING", {"multiline": False, "default": "(255, 0, 0)"}),
                "color_3rd": ("STRING", {"multiline": False, "default": "(255, 0, 255)"}),
                "mask_color": (["red", "green", "blue"], {}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("IMAGE", "MASK", "INVERTED_MASK",)
    FUNCTION = "qr_code_creation"
    CATEGORY = "🍭 QR Code Nodes/🚜 qrcode-based"
    OUTPUT_NODE = True

    def create_qr_code(self, text, bg_color, fg_color, error_correct, version,
                       radius, box_size, border, mask_color, style,
                       color, color_1st, color_2nd, color_3rd):
        '''Create the QR Code image.'''
        # Create the color tuples.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        mask_color = string2tuple(mask_color)
        color_1st = string2tuple(color_1st)
        color_2nd = string2tuple(color_2nd)
        color_3rd = string2tuple(color_3rd)
        # Set the error correction.
        err_corr = ERROR_CORRECT[error_correct]
        # Create the QR code.
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
        QRimg = None
        # Get style.
        isStyle = STYLE_DICT[style]
        # Define color style function.
        col1 = color_1st
        col2 = color_2nd
        col3 = color_3rd
        def color_style(color, col1, col2, col3):
            '''Set color to style.'''
            match color:
                case "SolidFillColorMask":
                    return qrcode.image.styles.colormasks.SolidFillColorMask(
                        back_color=col1, front_color=col2
                    )
                case "RadialGradiantColorMask":
                    return qrcode.image.styles.colormasks.RadialGradiantColorMask(
                        back_color=col1, center_color=col2, edge_color=col3
                    )
                case "SquareGradiantColorMask":
                    return qrcode.image.styles.colormasks.SquareGradiantColorMask(
                        back_color=col1, center_color=col2, edge_color=col3
                    )
                case "HorizontalGradiantColorMask":
                    return qrcode.image.styles.colormasks.HorizontalGradiantColorMask(
                        back_color=col1, left_color=col2, right_color=col3
                    )
                case "VerticalGradiantColorMask":
                    return qrcode.image.styles.colormasks.VerticalGradiantColorMask(
                        back_color=col1, top_color=col2, bottom_color=col3
                    )
        # Get color.
        isColor = color_style(color, col1, col2, col3)
        # Create the QR code.
        QRimg = QRcode.make_image(
            fill_color=fg_color, back_color=bg_color,
            image_factory=StyledPilImage,
            module_drawer=isStyle,
            color_mask=isColor
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

    def qr_code_creation(self, text, width, height, bg_color, fg_color,
                         error_correct, version, radius, box_size,
                         border, mask_color, style, color, color_1st,
                         color_2nd, color_3rd):
        '''Main node function. Creation of a QR code image.'''
        # Create the QR code from the text.
        qrcode_image = self.create_qr_code(text, bg_color, fg_color, error_correct,
                                           version, radius, box_size, border,
                                           mask_color, style, color, color_1st,
                                           color_2nd, color_3rd)
        # Resize the image.
        qrcode_image = qrcode_image.resize((width, height), resample=3)
        # Convert the PIL images to Torch tensors.
        image_out = pil2tensor(qrcode_image)
        maskImage = pil2tensor(qrcode_image)
        # Create the masks.
        idx = self.channels.index(mask_color)
        invertedmask = maskImage[:, :, :, idx]
        mask = 1 - invertedmask
        # Return the return types.
        return (image_out, mask, invertedmask)
