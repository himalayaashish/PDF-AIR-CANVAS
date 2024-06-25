# PDF Sign and Annotate with Hand Gestures

This project allows users to upload a PDF file and sign or annotate it using hand gestures captured via a webcam. The application leverages OpenCV, MediaPipe, and PyMuPDF for real-time hand tracking and PDF manipulation.

## Screenshot

Here's a screenshot of the application in action:

![Alt text](https://github.com/himalayaashish/PDF-AIR-CANVAS/blob/main/screensort/Screenshot%202024-06-25%20at%2011.58.39%E2%80%AFAM.png)

## Features

- **Hand Gesture Recognition**: Uses MediaPipe for real-time hand tracking.
- **PDF Annotation**: Allows drawing on PDF pages using different colors.
- **Page Navigation**: Navigate through PDF pages using keyboard keys.
- **Clear Drawing**: Clear annotations with a gesture.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repository/pdf-sign-annotate.git
    cd pdf-sign-annotate
    ```

2. **Install Dependencies**:
    ```bash
    pip install opencv-python numpy mediapipe PyMuPDF
    ```

## Usage

1. **Run the Application**:
    ```bash
    python main.py
    ```

2. **Upload PDF**: A file dialog will appear. Select the PDF file you want to annotate.

3. **Controls**:
    - **Drawing**: Use your hand to draw on the PDF.
    - **Change Color**: Select colors by moving your hand over the color buttons.
    - **Clear Drawing**: Move your hand over the "CLEAR" button to erase annotations.
    - **Navigate Pages**: Press `n` to go to the next page and `p` to go to the previous page.
    - **Quit**: Press `q` to exit the application.

## Code Structure

- **signPDF.py**: Main script that runs the application.
- **AbstractCanvas Class**: Abstract base class defining the canvas.
- **PDFCanvas Class**: Inherits from `AbstractCanvas` and adds PDF-specific functionality.

## Project Components

- **OpenCV**: For handling video capture and image processing.
- **MediaPipe**: For real-time hand detection and tracking.
- **PyMuPDF**: For handling PDF files and converting pages to images.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License


