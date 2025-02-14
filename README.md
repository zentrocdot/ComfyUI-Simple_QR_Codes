# ComfyUI-Simple_QR_Codes

> [!IMPORTANT]  
> <p align="justify">🚧 This documentation is still under construction.
> Parts of the node are still in development. There may be therefore
> minor differences between the node itself and the documentation of
> the node. The documentation is also not yet complete.</p>

## Introduction

<p align="justify">So far I have created three nodes. The first, the 
simplest, was for testing and learning purposes. The main goal is to 
create good looking QR codes that can be used in ComfyUI ComfyUI or
that can be saved and used in other applications or in other contexts.</p>

<p align="justify">The second node can create colorful QR codes and round corners can be
added. The third node can be used to integrate logos or image in the QR</p> 
code.

<p align="justify">One idea I have since discarded is the ability to invert the created images.
Especially with the QR code with logo, this idea no longer makes sense.</p>

## Node Preview

![image](https://github.com/user-attachments/assets/ddaeabac-883c-4677-b953-fc7be83f2900)

# Special Features

A special feature of the second node is the ability to add round corners to the QR code.

## Open Issues

<p align="justify">Using the Python package <code>qrcode</code> it
is not clear how to control the size of the created QR code. For the
moment the QR Code is created an then this QR code is resized. This
leads to a loss in quality.</p>

## To-Do

<p align="justify">In the course of the day I will programme a qr code
scan node. Then I can check the result of the QR code creation within
the same workflow.</p>

# References

[1] https://pypi.org/project/qrcode/

[2] https://pypi.org/project/segno/

[3] https://www.copus.io/work/a64d054abaa25f57bc1d23c59e5bec71?spaceId=zentrocdotsposts
