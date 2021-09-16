import exercise
from workout import WorkoutPlan
from tkinter import Tk
from tkinter.ttk import Label, Button

_IP_CAMERA_URL = 'http://192.168.1.33:8080/shot.jpg'


class GUI:
    def __init__(self):
        self.video_streams = {
            'Webcam': (480, 640),
            'IP Camera': (1080, 1920)
        }
        self.exercises = {
            'Pushups': exercise.PushUps(),
            'Biceps': exercise.Biceps(),
        }
        self.selected_video_stream = None
        self.selected_exercise = None
        self._window = None

    def _set_video_stream(self, video_stream):
        self.selected_video_stream = video_stream
        self.close()

    def _set_exercise(self, exc):
        self.selected_exercise = exc
        self.close()

    # Loads the video stream window, in which the user selects an available video stream.
    def open_video_stream_selection_window(self):
        window = Tk()
        window.title('Deep Trainer - Video Stream')
        window.geometry('200x150')
        window.resizable(False, False)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=2)
        window.columnconfigure(2, weight=1)

        Label(text='Select Video Stream').grid(row=0, column=1, padx=10, pady=10)

        for i, stream in enumerate(self.video_streams.keys()):
            Button(window, text=stream, command=lambda s=stream: self._set_video_stream(s)).grid(
                row=i+1,
                column=1,
                padx=10,
                pady=5
            )

        self._window = window
        self._window.mainloop()

    def open_exercise_selection_window(self):
        window = Tk()
        window.title('Deep Trainer - Exercises')
        window.geometry('200x150')
        window.resizable(False, False)
        window.columnconfigure(0, weight=1)
        window.columnconfigure(1, weight=2)
        window.columnconfigure(2, weight=1)

        Label(text='Select Exercise').grid(row=0, column=1, padx=10, pady=10)

        for i, exc in enumerate(self.exercises.keys()):
            Button(window, text=exc, command= lambda e=exc: self._set_exercise(e)).grid(
                row=i+1,
                column=1,
                padx=10,
                pady=5
            )

        self._window = window
        self._window.mainloop()

    def close(self):
        self._window.destroy()

gui = GUI()
gui.open_video_stream_selection_window()
gui.open_exercise_selection_window()

if gui.selected_video_stream is None or gui.selected_exercise is None:
    exit(-1)

workout_plan = WorkoutPlan(
    gui.video_streams[gui.selected_video_stream],
    dict(),
    gui.exercises[gui.selected_exercise]
)
if gui.selected_video_stream == 'Webcam':
    workout_plan.play_from_webcam()
elif gui.selected_video_stream == 'IP Camera':
    workout_plan.play_from_ip_cam(_IP_CAMERA_URL)
