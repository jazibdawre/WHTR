import os
import cv2
from path import Path


def image_crop(x1, y1, x2, y2, image):
    crop = image[y1:y2, x1:x2]

    return crop


def split_lines(path: Path):
    # (1) read
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # (2) threshold
    th, threshed = cv2.threshold(
        gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU
    )

    # (3) minAreaRect on the nozeros
    pts = cv2.findNonZero(threshed)
    ret = cv2.minAreaRect(pts)

    (cx, cy), (w, h), ang = ret
    if w > h:
        w, h = h, w
        ang += 90

    # (4) Find rotated matrix, do rotation
    M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
    rotated = cv2.warpAffine(threshed, M, (img.shape[1], img.shape[0]))

    # (5) find and draw the upper and lower boundary of each lines
    hist = cv2.reduce(rotated, 1, cv2.REDUCE_AVG).reshape(-1)

    th = 2
    H, W = img.shape[:2]
    uppers = [y for y in range(H - 1) if hist[y] <= th and hist[y + 1] > th]
    lowers = [y for y in range(H - 1) if hist[y] > th and hist[y + 1] <= th]

    rotated = cv2.cvtColor(rotated, cv2.COLOR_GRAY2BGR)

    x1 = 0
    x2 = W
    for index, (y1, y2) in enumerate(zip(uppers, lowers)):
        line = image_crop(x1, y1, x2, y2, rotated)
        line = cv2.bitwise_not(line)

        os.makedirs(os.path.splitext(path)[0], exist_ok=True)
        cv2.imwrite(os.path.join(os.path.splitext(path)[0], f"{str(index)}.png"), line)
