try:
    import pyautogui
    import pyperclip
    import pygetwindow as gw
    
    import time
    import os
    import re
    import ctypes
    import logging
    
    # import pytesseract
    # from pytesseract import Output

    from paddleocr import PaddleOCR
    import numpy as np

    from my_logger import Logger

    def wake_up_screen():
        pyautogui.move(100, 100, duration=1)
        pyautogui.move(-100, -100, duration=1)
        time.sleep(6)
        

    def find_max_numbered_file(folder_path):
        files = os.listdir(folder_path)
        pattern = re.compile(r'auto_(\d+)\.log')

        max_number = -1
        for file in files:
            match = pattern.match(file)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number

        return max_number

    def get_stat_exit(log_path):
        # 读取log文件的最后一行并用弹窗打印，不能中文
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_line = lines[-1]
            ctypes.windll.user32.MessageBoxW(0, last_line, "alert", 0)
        exit()

    root_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_path)

    save_path = os.path.join(root_path, 'res')
    log_path = os.path.join(root_path, 'log')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if not os.path.exists(log_path):
        os.makedirs(log_path)


    screen_width, screen_height = pyautogui.size()  # 获取屏幕的尺寸
    ocr = PaddleOCR(use_gpu=False)

    title_name = 'qndxx'
    log_num = find_max_numbered_file(log_path) + 1
    log_name = f'auto_{log_num}.log'
    log_path = os.path.join(log_path, log_name)

    logger = Logger('my_logger', log_path)
    
    # pyautogui.FAILSAFE = False
    wake_up_screen()


    class WindowState:
        def __init__(self, title):
            self.window = gw.getWindowsWithTitle(title)[0]
            self.initial_size = self.window.size
            self.initial_topleft = self.window.topleft

        def restore(self):
            self.window.size = self.initial_size
            self.window.topleft = self.initial_topleft


    def drag_window_to_main_screen(window_title, window_id=0, resize=None): # windowid=0表示第一个活动窗口
        screen_width, screen_height = pyautogui.size()  # 获取屏幕的尺寸
        window = gw.getWindowsWithTitle(window_title)[window_id]
        window.moveTo(round(screen_width / 8), round(screen_height / 10))
        window.activate()
        if resize is not None:
            window.resizeTo(resize[0], resize[1])
        time.sleep(1)


    def click_image(image_path, sleep_time=1, confidence_score=0.7):
        location = pyautogui.locateOnScreen(
            image_path, confidence=confidence_score)
        if location is not None:
            center = pyautogui.center(location)
            pyautogui.click(center)
            time.sleep(sleep_time)
            return True
        else:
            return False


    def confirm_image(image_path, confidence_score=0.6):
        location = pyautogui.locateOnScreen(
            image_path, confidence=confidence_score)
        if location is not None:
            return True
        else:
            return False


    def get_image_location(image_path, confidence_score=0.7):
        location = pyautogui.locateOnScreen(
            image_path, confidence=confidence_score)
        if location is not None:
            return pyautogui.center(location)
        else:
            return None

    def ocr_t_in_text(image, text): # 输入image可以为PIL或者numpy
        image = np.array(image)
        # 使用OCR模型识别截图中的文本
        result = ocr.ocr(image)
        # 遍历结果，找到指定的字符串，并打印其位置坐标
        coordinate = None
        # logger.log(len(result))
        for line in result:  # 目前只支持一个长文本中一个目标字符串
            for res in line:
                if text == res[1][0]:
                    logger.log(res[1][0])
                    if res[1][1] > 0.8:
                        coordinate = [res[0][0][0], res[0][0][1],
                                    res[0][2][0], res[0][2][1]]
                        break
                    
        return coordinate


    def ocr_window_image(window_title, text, action='click', window_id=0):
        window = gw.getWindowsWithTitle(window_title)[window_id]
        screenshot = pyautogui.screenshot(region=(
            window.left, window.top, window.width, window.height))
        # screenshot.save('active_window.png')
        coordinate = None
        coordinate = ocr_t_in_text(screenshot, text)
        if coordinate != None:
            center_point = (round((coordinate[0]+coordinate[2])/2+window.left),
                            round((coordinate[1]+coordinate[3])/2+window.top))
            if action == 'click':
                pyautogui.click(center_point)
            return True
        else:
            return False
        
    def save_window_image(window_title, save_path, title='qndxx', window_id=0):
        window = gw.getWindowsWithTitle(window_title)[window_id]
        screenshot = pyautogui.screenshot(region=(
            window.left, window.top, window.width, window.height))
        file_name = title + '.png'
        save_path = os.path.join(save_path, file_name)
        screenshot.save(save_path)


    def xywh_to_xyxy(x, y, w, h):
        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        return x1, y1, x2, y2


    # 打开微信
    logger.log("start wechat")
    os.startfile('e:\WeChat\ProgramFiles\WeChat\WeChat.exe')
    time.sleep(2)
    wechat_state = WindowState('微信')

    # 主屏幕操作
    drag_window_to_main_screen('微信', resize=(1076, 631))

    # 点击登录按钮
    if not click_image('./img/login_button.png', 3):
        logger.log("not found login button")

    # 点击搜索框
    if not click_image('./img/search_button.png', 4):
        logger.log("not found search button")
    else:
        pyperclip.copy('辽宁共青团')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(1)

    # 点击学习平台
    if not click_image('./img/pingtai.png', 4):
        logger.log("not found pingtai")

    # 点击青年大学习
    if not click_image('./img/qndxx.png', 30):
        logger.log("not found qndxx")
        
    # 主屏幕操作
    drag_window_to_main_screen('微信', resize=(880, 802))


    # 点击同意
    if not click_image('./img/tongyi.png', 6):
        logger.log("not found tongyishouquan")

    # 点击学习
    if not click_image('./img/xuexi.png', 4, confidence_score=0.6):
        logger.log("not found xuexi")

    if confirm_image('./img/benqi.png', confidence_score=0.6) and confirm_image('./img/wangqi.png', confidence_score=0.6):
        benqi_location = get_image_location('./img/benqi.png')
        wangqi_location = get_image_location('./img/wangqi.png')
        logger.log(benqi_location)
        logger.log(wangqi_location)
        y_distance = abs(benqi_location[1]-wangqi_location[1])
        # logger.log(x_distance)
        
        if y_distance < 200:  # 两个按钮的x坐标差值小于40，说明两个坐标特别靠近，没有新一期，退出
            logger.log('no new period')
            pyautogui.hotkey('alt', 'f4')
            pyautogui.hotkey('alt', 'f4')
            wechat_state.restore()
            get_stat_exit(log_path)
        else:
            center_point = (round((benqi_location[0]+wangqi_location[0])/2),
                            round((benqi_location[1]+wangqi_location[1])/2))
            pyautogui.click(center_point)  # 点击新一期
            # pyautogui.click(wangqi_location[0], wangqi_location[1]+150)
            time.sleep(2)

            # 出现省份市级选择
            if not click_image('./img/qingxuanze1.png', 3):
                logger.log("not found qingxuanze1")
            else:
                qingxuanze1_location = get_image_location('./img/qingxuanze1.png')
                xuanze1_loc = [qingxuanze1_location[0],
                            qingxuanze1_location[1]+10]  # 此处10为offset
                pyautogui.moveTo(xuanze1_loc[0], xuanze1_loc[1], duration=0.1)
                pyautogui.click(xuanze1_loc[0], xuanze1_loc[1])
                pyautogui.moveTo(
                    xuanze1_loc[0], xuanze1_loc[1]+20, duration=0.1)  # 此处20为offset
                if not click_image('./img/liaoning.png', 2):  
                    for i in range(10):
                        pyautogui.scroll(-80)
                        if click_image('./img/liaoning.png', 2):
                            break
                    print('not found liaoning')
                        
                qingxuanze1_location = get_image_location('./img/qingxuanze2.png')
                xuanze1_loc = [qingxuanze1_location[0],
                            qingxuanze1_location[1]-10]  # 此处10为offset
                pyautogui.moveTo(xuanze1_loc[0], xuanze1_loc[1], duration=0.1)
                pyautogui.click(xuanze1_loc[0], xuanze1_loc[1])
                pyautogui.moveTo(
                    xuanze1_loc[0], xuanze1_loc[1]+20, duration=0.1)  # 此处20为offset
                if not click_image('./img/dalian.png', 1):
                    for i in range(10):
                        pyautogui.scroll(-80)
                        if click_image('./img/dalian.png', 1):
                            break
                
                # 点击确定
                if not click_image('./img/queding.png', 5):
                    logger.log("not found queding")
                    
            # 点击开始学习(ocr)
            time.sleep(6)
            if not ocr_window_image('微信', '我要签到', action='click'):
                logger.log("not found woyaoqiandao")
            time.sleep(4)
            if not ocr_window_image('微信', '开始学习', action='click'):
                logger.log("not found kaishixuexi")
            else:
                time.sleep(4)
                pyautogui.hotkey('alt', 'left')
                time.sleep(1)
                if not click_image('./img/geren.png', 7):
                    logger.log("not found geren")
                if not click_image('./img/xuexijilu.png', 5):
                    logger.log("not found xuexijilu")
                else:
                    save_window_image('微信', save_path, title=title_name)
                    pyautogui.hotkey('alt', 'f4')
                    pyautogui.hotkey('alt', 'f4')
                    logger.log("finished study")
                    
                    # 发送到指定群聊
                    time.sleep(1)
                    if not click_image('./img/search_button.png', 3):
                        print("not found search button")
                    else:
                        pyperclip.copy('计算机物联网第一支部')
                        pyautogui.hotkey('ctrl', 'v')
                        pyautogui.press('enter')
                        
                        # 打开图片
                        time.sleep(1)
                        pyperclip.copy('本期青年大学习已经开始，请大家完成后发送至群里，谢谢！')
                        pyautogui.hotkey('ctrl', 'v')
                        os.startfile(os.path.join(save_path, title_name+'.png'))
                        time.sleep(2)
                        pyautogui.hotkey('ctrl', 'c')
                        pyautogui.hotkey('alt', 'f4')
                        pyautogui.hotkey('ctrl', 'v') # 粘贴图片
                        
                        if click_image('./img/send_button.png', 1):
                            logger.log("fasongchenggong")
                    
        
        
        wechat_state.restore()
    else:
        logger.log("not found benqi or wangqi")
        
    get_stat_exit(log_path)

except Exception as e:
    logger.log(f"Error: {str(e)}", level=logging.ERROR)
    get_stat_exit(log_path)