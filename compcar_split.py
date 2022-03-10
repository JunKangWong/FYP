from pathlib import Path
from PIL import Image
from convert_voc_to_yolo import convert
import shutil
import zipfile
import re
import numpy as np

def read_file(filepath: Path):
    with open(filepath, "r") as f:
        return list(f)

def write_files(files, data):
    outputs = zip(files, data)
    for file, dataset in outputs:
        with open(file, "w") as f:
            f.writelines(dataset)

def split_by_ratio(arr: list, ratios: list[float]):
    """
    Split array into 2-D array with the ratios and the remaining elements are assigned to a list
    and append to the 2-D array.
    """
    parts = np.ceil(np.array(ratios) * len(arr))
    ind = np.add.accumulate(parts).astype(int)
    return [list(x) for x in np.split(arr, ind)]

def split_info_files(input_path: Path, output_path: Path):
    # read train and test txt files and merge and sort them
    train_txt = read_file(input_path/"train.txt")
    test_txt = read_file(input_path/"test.txt")
    images = sorted([*train_txt, *test_txt])

    # get the start position of each unique model
    matches = [re.match(r"[0-9]*/[0-9]*/[0-9]*", img)[0] for img in images]
    _, counts = np.unique(matches, return_counts=True)
    pos = np.concatenate([[0], np.add.accumulate(counts)])  # insert 0 at the front of counts

    final_train, final_validation, final_test = [], [], []

    # split the dataset using the ratios
    for i in range(len(pos)-1):
        test, validation, train = split_by_ratio(images[pos[i]:pos[i+1]], [.1, .1])
        final_train = np.append(final_train, train)
        final_validation = np.append(final_validation, validation)
        final_test = np.append(final_test, test)

    datasets = [final_train, final_validation, final_test]
    prefixes = ["data/obj/", "data/test/", "data/unseen_test/"]

    # add appropriate prefix to the beginning of each data
    for i in range(len(datasets)):
        datasets[i] = list(map(lambda x: "".join([prefixes[i], x]), datasets[i]))

    # add appopriate prefix to the writing path
    file_suffixes = ["train.txt", "validation.txt", "test.txt"]
    files = list(map(lambda x: output_path/x, file_suffixes))

    write_files(files, datasets)

def move_label_to_image(label_path: Path, image_path: Path):
    for path in label_path.rglob("*.txt"):
        _, _, suffix = str(path).partition("label")
        out = Path("".join([str(image_path), suffix]))
        path.rename(out)
        
def convert_label(label_path: Path):
    for label in sorted(label_path.rglob("*.txt")):
        match = re.search(r"image\\[0-9]*\\([0-9]*)", str(label))   # match with "image\make id\model id"
        model_id = int(match[1]) - 1    # get model id and minus by 1 because yolo starts the index by 0

        image = label.with_suffix(".jpg")

        # get size of image
        size = 0
        with Image.open(image) as im:
            size = im.size

        # get bounding box of label
        box = 0
        with open(label, "r") as f:
            line = f.readlines()[-1]   

            # change the box from [x1, y1, x2, y2] to [x1, x2, y1, y2]
            # where 1 <= x1 < x2 <= image_width, and 1 <= y1 < y2 <= image_height
            box = line.split()
            box[1], box[2] = box[2], box[1]
            box = tuple(map(int, box))   # cast all the values to int

        # write the model id and converted label to the label file
        with open(label, "w") as f:
            f.write("{} {} {} {} {}".format(model_id, *convert(size,box)))

def make(dataset: Path):
    cur = Path.cwd()
    path = cur/"compcar"

    if path.exists():
        for subpath in path.iterdir():
            if subpath.is_dir():
                shutil.rmtree(subpath)
            else:
                subpath.unlink()
    
    with zipfile.ZipFile(dataset, "r") as zip_ref:
        zip_ref.extractall(path)

def main():
    compcar = Path.cwd()/"compcar"
    image, label = compcar/"image", compcar/"label"

    # move labels to image folders
    move_label_to_image(label, image)
    shutil.rmtree(label)

    # splitting the txt info files into specified ratios
    info_in = compcar/"txt info files"
    info_out = compcar/"temp"
    info_out.mkdir(parents=True, exist_ok=True)
    split_info_files(info_in, info_out)

    # move models.txt from txt info files to temp
    models = info_in/"models.txt"
    models.rename(info_out/models.name)

    # remove txt info files directory and rename temp to txt info files
    shutil.rmtree(info_in)
    info_out.rename(info_in)

    # convert labels' format to yolov4 format
    convert_label(image)
    
if __name__ == '__main__':
    zip_filepath = Path().cwd() / "partial_compcars.zip"       # TODO: enter the compcar dataset zip filepath
    make(zip_filepath)
    main()