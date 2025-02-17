#!/usr/bin/python
'''Object detection node.'''
# pylint: disable=no-member
# pylint: disable=invalid-name
# pylint: disable=too-many-locals
# pylint: disable=too-many-positional-arguments
# pylint: disable=bare-except
# pylint: disable=too-many-arguments

# Import the Python modules.
from PIL import Image
import cv2
import numpy as np
import torch

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

class CreateCornerFrame:
    '''A node that takes any value and displays it as a string.
    '''

    @classmethod
    def INPUT_TYPES(cls):
        '''Input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
                "fg_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "bg_color": ("STRING", {"multiline": False, "default": "(0, 0, 0)"}),
                "thickness": ("INT", {"default": 4, "min": 1, "max": 8192}),
                "frame_size": ("INT", {"default": 40, "min": 2, "max": 8192}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    OUTPUT_NODE = True

    CATEGORY = "🍭 QR Code Nodes/🎨 frames"
    FUNCTION = "render_data"

    def create_frame(self, image, w0, h0, thickness,
                     frame_size, fg_color, bg_color):
        '''Create frame.'''
        # Create the color tuple.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        # Create a new blank image.
        w1, h1 = w0+frame_size, h0+frame_size
        blank_image = np.zeros((h1, w1, 3), np.uint8)
        blank_image[:,0:w1] = bg_color
        # Get the offset and lens.
        dx, dy = int(frame_size//4), int(frame_size/4)
        lenx = int(w1//4)
        leny = int(h1//4)
        # Define poly line.
        poly = [
            [(w1-dx,h1-dy), (w1-dx-lenx,h1-dy)],
            [(w1-dx,h1-dy), (w1-dx,h1-leny-dy)],
            [(dx,h1-dy),(dx+lenx,h1-dy)],
            [(dx,h1-dy),(dx,h1-dy-leny)],
            [(w1-dx,dy),(w1-dx,dy+leny)],
            [(w1-lenx-dx,dy),(w1-dx,dy)],
            [(dx,dy),(dx+lenx,dy)],
            [(dx,dy),(dx,dy+leny)]
        ]
        # Draw polyline.
        for i in poly:
            print(i)
            start_point = i[0]
            end_point = i[1]
            cv2.line(blank_image, start_point, end_point, fg_color, thickness)
        # Create a new numpy image.
        pil_image = Image.fromarray(blank_image)
        pil_image.paste(image, (4*dx,4*dy))
        # Create a Numpy image.
        pil_image = np.array(pil_image)
        # Return Numpy image.
        return pil_image

    def render_data(self, image, thickness, frame_size, fg_color, bg_color):
        '''Render data.'''
        # Create a Pil from the Tensor.
        image = tensor2pil(image)
        # Copy image.
        newImg = image.copy()
        # Get width and height.
        width, height = newImg.size
        # Create the new image
        img = self.create_frame(newImg, width, height, thickness,
                                frame_size, fg_color, bg_color)
        # Create a Tensor from a Pil imgae.
        image = pil2tensor(img)
        # Return the new image with frame.
        return (image,)

class CreateSolidFrame:
    '''A node that takes any value and displays it as a string.
    '''

    @classmethod
    def INPUT_TYPES(cls):
        '''Input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
                "fg_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "bg_color": ("STRING", {"multiline": False, "default": "(0, 0, 0)"}),
                "thickness": ("INT", {"default": 4, "min": 1, "max": 8192}),
                "frame_size": ("INT", {"default": 40, "min": 2, "max": 8192}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    OUTPUT_NODE = True

    CATEGORY = "🍭 QR Code Nodes/🎨 frames"
    FUNCTION = "render_data"

    def create_frame(self, image, w0, h0, thickness,
                    frame_size, fg_color, bg_color):
        '''Create a text frame.'''
        # Create the color tuple.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        # Set new width and height.
        w1, h1 = int(w0+frame_size*2), int(h0+frame_size*2)
        # Create a new blank image.
        blank_image = np.zeros((h1, w1, 3), np.uint8)
        blank_image[:,0:w1] = bg_color
        # Calculate the offset.
        dx, dy = int(frame_size//2), int(frame_size//2)
        # Create colored rectangle.
        (x1, y1) =  (0, 0)
        (x2, y2) =  (w1,h1)
        cv2.rectangle(blank_image, (x1, y1), (x2, y2), bg_color, -1)
        cv2.rectangle(blank_image, (x1, y1), (x2, y2), fg_color, thickness)
        # Create a new Pil image.
        pil_image = Image.fromarray(blank_image)
        # Merge both images to a new RGB image.
        pil_image.paste(image, (2*dx,2*dy))
        pil_image = pil_image.convert(mode='RGB')
        # Create a Numpy image.
        numpy_image = np.array(pil_image)
        # Return Numpy image.
        return numpy_image

    def render_data(self, image, thickness, frame_size, fg_color, bg_color):
        '''Render data.'''
        # Create Pil image from Tensor.
        image = tensor2pil(image)
        # Copy image.
        newImg = image.copy()
        # Get width and height.
        width, height = newImg.size
        # Create image with frame.
        numpyImg = self.create_frame(newImg, width, height, thickness,
                                     frame_size, fg_color, bg_color)
        # Create Tensor from 'Pil' image.
        image = pil2tensor(numpyImg)
        # return new image.
        return (image,)

class CreateTextFrame:
    '''A node that takes any value and displays it as a string.
    '''

    @classmethod
    def INPUT_TYPES(cls):
        '''Input types.'''
        return {
            "required": {
                "image": ("IMAGE",),
                "fg_color": ("STRING", {"multiline": False, "default": "(255, 255, 255)"}),
                "bg_color": ("STRING", {"multiline": False, "default": "(0, 0, 0)"}),
                "thickness": ("INT", {"default": 4, "min": 1, "max": 8192}),
                "frame_size": ("INT", {"default": 40, "min": 2, "max": 8192}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)
    OUTPUT_NODE = True

    CATEGORY = "🍭 QR Code Nodes/🎨 frames"
    FUNCTION = "render_data"

    def create_frame(self, thickness, fg_color, bg_color):
        '''Create a text frame.'''
        # Create the color tuple.
        fg_color = string2tuple(fg_color)
        bg_color = string2tuple(bg_color)
        # Set new width and height.
        w1, h1 = 1024, 1408
        # Create a new blank image.
        blank_image = np.zeros((h1, w1, 3), np.uint8)
        blank_image[:,0:w1] = bg_color
        # Create colored rectangle.
        (x1, y1) =  (0, 0)
        (x2, y2) =  (w1,h1)
        cv2.rectangle(blank_image, (x1, y1), (x2, y2), bg_color, -1)
        cv2.rectangle(blank_image, (x1, y1), (x2, y2), fg_color, thickness)
        # Calculate the offset.
        dx, dy = 90, 1300
        position = (dx,dy)
        scale = 6
        cv2.putText(
            blank_image, "READ ME", position,
            cv2.FONT_HERSHEY_DUPLEX, scale, fg_color, thickness, cv2.LINE_AA
        )
        # Return Numpy image.
        return blank_image

    def render_data(self, image, thickness, frame_size, fg_color, bg_color):
        '''Render data.'''
        # Create Pil image from Tensor.
        image = tensor2pil(image)
        # Copy image.
        newImg = image.copy()
        # Get width and height.
        width, height = newImg.size
        # Create image with frame.
        numpyImg = self.create_frame(thickness, fg_color, bg_color)
        # Create a new Pil image.
        pil_image = Image.fromarray(numpyImg)
        # Merge both images to a new RGB image.
        size = (int(width)+frame_size, int(height*1.25)+frame_size)
        new_img = pil_image.resize(size, resample=3)
        dx, dy = int(frame_size//2), int(frame_size//2)
        new_img.paste(newImg, (dx,dy))
        pil_image = new_img.convert(mode='RGB')
        # Create a Numpy image.
        pilImg = np.array(pil_image)
        # Create Tensor from 'Pil' image.
        image = pil2tensor(pilImg)
        # return new image.
        return (image,)
