import glob
import json
import os
import shutil

import cv2
import matplotlib.pyplot as plt
from tqdm import tqdm

classes = [
    "helmet"
]  # classes (to decide indices)
dataset_path = "helmet_total_data"  # path to the dataset with files as .jpg and .json

output_data_path = dataset_path + "_out"
os.makedirs(output_data_path, exist_ok=True)

json_file_paths = glob.glob(f"{dataset_path}/*.json")
json_file_paths = list(map(os.path.basename, json_file_paths))


# get the output data file- label_index, normalized xc, yc, w, h; given the json file
def get_data_string(json_file_path):
    with open(json_file_path) as f:
        img_path = json_file_path[:-4] + "png"  # remove the .json and add jpg
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_h, img_w = img.shape[:2]

        final_string = ""
        for info in json.load(f)["shapes"]:
            label = info["label"].lower()
            label_index = classes.index(label)
            (x1, y1), (x2, y2) = info["points"]
            w = x2 - x1
            h = y2 - y1
            x_c = x1 + w / 2
            y_c = y1 + h / 2

            x_c, w = x_c / img_w, w / img_w
            y_c, h = y_c / img_h, h / img_h
            x_c, y_c, w, h = list(map(lambda x: max(0, min(x, 1)), [x_c, y_c, w, h]))
            final_string += f"{label_index} {x_c} {y_c} {w} {h}\n"
            # cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # cv2.putText(
            #     img,
            #     label,
            #     (x1, y1),
            #     cv2.FONT_HERSHEY_COMPLEX,
            #     1,
            #     (255, 255, 255),
            #     2,
            #     cv2.LINE_AA,
            # )
    # plt.imshow(img)
    # plt.show()
    return final_string[:-1]


for json_file_path in tqdm(json_file_paths):
    txt_path = json_file_path[:-4] + "txt"
    try:
        data_string = get_data_string(f"{dataset_path}/{json_file_path}")
    except Exception as e:
        print(e)
        print(json_file_path)

    with open(f"{output_data_path}/{txt_path}", "w") as f:
        f.write(data_string)

    imgname = json_file_path[:-4] + "png"  # remove the .json and add jpg
    orig_img_path = f"{dataset_path}/{imgname}"
    output_img_path = f"{output_data_path}/{imgname}"
    shutil.copy(orig_img_path, output_img_path)
