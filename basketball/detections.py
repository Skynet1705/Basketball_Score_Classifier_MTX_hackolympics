import cv2 as cv2
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import time
import os


def detectImage(image):
    #     INPUT_FILE=path
    #     OUTPUT_FILE='predicted.jpg'
    # print("Detecting Image")
    LABELS_FILE = 'basketball/model/config/obj.names'
    CONFIG_FILE = 'basketball/model/config/yolov4-obj.cfg'
    WEIGHTS_FILE = 'basketball/model/config/yolov4-obj_last.weights'
    CONFIDENCE_THRESHOLD = 0.3

    LABELS = open(LABELS_FILE).read().strip().split("\n")

    np.random.seed(4)
    COLORS = np.random.randint(0, 255, size=(4, 3),
                               dtype="uint8")

    net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)

#     image = cv2.imread(INPUT_FILE)
    (H, W) = image.shape[:2]

    # determine only the *output* layer names that we need from YOLO
    ln1 = np.array(net.getLayerNames())
    # print(ln1)
    # print(net.getUnconnectedOutLayers())
    ln1 = [ln1[i - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln1)
    end = time.time()


#     print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > CONFIDENCE_THRESHOLD:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
                            CONFIDENCE_THRESHOLD)

    # ensure at least one detection exists
    detections = []
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

    # 		color = [int(c) for c in COLORS[classIDs[i]]]

    # 		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
#     		print("x "+str(x)+" y "+str(y)+" "+text)
#             detections = np.append(detections,np,array([x,y,h,w,LABELS[classIDs[i]],confidences[i]]))
            detections.append(
                [x, y, h, w, LABELS[classIDs[i]], confidences[i]])
#             print(text+x)
    #         print("x"+str(x)+"y"+str(y)+text )
    # 		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
    # 			0.5, color, 2)
    basketball_detections = [-99999, -99999, 0, 0, 'basketball', 0]
    basket_detections = [99999, 99999, 0, 0, 'basket', 0]
    basketball_confidence = -1
    basket_confidence = -1
    for k in range(len(detections)):
        if detections[k][4] == 'basketball' and detections[k][5] > basketball_confidence:
            basketball_detections = detections[k]
            basketball_confidence = detections[k][5]
        if detections[k][4] == 'basket' and detections[k][5] > basket_confidence:
            basket_detections = detections[k]
            basket_confidence = detections[k][5]
    if basket_detections[0] != -99999:
        cv2.rectangle(image, (basket_detections[0], basket_detections[1]), (basket_detections[0] +
                      basket_detections[2], basket_detections[1] + basket_detections[3]), [int(c) for c in COLORS[0]], 2)
        text = "{}: {:.4f}".format('basket', basket_detections[5])
        cv2.putText(image, text, (basket_detections[0], basket_detections[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, [int(c) for c in COLORS[2]], 2)

    if basketball_detections[0] != 99999:
        cv2.rectangle(image, (basketball_detections[0], basketball_detections[1]), (basketball_detections[0] +
                      basketball_detections[2], basketball_detections[1] + basketball_detections[3]), [int(c) for c in COLORS[1]], 2)
        text = "{}: {:.4f}".format('ball', basketball_detections[5])
        cv2.putText(image, text, (basketball_detections[0], basketball_detections[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, [int(c) for c in COLORS[1]], 2)

    # show the output image
    cv2.imwrite("basketball/static/scripts/example.png", image)
    # print("Hi"+str(detections))
    return basketball_detections, basket_detections


def detectVideo(path):
    # print("Hello")
    detections = []
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0
    basket = []
    basketBall = []
    row = []
    while success:
        #       cv2.imwrite("ScoringFrames\{}\{}.jpg".format(name,count), image)     # save frame as JPEG file
        # print("Frame Read")
        basketball_detections, basket_detections = detectImage(image)
        print(count)
        basket.append(basket_detections)
        basketBall.append(basketball_detections)
        # detections.append(detected)
        success, image = vidcap.read()
        count += 1
#       if count== :
#           break
#       print('Read a new frame: ', success)
    # print(str(detections))
    for i in range(len(basket)):
        row.append(basket[i][0])
        row.append(basket[i][1])
        row.append(basket[i][2])
        row.append(basket[i][3])

    for i in range(len(basketBall)):
        row.append(basketBall[i][0])
        row.append(basketBall[i][1])
        row.append(basketBall[i][2])
        row.append(basketBall[i][3])

    return row
