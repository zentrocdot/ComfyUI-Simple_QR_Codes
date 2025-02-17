# Import the Python modules of the node.
from .nodes.qr_codes import *
from .nodes.qr_codes_style_color import *
from .nodes.qr_codes_reader import *
from .nodes.show_data import *
from .nodes.qr_codes_segno import *
from .nodes.qr_codes_segno_simple import *
from .nodes.qr_codes_segno_logo import *
from .nodes.create_frame_01 import *

NODE_CLASS_MAPPINGS = {
    "🛸 QRCodes (Segno Full Version)": QRCodesSegnoFull,
    "🛸 QRCodes (Segno Simple Version)": QRCodesSegnoSimple,
    "🛸 QRCodes (Segno Simple Logo)": QRCodesSegnoLogo,
    "🛰️ QRCodes (Simple Color)": QRCodesSimple,
    "🛰️ QRCodes (Simple Logo)": QRCodesLogo,
    "🛰️ QRCodes (Simple Style)": QRCodesStyle,
    "🛰️ QRCodes (Simple B&W)": QRCodesSimpleBW,
    "🎭 QRCodeReader": QRCodeReader,
    "🎭 ShowData": ShowData,
    "🚢 CreateCornerFrame": CreateCornerFrame,
    "🚢 CreateSolidFrame": CreateSolidFrame,
    "🚢 CreateTextFrame": CreateTextFrame,
    }
    
WEB_DIRECTORY = "./js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

MESSAGE = "\033[34mComfyUI Square Masks Nodes: \033[92mLoaded\033[0m" 

# Print message into the terminal window.
print(MESSAGE)
