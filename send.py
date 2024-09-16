import requests
import base64
import cv2
import timeimport os
camera = cv2.VideoCapture(0)
secret = True
while True:
    while secret==True:
        return_value,image = camera.read()    
        image_rotated = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imwrite('test222.jpg',image_rotated)    
        secret = False

    while secret==False:
        url = 'https://cortijo-security-cameras-dev.cortijodemazas.com/update'
        with open('test222.jpg', 'rb') as file:    
            binary_data = file.read()    
            headers = {'tenant': 'tenant1', 'Content-Type': 'image/jpeg', 'camera' : 'camera1', 'x-api-key': os.environ['CAMERA_KEY'], 'Content-Length': str(len(binary_data))}    
        response = requests.post(url, data=binary_data, headers=headers)    
        print(response.text)
        time.sleep(300) 
        secret = True
        break
