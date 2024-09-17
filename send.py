import requests
import base64
import cv2
import time
import os
from skimage.metrics import structural_similarity as compare_ssim

def are_image_different(image1_path, image2_path):
    # Load the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)
    
    # Ensure the images have the same size
    if image1.shape != image2.shape:
        return True

    # Convert the images to grayscale
    gray_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    
    ssim_score, diff = compare_ssim(gray_image1, gray_image2, full=True)
    print(f"SSIM: {ssim_score:.4f}")
    # print(f"DIFF :{diff}")
    
    if ssim_score >= 0.6:
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
        time.sleep(1) 
        return_value,image = camera.read()    
        image_rotated = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imwrite('/tmp/pic.jpg',image)    
        secret = False
        if os.path.exists('/tmp/old_pic.jpg'):
            secret = False
        else:
            os.system('mv /tmp/pic.jpg /tmp/old_pic.jpg')  
    if  are_image_different('/tmp/pic.jpg','/tmp/old_pic.jpg'):
        os.system('mv /tmp/pic.jpg /tmp/old_pic.jpg')  
        url = 'https://cortijo-security-cameras-dev.cortijodemazas.com/update'
        with open('/tmp/pic.jpg', 'rb') as file:    
            binary_data = file.read()    
            headers = {'tenant': 'tenant1', 'Content-Type': 'image/jpeg', 'camera': 'camera1', 'x-api-key': os.environ['CAMERA_KEY'], 'Content-Length': str(len(binary_data))}    
        response = requests.post(url, data=binary_data, headers=headers)  
        print("Pic send")
        print(response.text)
        finish = True
        break
