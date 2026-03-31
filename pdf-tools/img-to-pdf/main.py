# PNG to PDF converter v0.0.1
# Code by Enrique Luis P. Alvarado
# epalvarado@up.edu.ph

# Based on https://stackoverflow.com/a/47283224

from math import floor
from typing import Callable
from PIL import Image, ImageFile
from defs import *
from const import *
from os import getcwd, listdir
from os.path import abspath
import sys


# DEFINITIONS

# scales size by s percent
def scale_size(from_size: tuple[int, int], percent: float) -> tuple[int, int]:
    return (floor(from_size[0] * percent), floor(from_size[1] * percent))

# scales size to paper size ratio
def ratio_size(from_size: tuple[int, int], to_size: tuple[int, int]) -> tuple[int, int]:

    target_ratio = to_size[0]/to_size[1]    # alpha = tgt_w / tgt_h
    
    scaled_height = floor(max(from_size[1], to_size[1]))
    scaled_width = floor(target_ratio * scaled_height)

    return (scaled_width, scaled_height)


# get best dimensions based on performance needs
def get_best_dimensions(
        imageList: list[Image.Image] | list[ImageFile.ImageFile],
        compfunc: Callable[[Image.Image | ImageFile.ImageFile, tuple[int, int]], bool]
    ) ->tuple[int, int]:
    min_dim = None
    for image in imageList:
        if min_dim is None:
            min_dim = image.size
        if compfunc(image, min_dim):
            min_dim = image.size
    if min_dim is None:
        return (-1, -1)
    return min_dim

def get_min_dimensions(imageList: list[Image.Image] | list[ImageFile.ImageFile]):
    return get_best_dimensions(imageList, lambda image, best: image.size[0] <= best[0] and image.size[1] <= best[1])

def get_max_dimensions(imageList: list[Image.Image] | list[ImageFile.ImageFile]):
    return get_best_dimensions(imageList, lambda image, best: image.size[0] >= best[0] and image.size[1] >= best[1])

def load_images(dir: str) -> list[ImageFile.ImageFile]:
                                                            
    # get image filenames
    imageFileNames = sorted(listdir(dir))

    # load images from folder using the gathered filenames
    imageList = []
    for imageFileName in imageFileNames:
        try:
            imageList.append(Image.open(f"{dir}{imageFileName}"))
        except:
            imageList.append(Image.open(f"{dir}/{imageFileName}"))
    
    return imageList

def save_to_pdf(folder_name: str, scale: float = 1, paper_size: str | None = None, full_path: bool = False, performance: bool = False, pdf_name: str | None = None):

    # load images from folder
    images = load_images(abspath(folder_name) if full_path else f'{getcwd()}/input/{folder_name}/')

    if scale != 1:
        min_dim = (get_min_dimensions if performance else get_max_dimensions)(images)
        scaled_dim = scale_size(min_dim, scale)
        images = list(map(lambda image: image.resize(scaled_dim), images))

    if paper_size is not None:
    # resize images to minimum/maximum dimensions depending on performance mode flag
        min_dim = (get_min_dimensions if performance else get_max_dimensions)(images)
        scaled_dim = ratio_size(min_dim, PAGE_SIZE_PX[paper_size])
        images = list(map(lambda image: image.resize(scaled_dim), images))

    # save to /<folder_name>/<folder_name>.pdf
    pdf_path = PROGRAM_DIR + f'{folder_name if pdf_name is None else pdf_name}.pdf'

    images[0].save(
        pdf_path, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:]
    )

if __name__ == "__main__":

    if len(sys.argv) > 1:
        folder_name = sys.argv[1]
        scale = 1 if len(sys.argv) <= 2 else eval(sys.argv[2])
        paper_size = None if len(sys.argv) <= 3 else sys.argv[3]
        save_to_pdf(folder_name, full_path=True, scale=scale, paper_size=paper_size)
    else:
        print(f"USAGE:")
        print(f"  python main.py <folder_path> <scale> <paper_size>")
        print()
        print(f"  paper_size can be: folio, a4, short")
        # folder_name: string = name of the folder in the same directory as this python script
        # scale: float = size multiplier
        # paper_size: None | string
        for folder_name, scale, paper_size in [
            ("example", 1, "folio")
        ]:
            save_to_pdf(folder_name, scale=scale, paper_size=paper_size)