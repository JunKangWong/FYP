import xml.etree.ElementTree as ET
from PIL import Image, ImageOps
from pathlib import Path

def save_mirror_image(im_path: Path, save_path: Path):
    with Image.open(im_path) as im:
        im_flip = ImageOps.mirror(im)
        im_flip.save(save_path)

def save_mirror_box(im_path: Path, xml_path: Path, save_path: Path):
    with Image.open(im_path) as im:
        width = im.width
        tree = ET.parse(xml_path)
        root = tree.getroot()

        path_elem = root.find("path")
        path_elem.text = str(save_path)

        for bndbox in root.iter("bndbox"):
            xmin, xmax = bndbox.find("xmin"), bndbox.find("xmax")
            new_xmin, new_xmax = width-int(xmax.text), width-int(xmin.text)
            xmin.text, xmax.text = str(new_xmin), str(new_xmax)
        
        tree.write(save_path)
            
def compute_mirror_images_and_boxes(path: Path):
    """
    Compute the mirror images and the associated bounding boxes in the directory at the path
    """
    def compute(imgs: list[Path], i, direction):
        # get name of car model
        try:
            end = imgs[0].stem.find("_")  
            stem = imgs[0].stem[:end]
        except:
            return

        for im in imgs:
            im_save_path = im.with_stem(f"{stem}{direction}{i:03d}")
            xml_path = im.with_suffix(".xml")
            xml_save_path = im_save_path.with_suffix(".xml")

            save_mirror_image(im, im_save_path)
            save_mirror_box(im, xml_path, xml_save_path)
            i += 1

    left = list(path.glob("*_L_*.jpg"))
    right = list(path.glob("*_R_*.jpg"))
    l, r = len(left)+1, len(right)+1

    compute(left, r, "_R_")
    compute(right, l, "_L_")

def run_compute_mirror_images_and_boxes_recur(path: Path):
    """Compute mirror images and associated bounding boxes recursively"""
    for dir in path.iterdir():
        for next_dir in dir.iterdir():
            if next_dir.is_dir():
                compute_mirror_images_and_boxes(next_dir)


if __name__ == "__main__":
    your_path = r"C:\Users\jkwon\Desktop\car_images2"
    path = Path(your_path)
    run_compute_mirror_images_and_boxes_recur(path)