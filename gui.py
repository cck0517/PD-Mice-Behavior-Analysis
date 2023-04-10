import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QSlider, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class VideoPlayer(QWidget): 
    def __init__(self, video_file, data_file):
        super(VideoPlayer, self).__init__()

        # Load video
        self.cap = cv2.VideoCapture(video_file)
        self.data = data_file

        # Create GUI elements
        self.figure = Figure()
        self.label = QLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1)
        self.slider.sliderMoved.connect(self.update_frame)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_slider)
        self.playback_speed = 1

        # Create Play button
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play_video)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(self.play_button)
        self.setLayout(layout)

        # Start video playback
        self.update_frame(0)
        self.timer.start(30)

    def play_video(self):
        self.playback_speed = 1
        if self.timer.isActive():
            self.timer.stop()
            self.play_button.setText("Play")
        else:
            self.timer.start(30)
            self.play_button.setText("Pause")


    def update_frame(self, pos):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = self.cap.read()
        if ret:
            # Process the frame and update the label
            processed_frame = self.process_frame(frame) # Process the frame, e.g., detect activity levels
            self.label.setPixmap(processed_frame)
            self.plot_frame(processed_frame)
        else:
            self.timer.stop()

    def update_slider(self):
        # Update slider position based on video playback speed
        pos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        pos += self.playback_speed
        self.slider.setValue(int(pos))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = self.cap.read()
        if ret:
            # Process the frame and update the label
            processed_frame = self.process_frame(frame)
            self.label.setPixmap(processed_frame)
        else:
            self.timer.stop()


    def plot_frame(self, frame):
        self.canvas = FigureCanvas(self.figure)

    #     data = pd.read_csv(self.data)
    #     cluster = data['cluster']

    #     fig, ax = plt.subplots()
    #     ax.plot(1, 1, 'o', color='red')
    #     ax.set_xlabel('X Label')
    #     ax.set_ylabel('Y Label')
    #     fig.tight_layout()
    #     canvas = FigureCanvas(fig)
    #     canvas.draw()

    #     # Convert the matplotlib figure to QPixmap format
    #     buffer = canvas.buffer_info()
    #     img = np.array(buffer.rgb).reshape(buffer.height, buffer.width, 4)
    #     processed_image = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)  # Convert RGBA to BGR
    #     processed_image

    #     # Clear the previous plot
    #     self.figure.clear()
        
    #     ax.imshow(frame)

    #     # Redraw the canvas
    #     self.canvas.draw()

    def process_frame(self, frame):
        # Add your processing logic here
        # e.g., detect activity levels, calculate speed, angular change, etc.
        # and return the processed frame as a QPixmap or QImage
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = processed_frame.shape
        bytes_per_line = channel * width
        qimage = QImage(processed_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(qimage)
        return qpixmap

    def closeEvent(self, event):
        # Stop the timer and release the video capture when closing the window
        self.timer.stop()
        self.cap.release()
        super(VideoPlayer, self).closeEvent(event)

if __name__ == '__main__':
    # Create a QApplication instance
    app = QApplication([])
    
    # Create a VideoPlayer instance with the path to the video file
    video_file = "C:\\Users\\chang\\DeepLabCut\\main\\JUPYTER\\DLC_Data\\videos\\2022-10-12 14-41-54.mp4" # Replace with your actual video file path
    cluster_file = "C:\\Users\\chang\\DeepLabCut\\main\\JUPYTER\\DLC_Data\\videos\\2022-10-12 14-41-54_clustered.csv"
    player = VideoPlayer(video_file, cluster_file) 
    
    
    # Show the video player window
    player.show()
    
    # Start the event loop
    app.exec_()
