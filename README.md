# HideTextInImage
Hides text in a given image

# Requirements
To install the required libraries, use `pip install requirements.txt`

# How it works
For a given image, this script first changes all color values (0-255) of a specified color channel (R, G or B) to even values only.
A text message can then be inputted which will be converted to raw bits.
Starting on the top left of the image, each pixels color channel will then be made odd again or left even corresponding to the bits of the message.

# Configuration
The color channel and the text encoding can be changed at the top of the script.
