import pyautogui
import sys
import time
from esea_accept import imagesearch

def main():
    while True:
        coords = locate("findmatch.png")
        if coords is not None:
            x, y = coords
            pyautogui.click(x, y)
            break
        time.sleep(2)

    print("Clicked!")

def locate(image):
    try:
        return pyautogui.locateCenterOnScreen(image)  
    except TypeError:
        return None
    

if __name__ == "__main__":
    sys.exit(main())

