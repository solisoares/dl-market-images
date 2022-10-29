#!/usr/bin/python3
import os
import argparse
import requests
from bs4 import BeautifulSoup


def get_imgs_from_BIG(
    url: str,
    url_pattern: str
):
    """ Return images name and images source link.

    Args:
        url (str): BIG supermarket product source
        url_pattern (str): Pattern followed by the source links of the images found on the BIG website

    Returns:
        imgs_name (list), imgs_src (list): Lists with image name and source link
    """

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get all html tags that contain this url pattern
    imgs_tag = soup.select(f'img[src^="{url_pattern}"]')

    # Get the name of the products.
    imgs_name = [img_tag["alt"] for img_tag in imgs_tag]
    
    # Get the source url of the products.
    imgs_src = [img_tag["src"] for img_tag in imgs_tag]
    return imgs_name, imgs_src


def request_img_content(
    img_src: str
):
    """ Return img binaries 
    Parameters
        img_src (str): Image source link
    Returns
        img (Bytes): Bytes of the image.
    """

    img = requests.get(img_src).content
    return img


def __mkdir(dirpath: str):
    """ Creates a directory if it does not exist. 
    If it exists, do nothing.

    Parameters:
        > dirpath : String. Path to directory.
    Return:
        > None : Nothing 
    """

    if os.path.isdir(dirpath) is False:
        os.mkdir(dirpath)


def save_img(
    dirpath: str,
    img: bytes,
    img_name: str
):
    """ Save image to specified location.

    Parameters:
        > dirpath : String. Path to directory.
        > img : Bytes. Image content in Bytes
        > img_name : Name of the image to save
    Return:
        > None. 
    """

    __mkdir(dirpath)
    img_path = os.path.join(dirpath, img_name + ".png")

    with open(img_path, "wb") as file:
        file.write(img)


def parse_args():
    """ Parse args from terminal. """
    script_description = """ This script search and download product images from the BIG SuperMarket WebSite """
    parser = argparse.ArgumentParser(script_description)
    # parser.add_argument("dir", type=str, help="Directory to download images")
    parser.add_argument("products", nargs="+", type=str,
                        help="Products to search for")
    return parser.parse_args()


def main(products: list):  # products = ["arroz", "feijao"]
    """ Run the script. Scrape BIG Supermarket WebSite and download product images. """
    PRODUCT_URL = "https://www.big.com.br/{}?page={}"
    URL_PATTERN = "https://bighiper.vtexassets.com/arquivos/ids"
    DIRPATH = "./{}"

    for product in products:
        page = 1
        print(f"\n -- {product} -- ")
        # Get image names and source links
        imgs_name, imgs_src = [], []
        while True:
            # Product search in Supermarket WebSite
            url = PRODUCT_URL.format(product, page)
            imgs_name = imgs_name + get_imgs_from_BIG(url, URL_PATTERN)[0]
            imgs_src = imgs_src + get_imgs_from_BIG(url, URL_PATTERN)[1]
            if get_imgs_from_BIG(url, URL_PATTERN) == ([], []):
                break
            page += 1

        # Save images
        for name, src in zip(imgs_name, imgs_src):
            img = request_img_content(src)  # conteudo em si
            print(f"Downloading {name} ...")
            save_img(DIRPATH.format(product), img, name)
    print("\n Done. xD \n")


if __name__ == "__main__":
    args = parse_args()
    main(args.products)
