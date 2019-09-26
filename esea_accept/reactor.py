import pyautogui
import sys
import time
import cv2
import numpy as np
import mss
import imutils

BASE_SCALING = 0.25


def main():
    react("argus.png")


def react(template_path):
    templates = generate_templates(template_path)
    with mss.mss() as sct:
        while True:
            # start = time.process_time()
            coords = locate_fast_dpi_aware(sct, templates)
            # print(time.process_time() - start)
            if coords is not None:
                pyautogui.click(*coords)
                break
            time.sleep(1)

        # print("Clicked!")


def locate(image):
    try:
        return pyautogui.locateCenterOnScreen(image)
    except TypeError:
        return None


def generate_templates(filename):
    template_raw = cv2.imread(filename, 0)

    templates = []
    # Template scaling
    for dpi_scale in [0.5, 0.625, 0.75, 0.875, 1]:
        template = imutils.resize(
            template_raw, width=int(template_raw.shape[1] * BASE_SCALING * dpi_scale)
        )
        template.shape[::-1]
        templates.append((template, dpi_scale))

    return templates


def locate_fast_dpi_aware(sct, templates, precision=0.7):
    # Screenshot
    im = sct.grab(sct.monitors[0])

    # Pre-process
    img_rgb = np.array(im)
    img_rgb = imutils.resize(img_rgb, width=int(img_rgb.shape[1] * BASE_SCALING))
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Template scaling
    for template, dpi_scale in templates:

        # Matching
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val > precision:
            # print(max_val, dpi_scale)
            x, y = [int(c / BASE_SCALING) for c in max_loc]
            height, width = [int(d / BASE_SCALING) for d in template.shape]
            return x + (width / 2), y + (height / 2)

    return None


if __name__ == "__main__":
    sys.exit(main())
