import threading
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import random
import requests
import time
import wx
import wx.xrc
import wx.dataview
import wx.lib.scrolledpanel as scrolled
# 匯入自行建立的wxpython GUI
from GUI_wxpython_1 import MyFormMain

class ComicDownloader(MyFormMain):

    def __init__(self, parent):
        super().__init__(parent)
                
        # Initialize variables
        self.driver = None
        self.chapters = []
        self.button_ids = []
        self.chapter_id = None
        self.chapter_text = None
        self.text = None
        self.collected_images = set()
        self.chapter_window = None  # Track the popup window
        self.chapter_checks = []
        self.title = None
        self.selected_chapters = []
        self.save_path = None
        # 保存佇列資料
        self.queue_data = []  # 每個項目是一個字典，包含漫畫名稱、集數和儲存路徑
        self.comicfolder_name = None
        self.chapterfolder_name = None
        self.current_save_path = None
        self.soup = None
        self.self_chapters = None
        self.is_paused = False  # 用於控制是否暫停下載
        self.pause_event = threading.Event()  # 用於暫停與續傳控制
        self.pause_event.set()  # 初始化為非暫停狀態
        self.task_status = []  # 每個任務的狀態
        self.task_index = None
        self.i = None
        
        #瀏覽器隱形
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)

    def start_analyze(self, event):
        url = self.URL.GetValue().strip()
        if not url:
            self.log_message("Error, Please enter a URL.\n")
            return
        
        self.log_message("開始分析...\n")

#         threading.Thread(target=self.analyze_chapters, args=(url,)).start() # 無法使用threading會導致彈出視窗馬上被關閉
#     def analyze_chapters(self, url):

        # Close any existing popup window
        if hasattr(self, 'chapter_window') and self.chapter_window and self.chapter_window.IsShown():
            self.chapter_window.Destroy()
            
        self.driver.get(url)
        self.soup = BeautifulSoup(self.driver.page_source, "lxml")
      
        # Clear old data
        self.chapters.clear()
        # Find chapter links
        chapter_links = self.soup.find_all('a', id=re.compile(r'.*'), class_="Vol eps_a d-block") + self.soup.find_all('a', id=re.compile(r'.*'), class_="Ch eps_a d-block")

        for chapter in chapter_links:
            chapter_id = chapter['id']
            self.chapter_text = chapter.text.strip()
            self.chapters.append((chapter_id, self.chapter_text))
            self.log_message(f"找到章節: {self.chapter_text}\n")

        self.log_message("章節分析完畢\n")
        self.show_chapter_popup()
       
    def add_to_queue(self, event):
        threading.Thread(target=self.add_to_queue_1).start()
        
    def add_to_queue_1(self):
        # 檢查是否解析過網頁
        if not self.soup or not self.save_path:
            wx.MessageBox("Please analyze comic and set save path first!", "Warning")
            return

        #檢查操作是否正確
        comic_name = getattr(self, "current_comic_name")
        chapters = getattr(self, "selected_chapters")
        self.self_chapters = getattr(self, "chapters")

        # 將任務新增至資料列表
        for Chapter in chapters:
            self.task_index = len(self.queue_data)  # 動態生成索引
            for item in self.chapters:
                if Chapter in item:
                    self.queue_data.append(
                        {"task_index": self.task_index,
                         "Comic Name": comic_name,
                         "Chapter": Chapter,
                         "Save Path": self.save_path,
                         "Chapter_id": item[0],
                         "progress": "0%",  # 初始值為0 , 這個功能未顯示
                         "status": "Pending",  # 默認為 Pending
                         }
                        )
                    self.task_status.append("Ready")
                    self.queue_table.AppendItem([comic_name, Chapter, self.save_path, "Ready", 0])
               
    def Start_1(self, event):
        threading.Thread(target=self.start_download_1).start()

    def start_download_1(self):
        """开始下载佇列中的任务"""
        if not self.queue_data:
            wx.MessageBox("No tasks in the queue to download!", "Warning")
            return

        #進度條設定
        self.Total_Process.SetValue(0) # 重新歸0
        Total_tasks = len(self.queue_data)
        
        # 從佇列中一個一個取出任務的必要訊息
#         while self.queue_data:
        for self.i, task in enumerate(self.queue_data):
            # 檢查是否暫停
            # 如果暫停，會在這裡等待
            self.pause_event.wait()  
            # 如果是己完成的任務,則略過
            if self.task_status[self.i] == "Completed": 
                continue
            self.task_status[self.i] = "Running"
            self.update_task_status(self.i)
            
