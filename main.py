from flask import Flask, render_template, Response
import cv2

from flask import Flask, render_template, Response,request
from flask_uploads import UploadSet,configure_uploads,IMAGES
import detect_mask_video
from detect_mask_video import VideoCamera
from detect_mask_image import image_detect
from facial_recognition_module import FacialIdentificationSystem
app = Flask(__name__)

photos=UploadSet('photos',IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] ="examples"
configure_uploads(app,photos)
@app.route('/')
def index():
    print("index() method called")
    # rendering webpage
    return render_template('index.html')

def gen(detect_mask_video):
    print("gen() method called")
    while True:
        #get camera frame
        frame = detect_mask_video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def generate_frames_for_identification(facial_recognition_module):
    while True:
        frame = facial_recognition_module.generate_frames_to_show()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/recogniseEngine')
def index2():
    # rendering webpage
    print("index2() method called")
    return render_template('videocapture.html')
@app.route('/recogniseImage')
def index3():
    # rendering webpage
    print("index3() method called")
    #image_detect()
    return render_template('videocapture.html')

# @app.route('/getJavascriptData',methods=["POST"])
# def get_javascript_data():
#      actualFileName=request.json['filename']
#      print("inside javascript method")
#      print(actualFileName," javascript value is found")
#      image_detect(actualFileName)
#      return "OK";



@app.route('/upload',methods=['GET','POST'])
def upload():
    print("upload() method called")
    if request.method == "POST" and 'photo' in request.files:
        filename=photos.save(request.files['photo'])
        print("Photo saved Succesfully inside the server",filename)
        image_detect(filename)
    return render_template('videocapture.html')


@app.route('/video_feed')
def video_feed():
    print("video_feed() method called")
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/facial_feed')
def facial_recognition_feed():
    print("video_feed() method called")
    return Response(generate_frames_for_identification(FacialIdentificationSystem),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # defining server ip address and port
    app.run(debug=True)