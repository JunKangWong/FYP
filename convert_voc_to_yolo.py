import glob
import os
import xml.etree.ElementTree as ET
from os import listdir, getcwd
from os.path import join

# dirs = ['train', 'val']
# dirs = ['C:\Users\jkwon\Desktop\test_voc_convert']

def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    width, height = size
    xmin, xmax, ymin, ymax = box
    dw, dh = 1./width, 1./height

    x, y = (xmin + xmax)/2.0 - 1, (ymin + ymax)/2.0 - 1
    w, h = xmax-xmin, ymax-ymin
    
    x, y, w, h = x*dw, y*dh, w*dw, h*dh
    return (x,y,w,h)

def convert_annotation(classes, dir_path, output_path, image_path):
    basename = os.path.basename(image_path)
    basename_no_ext = os.path.splitext(basename)[0]

    in_file = open(dir_path + '/' + basename_no_ext + '.xml')
    out_file = open(output_path + basename_no_ext + '.txt', 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def main():
    dirs = ['all']
    classes = ['BMW_3Series', 'hyundai_elantra', 'hyundai_grandStarex', 'Mazda_3', 'Mazda_CX-5',
           'Mercedes_C-Class', 'Proton_Exora', 'Proton_Iriz', 'Proton_Persona', 'Proton_Saga',
           'Proton_X50', 'Proton_X70', 'toyota_alphard', 'toyota_camry', 'toyota_corollaAltis',
           'toyota_fortuner', 'toyota_harrier', 'toyota_hilux', 'toyota_vellfire', 'toyota_vios',
           'honda_accord', 'honda_city_6thGen', 'honda_crv_i-VTEC SUV_4thGen', 'honda_crv_i-VTEC SUV_5thGen', 'honda_jazz_i-VTEC_3rdGen', 
           'perodua_alza_1.5advanceMPV', 'perodua_axia_advance', 'perodua_bezza_xPremiumSedan', 'perodua_myvi_2ndGen', 'perodua_viva_ez_ex']


    cwd = getcwd()
    for dir_path in dirs:
        full_dir_path = cwd + '/' + dir_path
        output_path = full_dir_path +'/yolo/'

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        image_paths = getImagesInDir(full_dir_path)
        list_file = open(full_dir_path + '.txt', 'w')

        for image_path in image_paths:
            list_file.write(image_path + '\n')
            convert_annotation(classes, full_dir_path, output_path, image_path)
        list_file.close()

        print("Finished processing: " + dir_path)


if __name__ == "__main__":
    main()