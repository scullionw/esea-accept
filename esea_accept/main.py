import pyautogui
import sys
import time
import cv2
import numpy as np
import imutils


def main():
    while True:
        start = time.process_time()
        coords = locate_fast_scale_invariant("argus.png")
        print(time.process_time() - start)
        if coords is not None:
            x, y = coords
            pyautogui.click(x, y)
            break
        # time.sleep(2)

    print("Clicked!")


def locate(image):
    try:
        return pyautogui.locateCenterOnScreen(image)
    except TypeError:
        return None


def locate_fast(image):
    pos = imagesearch(image)
    if pos[0] != -1:
        return get_center(pos, image)
    else:
        return None


def locate_fast_scale_invariant(image):
    pos = imagesearch_scale_invariant(image)
    if pos[0] != -1:
        return get_center(pos, image)
    else:
        return None


def get_center(pos, image):
    img = cv2.imread(image)
    height, width, _ = img.shape
    x, y = pos[0] + (width / 2), pos[1] + (height / 2)
    return x, y


def imagesearch(image, precision=0.8):
    im = pyautogui.screenshot()

    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    template.shape[::-1]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc


def imagesearch_scale_invariant(image, precision=0.9, base_scaling=0.05):
    # Screenshot
    im = pyautogui.screenshot()

    img_rgb = np.array(im)
    img_rgb = imutils.resize(img_rgb, width=int(img_rgb.shape[1] * base_scaling))
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Template
    template = cv2.imread(image, 0)
    template = imutils.resize(template, width=int(template.shape[1] * base_scaling))
    template.shape[::-1]

    # Matching
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < precision:
        return [-1, -1]

    print(max_val)
    return [int(c / base_scaling) for c in max_loc]


if __name__ == "__main__":
    sys.exit(main())