#             task = self.queue_data.pop(0), 本來想用FIFO來做, 先comment掉以後再想想
            self.comicfolder_name = task["Comic Name"]
            self.chapterfolder_name = task["Chapter"]
            self.current_save_path = task["Save Path"]
            self.selected_ID = task["Chapter_id"]
            # 開始下載
            try:
                self.download_selected_chapters()
                self.Total_Process.SetValue( int((self.i+1)/Total_tasks*100) )
            except Exception as e:
                self.log_message(f"任務失敗: {e}\n")
                self.task_status[self.i] = "Error"
            self.task_status[self.i] = "Completed"
            self.update_task_status(self.i)            
        self.log_message("*****全部下載完成*****\n")


    def download_selected_chapters(self):
        #檢查self.selected_chapters是否為空
        if not self.selected_chapters:
            wx.MessageBox("No Selection", "Please select at least one chapter.")
            return

        self.chapter_id = self.selected_ID
        self.text = self.chapterfolder_name
        # Fetch images for chapter
        self.fetch_images_for_chapter()
        # Download images
        self.log_message(f"開始下載:{self.comicfolder_name}_{self.text}的圖片\n")
        self.download_images()
        self.log_message("="*20+"\n")
        self.log_message(f"{self.comicfolder_name}_{self.text}下載完成\n")

    def fetch_images_for_chapter(self):
        self.log_message("準備下載中,請稍待\n")
        # Clear for new chapter
        self.collected_images.clear()  
        self.driver.get(self.URL.GetValue().strip())
        soup = BeautifulSoup(self.driver.page_source, "lxml")
        self.title = soup.find('li', class_="h2 mb-1")
        time.sleep(random.random())
        
        button = self.driver.find_element(By.ID, self.chapter_id)
        button.click()
        time.sleep(random.random())

        
        while True:
            soup = BeautifulSoup(self.driver.page_source, "lxml")
            img_tags = soup.find_all('img', src=re.compile(r'.*'))

            for img in img_tags:
                img_url = img['src']
                if img_url not in self.collected_images:
                    self.collected_images.add(img_url)

            self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(random.random())

            new_height = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height >= total_height:
                self.log_message(f"章節 {self.text} 圖片搜尋完成\n")
                break

    def download_images(self):
        # 設定資料夾
        # 如果有指定路徑
        if self.current_save_path:
            save_folder = f"{self.current_save_path}/{self.comicfolder_name}/{self.chapterfolder_name}"
        # 如果沒有指定路徑
        else:
            save_folder = f"./{self.comicfolder_name}/{self.chapterfolder_name}"
        os.makedirs(save_folder, exist_ok=True)
        self.log_message(f"開始下載{self.text}\n")
        # 設定進度條
        total_images = len(self.collected_images)
        
        for idx, img_url in enumerate(self.collected_images):
            # 檢查是否暫停
            self.pause_event.wait()  # 如果暫停，會在這裡等待
            img_name = img_url.split("/")[-1]
            formatted_name = re.sub(r'(_[a-zA-Z0-9]+)?\.jpg$', '.jpg', img_name)
            img_path = os.path.join(save_folder, formatted_name)
            full_url = "https:" + img_url
            
            try:
                response = requests.get(full_url)
                with open(img_path, "wb") as file:
                    file.write(response.content)
                self.log_message(f"下載成功: {formatted_name}\n")
                progress = int(((idx+1) / total_images) * 100)
                # 更新進度條
                self.queue_table.SetValue(progress, self.i, 4)
             
            except Exception as e:
                self.log_message(f"下載失敗: {formatted_name}，錯誤: {e}\n")

    def delete_task(self):
        """刪除選中的佇列任務"""
        selected_item = self.queue_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a task to delete!")
            return

        for item in selected_item:
            index = self.queue_table.index(item)
            del self.queue_data[index]  # 刪除對應佇列的資料
            self.queue_table.delete(item)  # 刪除表格中的顯示

        self.log_message("Selected task(s) deleted.\n")

    def pause_task(self):
        """暫停佇列下載"""
        if self.is_paused:
            wx.MessageBox("Download is already paused.", "Info")
            return

        self.is_paused = True
        self.pause_event.clear()  # 暫停執行緒
        self.log_message("Download paused.\n")

    def resume_task(self):
        """續傳佇列下載"""
        if not self.is_paused:
            wx.MessageBox("Download is not paused.", "Info")
            return

        self.is_paused = False
        self.pause_event.set()  # 通知執行緒繼續
        self.log_message("Download resumed.\n")

    def update_task_status(self, task_index):
        """更新任務狀態"""
        self.queue_table.SetValue(self.task_status[task_index], self.i, 3)
        
    def on_confirm_selection(self, event):
        # 對wxpython而言下列動作必需在self.chapter_window.Destroy()前做完
        # 建立己選話數清單
        self.selected_chapters = [text for chk, text in self.chapter_checks if chk.GetValue()]# text for chk, text in self.chapter_checks if chk.GetValue()
        for selected_chapter in self.selected_chapters:
            self.log_message(f"Selected Chapters:{selected_chapter}\n")
        # submmit必需清空,避免下次疊加
        self.chapter_checks = [] 
        
        # 捉取漫畫名稱
        self.title = self.soup.find('li', class_="h2 mb-1")
        #只要字符串中的中文，字母，数字
        comicfolder_name = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',self.title.text,re.S)   
        comicfolder_name = "".join(comicfolder_name)
        self.current_comic_name = comicfolder_name
        self.log_message(f"Selected Comic:{comicfolder_name}\n") 
        self.chapter_window.Destroy()

if __name__ == "__main__":

    app = wx.App(False)
    frame = ComicDownloader(None)
    frame.Fit()
    frame.Show()
    app.MainLoop()

