import sys
import pandas as pd
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit)

class SpotifyAudioFeaturesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        # Load the CSV file without headers and assign column names manually
        self.data = pd.read_csv(r"C:\Users\agarw\Downloads\spotify_data(1).csv", header=None)
        self.data.columns = ['id', 'acousticness', 'danceability', 'duration_ms', 
                             'energy', 'instrumentalness', 'key', 'liveness', 
                             'loudness', 'mode', 'speechiness', 'tempo', 
                             'time_signature', 'valence', 'target', 
                             'song_title', 'artist']
        self.data['song_title'] = self.data['song_title'].str.strip()  # Remove leading/trailing spaces

    def initUI(self):
        self.setWindowTitle('Spotify Audio Features Finder by Song Title')
        
        # Set a larger window size
        self.resize(800, 600)

        # Set a background image related to Spotify
        self.setStyleSheet("background-color: #121212;")  # Default dark background
        self.background_image = QPixmap("spotify_background.jpg")  # Make sure to replace with actual image path
        
        layout = QVBoxLayout()
        
        self.label = QLabel('Enter Song Title:')
        self.label.setStyleSheet("color: #1DB954; font-size: 24px; font-weight: bold;")  # Larger green text for label
        layout.addWidget(self.label)
        
        self.song_name_input = QLineEdit(self)
        self.song_name_input.setStyleSheet("""
            background-color: #121212;
            color: white;
            border: 2px solid #1DB954;
            padding: 10px;
            font-size: 28px;
        """)  # Dark background with green border and white text, larger font
        layout.addWidget(self.song_name_input)
        
        self.search_button = QPushButton('Get Audio Features', self)
        self.search_button.setStyleSheet("""
            background-color: #1DB954;
            color: white;
            border: none;
            padding: 15px;
            font-size: 28px;
            border-radius: 5px;
        """)  # Green background for button with white text, larger font size
        self.search_button.clicked.connect(self.get_audio_features)
        layout.addWidget(self.search_button)
        
        self.result_area = QTextEdit(self)
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("""
            background-color: #121212;
            color: white;
            border: 1px solid #1DB954;
            padding: 15px;
            font-size: 20px;
        """)  # Dark background with white text and green border for result area, larger font
        layout.addWidget(self.result_area)
        
        self.setLayout(layout)

        # Animation for the result area (fade-in effect)
        self.fade_in_animation = QPropertyAnimation(self.result_area, b"opacity")
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw background image
        if not self.background_image.isNull():
            painter.drawPixmap(self.rect(), self.background_image)  # Stretch the background to fit the window

        super().paintEvent(event)  # Call the base class paintEvent

    def get_audio_features(self):
        try:
            song_title = self.song_name_input.text().strip()
            if song_title:
                # Check if the song title exists in the data (case-insensitive)
                matched_songs = self.data[self.data['song_title'].str.contains(song_title, case=False, na=False)]
                if not matched_songs.empty:
                    result_text = f"Audio Features for '{song_title}':\n"
                    for index, features in matched_songs.iterrows():
                        result_text += f"\nTrack ID: {features['id']}\n"
                        result_text += f"Acousticness: {features['acousticness']}\n"
                        result_text += f"Danceability: {features['danceability']}\n"
                        result_text += f"Duration (ms): {features['duration_ms']}\n"
                        result_text += f"Energy: {features['energy']}\n"
                        result_text += f"Instrumentalness: {features['instrumentalness']}\n"
                        result_text += f"Liveness: {features['liveness']}\n"
                        result_text += f"Loudness (dB): {features['loudness']}\n"
                        result_text += f"Tempo (BPM): {features['tempo']}\n"
                        result_text += f"Valence: {features['valence']}\n"
                        result_text += f"Artist: {features['artist']}\n"
                    self.result_area.setPlainText(result_text)
                    self.fade_in_animation.start()  # Start fade-in animation
                else:
                    self.result_area.setPlainText(f"Song '{song_title}' not found in the data.")
                    self.fade_in_animation.start()  # Start fade-in animation
            else:
                self.result_area.setPlainText("Please enter a valid song title.")
                self.fade_in_animation.start()  # Start fade-in animation
        except Exception as e:
            self.result_area.setPlainText(f"An error occurred: {str(e)}")
            self.fade_in_animation.start()  # Start fade-in animation

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SpotifyAudioFeaturesApp()
    ex.show()
    sys.exit(app.exec_())
