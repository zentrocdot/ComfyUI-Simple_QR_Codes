# ComfyUI Simple QR Codes Node

> [!IMPORTANT]  
> <p align="justify">🚧 This documentation is still under construction.
> Parts of the node are still in development. There may be therefore
> minor differences between the node itself and the documentation of
> the node. The documentation is also not yet complete.</p>

## Preface

<p align="justify">A distinction must be made between the terms node and
node. In the Comfy registry there is a node registered. In this case this
is the <code>ComfyUI-Simple_QR_Codes</code> node. Such a node can be
installed using the ComfyUI Manager or using a terminal window and cloning
the node to the correct directory <code>custom_nodes</code>. In case of my
registered node, there are seven different nodes are contained which can be
used in a workflow.</p>

## Get Started

<p align="justify">The word QR Code is a registered trademark of the 
DENSO WAVE INCORPORATED in Japan and other countries. The trademark
refers primarily to the word QR Code. However, it should be noted that
the trademark must also refer to the encoding and decoding, otherwise
the benefits of the QR code would be diluted. Nevertheless the created
QR Code images can be used private as well as commercial free of
charge.</p>

<p align="justify">For the QR code generation one can use the Python
module <code>qrcode</code> or the Python module <code>segno</code>. I
make use of both of them. In terms of regulations, I have to say that 
I have not checked that both Python modules comply with the published
QR code standards.</p>

# Segno Based Node

## Nodes Preview

<p align="justify">Figure 1 shows a preview of the three nodes which
can be used for the creation of QR codes. In the text area one writes
the text which should be encoded as QR code.</p>

![image](https://github.com/user-attachments/assets/83d2c020-9003-4ed7-83d6-ef797bd69d22)

*Figure 1: Nodes overview* 



## Node Preview 

![image](https://github.com/user-attachments/assets/62d96992-c423-4f0a-ba55-1b4a5800f73a)

*Figure 2: Workflow preview* 

# Qrcode Based 

## Introduction

<p align="justify">So far I have created three nodes. The main goal
is to create good looking QR codes that can be used in ComfyUI ComfyUI
or that can be saved and used in other applications or in other 
contexts.</p>

<p align="justify">The first node, the simplest, was for testing and
learning purposes. The second node can create colorful QR codes and
round corners can be added. The third node can be used to integrate
logos or image in the QR code.</p> 

<p align="justify">One idea I have since discarded is the ability to 
invert the created images. Especially with the QR code with logo, this
idea no longer makes sense.</p>

<p align="justify">The node is supplied with everything needed to work
with each node.</p>


## Node Preview

![image](https://github.com/user-attachments/assets/d22611f0-8e74-4bd0-978c-0f51294ea01f)

*Figure 3: QRCodes (Simple Color)* 

![image](https://github.com/user-attachments/assets/9779b51c-9529-40c1-9f06-2d92c908dbae)

*Figure 4: QRCodes (Logo)* 

![image](https://github.com/user-attachments/assets/e06c0c9f-bd85-411e-9d8c-df3fe2de0203)

*Figure 5: QRCodes (Simple B&W)* 

## Special Features

<p align="justify">A special feature of the second node is the
ability to add round corners to the QR code.</p>

## Limitations

<p align="justify">The rudimentary QR code reader node is only
suitable for reading black QR code on white background so far.</p>

## Open Issues

<p align="justify">Using the Python package <code>qrcode</code> it
is not clear how to control the size of the created QR code. For the
moment the QR Code is created an then this QR code is resized. This
leads to a loss in quality.</p>

## To-Do

<p align="justify">In the course of the day I will programme a qr code
scan node. Then I can check the result of the QR code creation within
the same workflow.</p>

## Legal Notice

<p align="justify">QR Code is a registered trademark of the DENSO WAVE INCORPORATED.</p>

# References

[1] https://pypi.org/project/qrcode/

[2] https://pypi.org/project/segno/

[3] https://pypi.org/project/segno-pil/

[4] https://segno.readthedocs.io/en/latest/

[5] https://www.copus.io/work/a64d054abaa25f57bc1d23c59e5bec71?spaceId=zentrocdotsposts

[6] https://www.copus.io/work/4444e7bc1d45f2fca85a06d5646feb47?spaceId=zentrocdotsposts

[7] https://github.com/coreyryanhanson/ComfyQR-scanning-nodes

[8] https://registry.comfy.org/nodes

[9] https://github.com/heuer/segno/

[10] https://www.qrcode.com/en/faq.html
