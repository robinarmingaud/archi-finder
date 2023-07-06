import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
import cv2

import win32gui,win32process
import win32ui
from ctypes import windll
from PIL import Image

# Make program aware of DPI scaling
user32 = windll.user32
user32.SetProcessDPIAware()
window_name = None

def get_window_name(hwnd, ctx):
    if win32gui.IsWindowVisible( hwnd ) and 'Lillia-Simp' in win32gui.GetWindowText(hwnd):
        global window_name
        window_name = win32gui.GetWindowText(hwnd)

win32gui.EnumWindows(get_window_name, None)



hwnd = win32gui.FindWindow(None, window_name)
# Get window bounds
left, top, right, bot = win32gui.GetWindowRect(hwnd)
w = right - left
h = bot - top

def get_coordinates(hwnd):
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    bmp_info = saveBitMap.GetInfo()
    bmp_str = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    im = im.crop((3, 69, 260,110  ))

    text=pytesseract.image_to_string(im)
    text = text.split(',')
    x,y = int(text[0]), int(text[1])
    
    
    return x,y

print(get_coordinates(hwnd))

def search_for_archi(hwnd):
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    bmp_info = saveBitMap.GetInfo()
    bmp_str = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmp_info['bmWidth'], bmp_info['bmHeight']),
        bmp_str, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im.save("test.png")    


search_for_archi(hwnd)