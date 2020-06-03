from PIL import Image
from tkinter.filedialog import askopenfile
from tkinter import Tk
import bitarray

# specify the color channel to use (red=0 green=1 blue=2 (alpha=3))
COLOR_CHANNEL = 0

# specify text encoding to use (in most cases 'ascii' or 'utf8')
TEXT_ENCODING = 'utf8'

def array_from_image(dialog_title: str = 'Select file') -> (list, int, int):
    root = Tk()
    root.withdraw()

    file = askopenfile(title=dialog_title)
    if file is None:
        exit()
    file = file.name
    img = Image.open(file)
    height, width = img.height, img.width
    data = list(img.getdata())

    return data, height, width


def array_to_image(array: list, img_height, img_width, show_image: bool = True, image_name: str = 'out.png') -> str:

    out = Image.new('RGBA', (img_width, img_height))
    out.putdata(array)
    out.save(image_name, 'PNG')

    if show_image:
        out.show()

    return image_name


def even_colorchannel(array: list, color_channel: int):
    for i, pixl in enumerate(array):
        colorvalue = pixl[color_channel]
        if colorvalue % 2 == 1: # odd
            new_pixl = list(pixl)
            new_pixl[color_channel] = colorvalue - 1
            array[i] = tuple(new_pixl)


def hide_bitlist_in_array(array:list, color_channel: int, bitlist: list):
    if len(bitlist) > len(array):
        print('The image is too small to hide this messages.')
        exit(47)

    for i, bit in enumerate(bitlist):
        pixl = list(array[i])
        pixl[color_channel] += bit
        pixl = tuple(pixl)
        array[i] = pixl


def string_to_bitlist(string: str, textencoding) -> list:
    ba = bitarray.bitarray()  # https://stackoverflow.com/a/10238101/11998115

    ba.frombytes(string.encode(textencoding))
    l = ba.tolist()
    return l


def bitlist_to_string(bitlist: list, textencoding) -> str:
    return bitarray.bitarray(bitlist).tobytes().decode(textencoding)


def hide_text_in_image(text: str, text_encoding, color_channel: int) -> str:
    inp_bitlist = string_to_bitlist(text, text_encoding)
    main_array, img_height, img_width = array_from_image(dialog_title='Select the image in which to hide the message')
    even_colorchannel(main_array, color_channel)
    hide_bitlist_in_array(main_array, color_channel, inp_bitlist)
    filename = array_to_image(main_array, img_height, img_width)
    return filename


def read_text_from_image(text_encoding, color_channel) -> str:
    main_array, img_height, img_width = array_from_image(dialog_title='Select the image to read from')
    message_bits = []
    for pixl in main_array:
        message_bits.append(bool(pixl[color_channel] % 2))

    outstr = bitlist_to_string(message_bits, text_encoding)
    return outstr

if __name__ == '__main__':
    mode = input('What would you like to do? (hide/read) ').lower()

    if mode in ('hide', 'h'):
        inp = input('Please enter your message:\n')
        outfile = hide_text_in_image(inp, TEXT_ENCODING, COLOR_CHANNEL)
        print(f'Done. Image saved as "{outfile}".')
    elif mode in ('read', 'r'):
        msg = read_text_from_image(TEXT_ENCODING, COLOR_CHANNEL)
        print(msg)
