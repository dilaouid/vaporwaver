<h1 align="center">vaporwaver.py</h1>
<p align="center"><i>Python version of existing <a target="_blank" href="https://github.com/dilaouid/vaporwaver">vaporwaver</a> PHP version</i></p>
<hr>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white) 


A Python3 script to create vaporwave image based on PNG files. An improved version of the PHP one I did 2 years ago. However, this time I used multiple third-party libraries, which are:
- PIL (Pillow)
- glitch-this (https://github.com/TotallyNotChase/glitch-this)
- opencv-python

You can install them with `pip install -r requirements.txt`

![example](https://github.com/dilaouid/vaporwaver.py/blob/media/example.png)

<hr>

This program uses **tkinter** for the GUI tool (very pretty)

## How does it works
The program takes an image, with or without transparency (though, please use an image with transparency for a better result!), we will call this image the "character"
You can move the character in the X and Y axis, and scale it. You can apply a glitch amount and seed on it and also a predefined gradient map filter.
The gradients are the built in opencv colormap

![colormap](https://github.com/dilaouid/vaporwaver.py/blob/media/gradients.png)

You can add a predefined misc item behind the character, which you can :
- Move
- Rotate
- Scale

And you can select one of the predefined background image. The output image will have a size of 460 x 595 px

## Image ressources
⚠️ **WARNING** ⚠️
For launching, this program needs three files in specific paths. They are already in the repository, but please do not rename nor delete them. You can replace their content tho.
- `picts/backgrounds/default.png`
- `picts/crt/crt.png`
- `picts/miscs/none.png`

**Do not remove thoses files, at any cost !**

### Backgrounds
The backgrounds size, in order to be selectable in the GUI list, must have the size of the output image, which means 460 x 595 px. You can name them as you want, they must be `PNG` files located at the `picts/backgrounds` folder.

### Miscs
The miscs items are just decorations to put behind the character. There is no specific restriction on it. You can take any size, but they still musts be `PNG` files.

# What does the program looks like ?
![screenshot](https://github.com/dilaouid/vaporwaver.py/blob/media/screenshot.png)
