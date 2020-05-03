import os, sys, shutil, glob, re, json, tqdm, cv2


def convert_format(origin, img_list_output_file):
    with open(origin, "r") as f:
        lines = f.readlines()

    if not os.path.exists("labels"):
        os.makedirs("labels")

    with open("{}.txt".format(img_list_output_file), "w") as img_list_file:
        for line in tqdm.tqdm(lines):
            v = line.split()
            img_path = v[1]
            img_id = img_path.split("/")[-1]
            width, height = float(v[2]), float(v[3])

            img_list_file.write("data/custom/images/{}\n".format(img_id))

            with open("labels/{}.txt".format(img_id.split(".")[0]), "w") as box_file:
                for idx in range(4, len(v), 5):
                    b = v[idx: idx+5]
                    label, x1, y1, x2, y2 = [int(x) for x in b]

                    xc, yc, w, h = float(x1+(x2-x1)/2), float(y1+(y2-y1)/2), float(x2-x1), float(y2-y1)
                    xc, yc, w, h = xc/width, yc/height, w/width, h/height
                    assert(0<=xc<=1 and 0<=yc<=1 and 0<=w<=1 and 0<=h<=1)

                    # need verity coordinates, need swap x & y?
                    box_file.write("{} {} {} {} {}\n".format(label, xc, yc, w, h))


if os.path.exists("labels"):
    shutil.rmtree("labels")
convert_format("tf_format_dataset/train.txt", "train")
convert_format("tf_format_dataset/test.txt", "valid")
