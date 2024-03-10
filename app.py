from flask import Flask, render_template, Response
import cv2

# app = Flask(__name__)
app = Flask(__name__, template_folder="templates")


# cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# recording = True


def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()

        if not success:
            break

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # if len(faces) > 0:
        #     recording = True

        # for x, y, width, height in faces:
        #     cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

        _, jpeg = cv2.imencode(".jpg", frame)
        frame_bytes = jpeg.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n"
        )

        # cap.release()


def cleanup_camera():
    cap = cv2.VideoCapture(0)
    cap.release()


@app.route("/")
def index():
    return render_template("index.html")


#
#
# hudai
@app.route("/api/hello")
def hello():
    return "Hello from Flask on Vercel!"


# hudai
#
#


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/preview")
def preview():
    return render_template("preview.html")


# Add a route to call cleanup_camera() when leaving the preview page
@app.route("/close_camera")
def close_camera():
    cleanup_camera()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
