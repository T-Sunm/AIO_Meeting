import cv2
import numpy as np
from PIL import Image
import streamlit as st

MODEL = "../model/MobileNetSSD_deploy.caffemodel"
PROTOTXT = "../model/MobileNetSSD_deploy.prototxt.txt"


def process_image(image):
  blob = cv2.dnn.blobFromImage(
      cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
  net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
  net.setInput(blob)
  detections = net.forward()
  return detections


def annotate_image(image, detections, confidence_threshold=0.5):
  # loop over the detections
  (h, w) = image.shape[:2]
  for i in np.arange(0, detections.shape[2]):
    confidence = detections[0, 0, i, 2]

    if confidence > confidence_threshold:
      # extract the index of the class label from the ‘detections ‘ ,
      # then compute the (x, y)-coordinates of the bounding box for
      # the object
      box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
      (start_x, start_y, end_x, end_y) = box.astype("int")
      cv2.rectangle(image, (start_x, start_y), (end_x, end_y), 70, 2)
    return image


def main():
  st.title("Object Detection for Images")

  uploaded_file = st.file_uploader("Choose files", type=['jpg', 'png', 'jpeg'])
  # đọc file ở dạng byte
  if uploaded_file:

    image = Image.open(uploaded_file)
    image_np = np.array(image)
    detections = process_image(image_np)
    processed_image = annotate_image(image_np, detections)
    print(detections)

    col1, col2 = st.columns(2)
    col1.image(image, caption=f"Original image: {uploaded_file.name}")
    col2.image(processed_image, caption="Processed image")


if __name__ == "__main__":
  main()
