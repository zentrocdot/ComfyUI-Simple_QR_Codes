#!/usr/bin/python
'''Simple qr code node.'''
# pylint: disable=import-error
# pylint: disable=invalid-name
# pylint: disable=bare-except
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
##pylint:#disable=line-too-long
##pylint:#disable=consider-using-from-import
#
# https://www.geeksforgeeks.org/generate-qr-code-using-qrcode-in-python/
# https://realpython.com/python-generate-qr-code/
# https://pypi.org/project/qrcode/
# https://segno.readthedocs.io/en/latest/

# Import the Python modules.
from PIL import Image
import numpy as np
import torch
import qrcode
import segno

# Create version list.
VERSION = list(range(1, 41))

# Set error correction.
ERROR_LEVEL = ["L", "M", "Q", "H"]

# -----------------------
# Tensor to PIL function.
# -----------------------
def tensor2pil(image):
    '''Tensor to PIL image.'''
    # Return a PIL image.
    return Image.fromarray(np.clip(255.0 * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# ---------------------------------
# Convert 'PIL' to Tensor function.
# ---------------------------------
def pil2tensor(image):
    '''PIL image to tensor.'''
    # Return a Tensor.
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

# **********************
# Class QRCodesSegnoFull
# **********************
class QRCodesSegnoFull:
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
                "scale": ("INT", {"default": 4, "min": 0, "max": 1024}),
                "error_correct": (ERROR_LEVEL, {}),
                "version": (VERSION, {}),
                "border": ("INT", {"default": 4, "min": 0, "max": 8192}),
                "dark": ("STRING", {"multiline": False, "default": "darkred"}),
                "light": ("STRING", {"multiline": False, "default": "salmon"}),
                "data_dark": ("STRING", {"multiline": False, "default": "darkorange"}),
                "data_light": ("STRING", {"multiline": False, "default": "yellow"}),
                "alignment_dark": ("STRING", {"multiline": False, "default": "darkgreen"}),
                "alignment_light": ("STRING", {"multiline": False, "default": "palegreen"}),
                "version_dark": ("STRING", {"multiline": False, "default": "peru"}),
                "version_light": ("STRING", {"multiline": False, "default": "tan"}),
                "finder_dark": ("STRING", {"multiline": False, "default": "darkblue"}),
                "finder_light": ("STRING", {"multiline": False, "default": "lightblue"}),
                "format_dark": ("STRING", {"multiline": False, "default": "indigo"}),
                "format_light": ("STRING", {"multiline": False, "default": "magenta"}),
                "timing_dark": ("STRING", {"multiline": False, "default": "mediumvioletred"}),
                "timing_light": ("STRING", {"multiline": False, "default": "pink"}),
                "separator": ("STRING", {"multiline": False, "default": "azure"}),
                "dark_module": ("STRING", {"multiline": False, "default": "black"}),
                "quiet_zone": ("STRING", {"multiline": False, "default": "lightyellow"}),
                "mask_color": (["red", "green", "blue"], {}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK", "MASK",)
    RETURN_NAMES = ("IMAGE", "MASK", "INVERTED_MASK",)
    FUNCTION = "qr_code_creation"
    CATEGORY = "🍭 QR Code Nodes/🚂 segno-based"
    OUTPUT_NODE = True

    def create_qr_code(self, text, error_correct, version, border,dark, light,
                       data_dark, data_light, alignment_dark, alignment_light,
                       version_dark, version_light, quiet_zone, finder_dark,
                       finder_light, format_dark, format_light, timing_dark,
                       timing_light, separator, dark_module, scale):
        '''Create the QR Code image.'''
        # Create the QR code.
        error = error_correct.lower()
        QRcode = segno.make(text, version=version, error=error_correct)
        # Configure the QR code image.
        dark = None if dark == "None" else dark
        light = None if light == "None" else light
        data_dark = None if data_dark == "None" else data_dark
        data_light = None if data_light == "None" else data_light
        alignment_dark = None if alignment_dark == "None" else alignment_dark
        alignment_light = None if alignment_light == "None" else alignment_light
        version_dark = None if version_dark == "None" else version_dark
        version_light = None if version_light == "None" else version_light
        finder_dark = None if finder_dark == "None" else finder_dark
        finder_light = None if finder_light == "None" else finder_light
        format_dark = None if format_dark == "None" else format_dark
        format_light = None if format_light == "None" else finder_light
        timing_dark = None if timing_dark == "None" else timing_dark
        timing_light = None if timing_light == "None" else timing_light
        dark_module = None if dark_module == "None" else dark_module
        separator = None if separator == "None" else separator
        quiet_zone = None if quiet_zone == "None" else quiet_zone
        qrcode_image = QRcode.to_pil(
            scale=scale,
            border=border,
            dark=dark,
            light=light,
            data_dark=data_dark,
            data_light=data_light,
            quiet_zone=quiet_zone,
            alignment_dark=alignment_dark,
            alignment_light=alignment_light,
            version_dark=version_dark,
            version_light=version_light,
            finder_dark=finder_dark,
            finder_light=finder_light,
            format_dark=format_dark,
            format_light=format_light,
            timing_dark=timing_dark,
            timing_light=timing_light,
            dark_module=dark_module,
            separator=separator
        )
        # Return the QR code image.
        return qrcode_image

    def qr_code_creation(self, text, width, height, error_correct, version,
             border, mask_color, dark, light, data_dark, data_light,
             alignment_dark, alignment_light, version_dark, version_light,
             quiet_zone, finder_dark, finder_light, format_dark, format_light,
             timing_dark, timing_light, separator, dark_module, scale):
        '''Main node function. Create a QR code image.'''
        # Create the QR code from the given text.
        qrcode_image = self.create_qr_code(text, error_correct, version,
            border, dark, light, data_dark, data_light, alignment_dark,
            alignment_light, version_dark, version_light, quiet_zone,
            finder_dark, finder_light, format_dark, format_light,
            timing_dark, timing_light, separator, dark_module, scale)
        # Resize the image. Convert the image to RGB.
        qrcode_image = qrcode_image.resize((width, height), resample=3)
        qrcode_image = qrcode_image.convert(mode='RGB')
        # Convert the PIL image to a Numpy array.
        qrcode_image = np.array(qrcode_image)
        # Convert the the 'PIL' images to Torch Tensors.
        image_out = pil2tensor(qrcode_image)
        maskImage = pil2tensor(qrcode_image)
        # Create a mask and a inverted mask.
        idx = self.channels.index(mask_color)
        invertedmask = maskImage[:, :, :, idx]
        mask = 1 - invertedmask
        # Return the return types.
        return (image_out, mask, invertedmask,)
