import cv2
from PIL import Image

cap = cv2.VideoCapture("video_file.mp4")

if cap.isOpened() == False:
    print('error opening file image classification')

(success, image) = cap.read()

list = []

while success:
    pil_image = Image.fromarray(image)

    res = pil_image.getcolors(pil_image.size[0] * pil_image.size[1])

    sorted_colors = sorted(res, key = lambda x:x[0], reverse=True)

    top_colors = sorted_colors[:3]

    rgb_colors = [c[1] for c in top_colors]

    if rgb_colors[0] not in list:
        list.append(rgb_colors[0])
    if rgb_colors[1] not in list:
        list.append(rgb_colors[1])
    if rgb_colors[2] not in list:
        list.append(rgb_colors[2])

    key = cv2.waitKey(1)

    (success, image) = cap.read()
cv2.destroyAllWindows()

print(list)

