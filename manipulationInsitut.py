#coding : "utf-8"
import pyautogui

def selection_etage():
    try :
        for win in pyautogui.getAllWindows():
            if "InSitu" in win.title:
                win.activate()
    except Exception as e:
        print(e)
        exit(1)

    pyautogui.hotkey('alt','t','s')
    for _ in range(3):
        pyautogui.press("down")

    pyautogui.moveTo(260,360)
    pyautogui.click()


