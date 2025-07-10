import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
import final_menu 
import final_UCL
import final_world_cup
import os
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sqlite3

class MainMenuWindow(QMainWindow, final_menu.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.exit_button.clicked.connect(self.close)
        
        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.handle_media_status)
        
        self.songs = {
            "Y QUE FUE": "Y_QUE_FUE.mp3",
            "Wavin Flag": "wavin_flag.mp3",
            "Waka Waka": "waka_waka.mp3",
            "UCL Song": "UCL_song.mp3",
            "Spageti Mafia": "spageti_mafia.mp3",
            "Ole Ole": "ole_ole.mp3",
            "Ibra Song": "ibra_song.mp3",
            "Cup of Life": "cup_of_life.mp3"
        }
        
        self.setup_music_dropdown()
        
        self.current_song = "Y QUE FUE"
        self.load_and_play_song(self.current_song)
        
        self.mute_radio_button.toggled.connect(self.toggle_mute)
        
        self.UCL_button.clicked.connect(self.open_ucl)
        self.world_cup_button.clicked.connect(self.open_world_cup)
    
    def setup_music_dropdown(self):
        self.music_dropbox.addItems(self.songs.keys())
        
        self.music_dropbox.setCurrentText("Y QUE FUE")
        
        self.music_dropbox.currentTextChanged.connect(self.change_song)
    
    def change_song(self, song_name):
        if song_name in self.songs:
            self.current_song = song_name
            self.load_and_play_song(song_name)
    
    def load_and_play_song(self, song_name):
        song_file = self.songs.get(song_name)
        if song_file:
            path = os.path.join(os.getcwd(), song_file)
            url = QUrl.fromLocalFile(path)
            self.player.setMedia(QMediaContent(url))
            self.player.setVolume(50)
            self.player.play()
            self.music_dropbox.setCurrentText(song_name)
        
    def handle_media_status(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.player.setPosition(1200)
            self.player.play()
        elif status == QMediaPlayer.EndOfMedia:
            self.player.setPosition(1200)
            self.player.play()
    
    def toggle_mute(self):
        if self.mute_radio_button.isChecked():
            self.player.setVolume(0)
        else:
            self.player.setVolume(50)
    
    def open_ucl(self):
        self.ucl_window = UCLWindow(self.player, self)
        self.ucl_window.show()
        self.hide()
    
    def open_world_cup(self):
        self.world_cup_window = WorldCupWindow(self.player, self)
        self.world_cup_window.show()
        self.hide()


class UCLWindow(QMainWindow, final_UCL.Ui_MainWindow):
    def __init__(self, player, main_window):
        super().__init__()
        self.setupUi(self)
        self.player = player
        self.main_window = main_window
        
        self.previous_song = main_window.current_song
        
        self.load_and_play_song("UCL Song")
        self.back_button.clicked.connect(self.go_back)
        self.mute_radio_button.toggled.connect(self.toggle_mute)
        
        self.setup_database()
        self.display_data()
        
        self.add_button.clicked.connect(self.add_record)
        self.update_button.clicked.connect(self.update_record)
        self.delete_button.clicked.connect(self.delete_record)
    
    def setup_database(self):
        self.conn = sqlite3.connect('ucl_data.sqlite3')
        self.cursor = self.conn.cursor()
        
    def display_data(self):
        self.listWidget.clear()
        
        self.cursor.execute("SELECT * FROM champions_league ORDER BY year")
        records = self.cursor.fetchall()
        
        header = QListWidgetItem("Year  |  Winner  |  Top Goalscorer  |  Top Assistant  |  Best Manager")
        self.listWidget.addItem(header)
        
        for record in records:
            year, winner, top_goalscorer, top_assistant, best_manager = record
            item_text = f"{year}  |  {winner}  |  {top_goalscorer}  |  {top_assistant}  |  {best_manager}"
            item = QListWidgetItem(item_text)
            self.listWidget.addItem(item)
    
    def update_record(self):
        selected_item = self.listWidget.currentItem()
        if selected_item and not selected_item.text().startswith("Year"):
            year = int(selected_item.text().split('|')[0].strip())
            winner = self.winner_line_Edit.text().strip()
            top_goalscorer = self.top_scorrer_line_Edit.text().strip()
            top_assistant = self.top_assistman_line_Edit.text().strip()
            best_manager = self.bes_manager_line_Edit.text().strip()
            
            if winner and top_goalscorer and top_assistant and best_manager:
                try:
                    self.cursor.execute(
                        "UPDATE champions_league SET winner=?, top_goalscorer=?, top_assistant=?, best_manager=? WHERE year=?",
                        (winner, top_goalscorer, top_assistant, best_manager, year)
                    )
                    self.conn.commit()
                    self.display_data()
                    
                    self.winner_line_Edit.clear()
                    self.top_scorrer_line_Edit.clear()
                    self.top_assistman_line_Edit.clear()
                    self.bes_manager_line_Edit.clear()
                    
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
    
    def delete_record(self):
        selected_item = self.listWidget.currentItem()
        if selected_item and not selected_item.text().startswith("Year"):
            year = int(selected_item.text().split('|')[0].strip())
            
            try:
                self.cursor.execute("DELETE FROM champions_league WHERE year=?", (year,))
                self.conn.commit()
                self.display_data()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
    
    def load_and_play_song(self, song_name):
        song_file = self.main_window.songs.get(song_name)
        if song_file:
            path = os.path.join(os.getcwd(), song_file)
            url = QUrl.fromLocalFile(path)
            self.player.setMedia(QMediaContent(url))
            self.player.setVolume(50)
            self.player.play()
    
    def toggle_mute(self):
        if self.mute_radio_button.isChecked():
            self.player.setVolume(0)
        else:
            self.player.setVolume(50)
    
    def go_back(self):
        self.main_window.load_and_play_song(self.previous_song)
        self.main_window.show()
        self.close()
        
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

    def add_record(self):
        winner = self.winner_line_Edit.text().strip()
        top_goalscorer = self.top_scorrer_line_Edit.text().strip()
        top_assistant = self.top_assistman_line_Edit.text().strip()
        best_manager = self.bes_manager_line_Edit.text().strip()
        
        if not all([winner, top_goalscorer, top_assistant, best_manager]):
            return
        
        self.cursor.execute("SELECT MAX(year) FROM champions_league")
        max_year = self.cursor.fetchone()[0]
        year = max_year + 1 if max_year else 2025  
        
        try:
            self.cursor.execute(
                "INSERT INTO champions_league (year, winner, top_goalscorer, top_assistant, best_manager) VALUES (?, ?, ?, ?, ?)",
                (year, winner, top_goalscorer, top_assistant, best_manager)
            )
            self.conn.commit()
            
            self.display_data()
            
            self.winner_line_Edit.clear()
            self.top_scorrer_line_Edit.clear()
            self.top_assistman_line_Edit.clear()
            self.bes_manager_line_Edit.clear()
            
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")



class WorldCupWindow(QMainWindow, final_world_cup.Ui_MainWindow):
    def __init__(self, player, main_window):
        super().__init__()
        self.setupUi(self)
        self.player = player
        self.main_window = main_window
        
        self.previous_song = main_window.current_song

        self.load_and_play_song("Waka Waka")
        self.back_button.clicked.connect(self.go_back)
        self.mute_radio_button.toggled.connect(self.toggle_mute)
        
        self.setup_database()
        self.display_data()
        
        self.add_button.clicked.connect(self.add_record)
        self.update_button.clicked.connect(self.update_record)
        self.delete_button.clicked.connect(self.delete_record)
    
    def setup_database(self):
        self.conn = sqlite3.connect('WC_data.sqlite3')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS world_cup
                             (year INTEGER PRIMARY KEY,
                              winner TEXT,
                              top_goalscorer TEXT,
                              top_assistant TEXT,
                              best_manager TEXT)''')
        self.conn.commit()
        
    def display_data(self):
        self.listWidget.clear()
        
        self.cursor.execute("SELECT * FROM world_cup ORDER BY year")
        records = self.cursor.fetchall()
        
        header = QListWidgetItem("Year  |  Winner  |  Top Goalscorer  |  Top Assistant  |  Best Manager")
        self.listWidget.addItem(header)
        
        for record in records:
            year, winner, top_goalscorer, top_assistant, best_manager = record
            item_text = f"{year}  |  {winner}  |  {top_goalscorer}  |  {top_assistant}  |  {best_manager}"
            item = QListWidgetItem(item_text)
            self.listWidget.addItem(item)
    
    def add_record(self):
        winner = self.winner_line_Edit.text().strip()
        top_goalscorer = self.top_scorrer_line_Edit.text().strip()
        top_assistant = self.top_assistman_line_Edit.text().strip()
        best_manager = self.bes_manager_line_Edit.text().strip()
        
        if not all([winner, top_goalscorer, top_assistant, best_manager]):
            return
        
        self.cursor.execute("SELECT MAX(year) FROM world_cup")
        max_year = self.cursor.fetchone()[0]
        year = max_year + 4 if max_year else 2026  
        
        try:
            self.cursor.execute(
                "INSERT INTO world_cup (year, winner, top_goalscorer, top_assistant, best_manager) VALUES (?, ?, ?, ?, ?)",
                (year, winner, top_goalscorer, top_assistant, best_manager)
            )
            self.conn.commit()
            
            self.display_data()
            
            self.winner_line_Edit.clear()
            self.top_scorrer_line_Edit.clear()
            self.top_assistman_line_Edit.clear()
            self.bes_manager_line_Edit.clear()
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
    
    def update_record(self):
        selected_item = self.listWidget.currentItem()
        if selected_item and not selected_item.text().startswith("Year"):
            year = int(selected_item.text().split('|')[0].strip())
            
            winner = self.winner_line_Edit.text().strip()
            top_goalscorer = self.top_scorrer_line_Edit.text().strip()
            top_assistant = self.top_assistman_line_Edit.text().strip()
            best_manager = self.bes_manager_line_Edit.text().strip()
            
            if winner and top_goalscorer and top_assistant and best_manager:
                try:
                    self.cursor.execute(
                        "UPDATE world_cup SET winner=?, top_goalscorer=?, top_assistant=?, best_manager=? WHERE year=?",
                        (winner, top_goalscorer, top_assistant, best_manager, year)
                    )
                    self.conn.commit()
                    self.display_data()
                    
                    self.winner_line_Edit.clear()
                    self.top_scorrer_line_Edit.clear()
                    self.top_assistman_line_Edit.clear()
                    self.bes_manager_line_Edit.clear()
                    
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
    
    def delete_record(self):
        selected_item = self.listWidget.currentItem()
        if selected_item and not selected_item.text().startswith("Year"):
            year = int(selected_item.text().split('|')[0].strip())
            
            try:
                self.cursor.execute("DELETE FROM world_cup WHERE year=?", (year,))
                self.conn.commit()
                self.display_data()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
    
    def load_and_play_song(self, song_name):
        song_file = self.main_window.songs.get(song_name)
        if song_file:
            path = os.path.join(os.getcwd(), song_file)
            url = QUrl.fromLocalFile(path)
            self.player.setMedia(QMediaContent(url))
            self.player.setVolume(50)
            self.player.play()
    
    def toggle_mute(self):
        if self.mute_radio_button.isChecked():
            self.player.setVolume(0)
        else:
            self.player.setVolume(50)
    
    def go_back(self):
        self.main_window.load_and_play_song(self.previous_song)
        self.main_window.show()
        self.close()
        
    def closeEvent(self, event):
        self.conn.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainMenuWindow()
    main_window.show()
    sys.exit(app.exec_())

