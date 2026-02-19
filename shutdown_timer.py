import customtkinter as ctk
import os
import time
import threading
from datetime import datetime, timedelta

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ShutdownApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(" 自动关机助手 ")
        self.geometry("400x450") # Increased height to prevent cramping
        self.resizable(False, False)

        self.shutdown_thread = None
        self.is_running = False
        self.stop_event = threading.Event()
        self.total_seconds = 0 

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Header
        self.grid_rowconfigure(1, weight=0) # Tabs - Fixed height
        self.grid_rowconfigure(2, weight=0) # Progress
        self.grid_rowconfigure(3, weight=0) # Buttons
        self.grid_rowconfigure(4, weight=1) # Status

        # Header
        self.header_label = ctk.CTkLabel(self, text="系统定时关机", font=ctk.CTkFont(family="Microsoft YaHei UI", size=26, weight="bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 15))

        # Tab View
        # Increased height to 180 to comfortably fit all content without resizing
        self.tab_view = ctk.CTkTabview(self, width=340, height=180, corner_radius=10)
        self.tab_view.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        self.tab_time = self.tab_view.add("按时刻关机")
        self.tab_countdown = self.tab_view.add("倒计时关机")

        # --- Tab 1: By Time ---
        self.setup_time_tab()

        # --- Tab 2: Countdown ---
        self.setup_countdown_tab()

        # Progress Bar
        self.progressbar = ctk.CTkProgressBar(self, width=320, height=12, corner_radius=6)
        self.progressbar.grid(row=2, column=0, padx=20, pady=(10, 20))
        self.progressbar.set(0)

        # Control Buttons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.start_btn = ctk.CTkButton(self.btn_frame, text="开始任务", command=self.start_timer, width=140, height=45, 
                                       font=ctk.CTkFont(family="Microsoft YaHei UI", size=15, weight="bold"),
                                       corner_radius=8)
        self.start_btn.pack(side="left", padx=10)

        self.cancel_btn = ctk.CTkButton(self.btn_frame, text="取消任务", command=self.cancel_timer, width=140, height=45, 
                                        fg_color="#D32F2F", hover_color="#B71C1C", state="disabled",
                                        font=ctk.CTkFont(family="Microsoft YaHei UI", size=15, weight="bold"),
                                        corner_radius=8)
        self.cancel_btn.pack(side="right", padx=10)

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="准备就绪", text_color="gray", font=ctk.CTkFont(family="Microsoft YaHei UI", size=14))
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 20))

    def setup_time_tab(self):
        self.tab_time.grid_columnconfigure((0, 1, 2), weight=1)
        self.tab_time.grid_rowconfigure(0, weight=1)
        self.tab_time.grid_rowconfigure(1, weight=1)

        font_entry = ctk.CTkFont(family="Arial", size=30, weight="bold")
        
        # Standardized height 50
        self.hour_entry = ctk.CTkEntry(self.tab_time, width=70, height=50, placeholder_text="23", justify="center", font=font_entry)
        self.hour_entry.grid(row=0, column=0, padx=5, pady=25)
        
        ctk.CTkLabel(self.tab_time, text=":", font=font_entry).grid(row=0, column=1)
        
        self.minute_entry = ctk.CTkEntry(self.tab_time, width=70, height=50, placeholder_text="00", justify="center", font=font_entry)
        self.minute_entry.grid(row=0, column=2, padx=5, pady=25)

        self.time_info_label = ctk.CTkLabel(self.tab_time, text="请输入24小时制时间", font=ctk.CTkFont(family="Microsoft YaHei UI", size=12))
        self.time_info_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))


    def setup_countdown_tab(self):
        self.tab_countdown.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.tab_countdown.grid_rowconfigure(0, weight=1)

        font_cd = ctk.CTkFont(family="Arial", size=30, weight="bold") # Increased to match Tab 1
        
        # Increased width to 70 to match Tab 1
        self.cd_hour = ctk.CTkEntry(self.tab_countdown, width=70, height=50, placeholder_text="0", justify="center", font=font_cd)
        self.cd_hour.grid(row=0, column=0, padx=2, pady=30)
        ctk.CTkLabel(self.tab_countdown, text="时", font=ctk.CTkFont(size=14)).grid(row=0, column=1)

        self.cd_min = ctk.CTkEntry(self.tab_countdown, width=70, height=50, placeholder_text="0", justify="center", font=font_cd)
        self.cd_min.grid(row=0, column=2, padx=2, pady=30)
        ctk.CTkLabel(self.tab_countdown, text="分", font=ctk.CTkFont(size=14)).grid(row=0, column=3)

        self.cd_sec = ctk.CTkEntry(self.tab_countdown, width=70, height=50, placeholder_text="0", justify="center", font=font_cd)
        self.cd_sec.grid(row=0, column=4, padx=2, pady=30)
        ctk.CTkLabel(self.tab_countdown, text="秒", font=ctk.CTkFont(size=14)).grid(row=0, column=5)

    def get_target_time(self):
        mode = self.tab_view.get()
        now = datetime.now().replace(microsecond=0)

        if mode == "按时刻关机":
            try:
                h_str = self.hour_entry.get()
                m_str = self.minute_entry.get()
                
                if not h_str or not m_str: return None
                
                h = int(h_str)
                m = int(m_str)
                if not (0 <= h <= 23 and 0 <= m <= 59):
                    raise ValueError
                
                target = now.replace(hour=h, minute=m, second=0)
                if target <= now:
                    target += timedelta(days=1) # tomorrow
                return target
            except ValueError:
                return None

        elif mode == "倒计时关机":
            try:
                h = int(self.cd_hour.get() or 0)
                m = int(self.cd_min.get() or 0)
                s = int(self.cd_sec.get() or 0)
                
                if h == 0 and m == 0 and s == 0:
                    return None
                    
                delta = timedelta(hours=h, minutes=m, seconds=s)
                return now + delta
            except ValueError:
                return None
        return None

    def start_timer(self):
        target_time = self.get_target_time()
        if not target_time:
            self.status_label.configure(text="请输入有效的时间！", text_color="#D32F2F")
            return

        self.is_running = True
        self.stop_event.clear()
        
        # Calculate total seconds for progress bar
        now = datetime.now().replace(microsecond=0)
        self.total_seconds = (target_time - now).total_seconds()
        self.progressbar.set(0) # Start empty or full? Let's say fills up. No, usually depletes or fills. Let's make it fill.
        
        # UI updates
        self.start_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.set_inputs_state("disabled")

        self.shutdown_thread = threading.Thread(target=self.run_timer, args=(target_time,))
        self.shutdown_thread.start()

    def set_inputs_state(self, state):
        self.hour_entry.configure(state=state)
        self.minute_entry.configure(state=state)
        self.cd_hour.configure(state=state)
        self.cd_min.configure(state=state)
        self.cd_sec.configure(state=state)

    def run_timer(self, target_time):
        while not self.stop_event.is_set():
            now = datetime.now().replace(microsecond=0)
            remaining = target_time - now
            rem_seconds = remaining.total_seconds()
            
            if rem_seconds <= 0:
                self.perform_shutdown()
                break
            
            # Update Progress
            if self.total_seconds > 0:
                progress = 1 - (rem_seconds / self.total_seconds)
                self.progressbar.set(progress)

            # Update status (Check stop_event again to avoid race condition overwriting 'Cancelled' message)
            if not self.stop_event.is_set():
                self.status_label.configure(text=f"关机倒计时: {remaining}", text_color="#388E3C")
            
            time.sleep(0.5)

    def perform_shutdown(self):
        if not self.stop_event.is_set():
            self.progressbar.set(1)
            self.status_label.configure(text="系统即将关机！(60秒撤销期)", text_color="#D32F2F")
            # Execute shutdown command with 60s delay
            os.system("shutdown /s /t 60")
            
            # Allow user to abort
            self.cancel_btn.configure(text="撤销关机 (Abort)", state="normal", fg_color="#E65100", hover_color="#EF6C00")
            self.start_btn.configure(state="disabled")
            self.is_running = True 

    def cancel_timer(self):
        # Always try to abort system shutdown
        os.system("shutdown /a")
        
        self.stop_event.set()
        self.is_running = False
        self.progressbar.set(0)
        
        # UI Reset
        self.start_btn.configure(state="normal")
        self.cancel_btn.configure(text="取消任务", state="disabled", fg_color="#D32F2F", hover_color="#B71C1C")
        self.set_inputs_state("normal")
        
        self.status_label.configure(text="当前无关机任务", text_color="gray")

if __name__ == "__main__":
    app = ShutdownApp()
    app.mainloop()
