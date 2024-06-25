import cv2
import numpy as np
import mediapipe as mp
import fitz  # PyMuPDF
from collections import deque
from abc import ABC, abstractmethod
from tkinter import filedialog, Tk

# Initialize Tkinter root for file dialog
root = Tk()
root.withdraw()


class AbstractCanvas(ABC):
    def __init__(self):
        self.bpoints = [deque(maxlen=1024)]
        self.gpoints = [deque(maxlen=1024)]
        self.rpoints = [deque(maxlen=1024)]
        self.ypoints = [deque(maxlen=1024)]
        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0
        self.kernel = np.ones((5, 5), np.uint8)
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0
        self.paintWindow = np.zeros((471, 636, 3)) + 255
        self.setup_canvas()

    def setup_canvas(self):
        self.paintWindow = cv2.rectangle(self.paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (160, 1), (255, 65), (255, 0, 0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (275, 1), (370, 65), (0, 255, 0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (390, 1), (485, 65), (0, 0, 255), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (505, 1), (600, 65), (0, 255, 255), 2)

        cv2.putText(self.paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

    @abstractmethod
    def draw_on_canvas(self, center, colorIndex):
        pass


class PDFCanvas(AbstractCanvas):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.pdf_images = self.pdf_to_images(pdf_path)
        self.pdf_page_index = 0
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils

    def pdf_to_images(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        images = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append(img)
        return images

    def draw_on_canvas(self, center, colorIndex):
        if colorIndex == 0:
            self.bpoints[self.blue_index].appendleft(center)
        elif colorIndex == 1:
            self.gpoints[self.green_index].appendleft(center)
        elif colorIndex == 2:
            self.rpoints[self.red_index].appendleft(center)
        elif colorIndex == 3:
            self.ypoints[self.yellow_index].appendleft(center)

    def clear_canvas(self):
        self.bpoints = [deque(maxlen=512)]
        self.gpoints = [deque(maxlen=512)]
        self.rpoints = [deque(maxlen=512)]
        self.ypoints = [deque(maxlen=512)]

        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0

        self.pdf_images[self.pdf_page_index] = np.zeros_like(self.pdf_images[self.pdf_page_index]) + 255

    def process_frame(self, frame):
        x, y, c = frame.shape
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.rectangle(frame, (40, 1), (140, 65), (0, 0, 0), 2)
        frame = cv2.rectangle(frame, (160, 1), (255, 65), (255, 0, 0), 2)
        frame = cv2.rectangle(frame, (275, 1), (370, 65), (0, 255, 0), 2)
        frame = cv2.rectangle(frame, (390, 1), (485, 65), (0, 0, 255), 2)
        frame = cv2.rectangle(frame, (505, 1), (600, 65), (0, 255, 255), 2)
        cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        result = self.hands.process(framergb)

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * frame.shape[1])
                    lmy = int(lm.y * frame.shape[0])
                    landmarks.append([lmx, lmy])
                self.mpDraw.draw_landmarks(frame, handslms, self.mpHands.HAND_CONNECTIONS)

            fore_finger = (landmarks[8][0], landmarks[8][1])
            center = fore_finger
            thumb = (landmarks[4][0], landmarks[4][1])
            cv2.circle(frame, center, 3, (0, 255, 0), -1)

            if (thumb[1] - center[1] < 30):
                self.bpoints.append(deque(maxlen=512))
                self.blue_index += 1
                self.gpoints.append(deque(maxlen=512))
                self.green_index += 1
                self.rpoints.append(deque(maxlen=512))
                self.red_index += 1
                self.ypoints.append(deque(maxlen=512))
                self.yellow_index += 1

            elif center[1] <= 65:
                if 40 <= center[0] <= 140:
                    self.clear_canvas()
                elif 160 <= center[0] <= 255:
                    self.colorIndex = 0  # Blue
                elif 275 <= center[0] <= 370:
                    self.colorIndex = 1  # Green
                elif 390 <= center[0] <= 485:
                    self.colorIndex = 2  # Red
                elif 505 <= center[0] <= 600:
                    self.colorIndex = 3  # Yellow
            else:
                self.draw_on_canvas(center, self.colorIndex)
        else:
            self.bpoints.append(deque(maxlen=512))
            self.blue_index += 1
            self.gpoints.append(deque(maxlen=512))
            self.green_index += 1
            self.rpoints.append(deque(maxlen=512))
            self.red_index += 1
            self.ypoints.append(deque(maxlen=512))
            self.yellow_index += 1

        points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(self.pdf_images[self.pdf_page_index], points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
                    cv2.line(self.paintWindow, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)

        return frame

    def show_pdf_page(self):
        cv2.imshow("PDF Page", self.pdf_images[self.pdf_page_index])

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = self.process_frame(frame)
            cv2.imshow("Output", frame)
            cv2.imshow("Paint", self.paintWindow)
            self.show_pdf_page()

            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('n'):
                self.pdf_page_index = (self.pdf_page_index + 1) % len(self.pdf_images)
            elif key == ord('p'):
                self.pdf_page_index = (self.pdf_page_index - 1) % len(self.pdf_images)

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        canvas = PDFCanvas(pdf_path)
        canvas.run()
