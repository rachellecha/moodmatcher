## IMPORTS ##

# Input/Output and Operating System status
import io 
import os 

# Google Vision API
from google.cloud import vision 
from google.cloud.vision import types

# drawing tools using Pillow
from PIL import Image, ImageDraw

# establish flask
from flask import Flask, render_template, redirect, request

## BEGIN APPLICATION ##

# creates application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

# routing to defualt page
@app.route('/')
def home():
    return render_template('index.html')

## GOOGLE VISION API ##

# set the os GCP APP varibale
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'VisionAPI/moodmatchervision.json'

def convert_likelyhood_to_int(str):
    likelihood_nums = { 'UNKNOWN': -1, 
                        'VERY_UNLIKELY': 0,
                        'UNLIKELY': 1,
                        'POSSIBLE': 2,
                        'LIKELY' : 3,
                        'VERY_LIKELY': 4}
    return likelihood_nums[str]

# os path detect faces; returns dictionary of emotions
def detect_faces():
    # client for image annotate vision 
    client = vision.ImageAnnotatorClient()

    # image to send
    file_name = os.path.relpath('aidanheadshot.jpg')

    #reading in the image file to memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    # setting the image 
    image = vision.types.Image(content=content)

    # making the request to vision 
    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    
    emotions = {'anger' : -1, 'sorrow': -1, 'joy' : -1,'suprise' : -1, 'detection_confidence' : 0}

    for face in faces:
        # print(type(face))
        emotions['anger'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.anger_likelihood]))
        emotions['sorrow'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.sorrow_likelihood]))
        emotions['joy'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.joy_likelihood]))
        emotions['suprise'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.surprise_likelihood]))
        emotions['detection_confidence'] = '{}'.format(face.detection_confidence)
        break

    # returns dictionary of emotions
    return emotions

# uri path detect faces; returns dictionary of emotions

def detect_faces_uri(uri):
    """Detects faces in the file located in Google Cloud Storage or the web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    
    emotions = {'anger' : -1, 'sorrow': -1, 'joy' : -1,'suprise' : -1, 'detection_confidence' : 0}

    for face in faces:
        emotions['anger'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.anger_likelihood]))
        emotions['sorrow'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.sorrow_likelihood]))
        emotions['joy'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.joy_likelihood]))
        emotions['suprise'] = convert_likelyhood_to_int('{}'.format(likelihood_name[face.surprise_likelihood]))
        emotions['detection_confidence'] = '{}'.format(face.detection_confidence)
        break

    return emotions
    

def detect_face(face_file, max_results=4):
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(
        image=image, max_results=max_results).face_annotations

def highlight_faces(image, faces, output_filename):
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(((face.bounding_poly.vertices)[0].x,
                   (face.bounding_poly.vertices)[0].y - 30),
                  str(format(face.detection_confidence, '1f')) + '%',
                  fill='#00ff00')
    im.save(output_filename)

def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)

# test scripts
main(os.path.relpath('aidanheadshot.jpg'), os.path.relpath('snipedaidanheadshot.jpg'),1)
emot = detect_faces()

print("DICTIONARY OF EMOTIONS")
for pair in emot.items():
    print(pair)

## APPLICATION DEPLOYMENT ##

# runs application
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(port=8080)