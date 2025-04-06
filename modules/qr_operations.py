import qrcode
import cv2
import numpy as np

def generate_qr(data):
    """Generate a simple QR code"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def decode_qr(file):
    """Decode QR code from image"""
    try:
        # Read the image file
        img_bytes = file.read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("Error: Failed to decode image")
            return None
            
        print("Image successfully loaded")
        
        # Convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("Image converted to grayscale")
        
        # Use OpenCV's QR code detector
        qr_detector = cv2.QRCodeDetector()
        retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(img)
        
        print(f"QR Detection result: {retval}")
        if retval and decoded_info:
            print(f"Decoded QR code: {decoded_info[0]}")
            return decoded_info[0]
            
        print("No QR code found in image")
        return None
        
    except Exception as e:
        print(f"Error decoding QR code: {str(e)}")
        return None 