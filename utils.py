import cv2
image = cv2.imread('Resources/keyboard_layout.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    
    if w > 20 and h > 20:
        key_image = image[y:y+h, x:x+w]
        cv2.imwrite(f'keys/key_{i}.png', key_image)

print(f"Extracted {len(contours)} keys")