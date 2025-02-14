# Import the Python modules of the node.
from .nodes.qr_codes import *

NODE_CLASS_MAPPINGS = { 
    "🎭 QRCodes (Simple B&W)": QRCodesSimpleBW,
    "🎭 QRCodes (Simple Color)": QRCodesSimple,
    "🎭 QRCodes (Logo)": QRCodesLogo,
    }
    
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

MESSAGE = "\033[34mComfyUI Square Masks Nodes: \033[92mLoaded\033[0m" 

# Print message into the terminal window.
print(MESSAGE)
