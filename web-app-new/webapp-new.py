import argparse
import os
import cv2
import time
from flask import Flask, request, Response, jsonify
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'runs/detect'
ALLOWED_EXTENSIONS = {'mp4'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = YOLO('C:/Users/JenyThev/Downloads/webapp/PDD_Phase2_V3.pt')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_video():
    if request.method == "POST":
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Process the video and make predictions
            video_path = filepath
            cap = cv2.VideoCapture(video_path)

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Define the codec and create VideoWriter object
            output_video_path = os.path.join(OUTPUT_FOLDER, 'output.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame_width, frame_height))

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = model(frame, save=False)
                res_plotted = results[0].plot()

                # Save frame as image
                frame_filename = f"frame_{frame_count}.jpg"
                frame_filepath = os.path.join(OUTPUT_FOLDER, frame_filename)
                cv2.imwrite(frame_filepath, res_plotted)

                # Write the frame to the output video
                out.write(res_plotted)
                frame_count += 1

                if cv2.waitKey(1) == ord('q'):
                    break

            cap.release()
            out.release()

            return jsonify({"message": "Video processed successfully", "output_video_path": output_video_path}), 200

    return '''
    <!doctype html>
    <title>Upload Video</title>
    <h1>Upload Video for Detection</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing YOLO models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.run(host="0.0.0.0", port=args.port)
