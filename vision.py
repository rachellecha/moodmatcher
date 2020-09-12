import io 
import os 

from google.cloud import vision 
from google.cloud.vision import types

# set the os GCP APP varibale
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'VisionAPI\moodmatchervision.json'

#client for image annotate vision 
client = vision.ImageAnnotatorClient()

# image to send
file_name = os.path.relpath('test.jpg')

#reading in the image file to memory
with io.open(file_name,'rb') as image_file:
    content = image_file.read()

# setting the image 
image = types.Image(content=content)

# making the request to vision 
response = client.label_detection(image=image)

labels = response.label_annotations

for label in labels:
    print(label)

'''
def detect_faces(path):
    """Detects faces in an image."""

    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE', 'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
'''