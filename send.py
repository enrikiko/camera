import requests
import base64
import cv2
import time
import os
from skimage.metrics import structural_similarity as compare_ssim
import imageio
import numpy as np
sensivility=0.73
dark_sensivility=14

def image_is_not_black(image1_path):
    f = imageio.imread(image1_path, mode='L')
    if np.mean(f) > dark_sensivility:
        print("Not dark")
        print(np.mean(f))
        return True
    else:
        print("Dark")
        print(np.mean(f))
        return False

def are_image_different(image1_path, image2_path):
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    if image1.shape != image2.shape:
        return True
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    ssim_score, diff = compare_ssim(gray_image1, gray_image2, full=True)
    print(f"SSIM: {ssim_score}")
    if ssim_score >= 0.75:
        print("The images are similar (SSIM).")
        return False
    else:
        print("The images are different (SSIM).")
        return True
        
camera = cv2.VideoCapture(0)
secret = True
finish = False

while finish==False:
    while secret==True:
        # print(f"Old pic : {os.path.exists('/tmp/old_pic.jpg')}")
        # print(f"New pic : {os.path.exists('/tmp/pic.jpg')}")
        # print(f"secret : {secret}")
        # print(f"finish : {finish}")
        # time.sleep(0.1) 
        # print("Taking pics")
        return_value,image = camera.read()   
        # time.sleep(0.1) 
        image_rotated = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imwrite('/tmp/pic.jpg',image)    
        # print("Saving pics")
        # time.sleep(0.1) 
        secret = False
        if os.path.exists('/tmp/old_pic.jpg'):
            secret = False
            # print("Old pic exist")
        else:
            os.system('mv /tmp/pic.jpg /tmp/old_pic.jpg')  
            # print("Old pic not exist")
        # time.sleep(0.1) 
    if  are_image_different('/tmp/pic.jpg','/tmp/old_pic.jpg'):
        if image_is_not_black('/tmp/pic.jpg'):
            # print(f"Is diff pic: {are_image_different('/tmp/pic.jpg','/tmp/old_pic.jpg')}")
            url = 'https://cortijo-security-cameras-dev.cortijodemazas.com/update'
            with open('/tmp/pic.jpg', 'rb') as file:    
                binary_data = file.read()    
                headers = {'tenant': 'tenant1', 'Content-Type': 'image/jpeg', 'camera': 'camera1', 'x-api-key': os.environ['CAMERA_KEY'], 'Content-Length': str(len(binary_data))}    
            response = requests.post(url, data=binary_data, headers=headers)  
            # print("Pic send")
            # print(response.text)
            os.system('mv /tmp/pic.jpg /tmp/old_pic.jpg') 
            finish = True
            break
        else: 
            secret = True
            break
    else: 
        finish = True
        break
