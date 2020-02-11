import cv2;
import numpy as np;
from skimage import morphology, color, data;

# TODO: delete the following test code
path = 'C:/Users/47902/Desktop/task1.png' # 330*140
CIRCLES = np.zeros((2,3))

# Structure:
#   3 types images
#       1: src: original image
#       2: target: processing image
#       3: output: output image (copy of original one but have more info)

def readImage(path):
    """

    :param path:
    :return:
    """
    # read image and show original image
    src = cv2.imread(path)
    cv2.imshow('original image(input image)',src)

    target = preProcessing(src)
    findCircle(src)
    line_detection(target)
    arrowDetection(target)
    cv2.waitKey(0)

def preProcessing(src):
    """

    :param src: the original image
    :return:
    """
# TODO:
#     other preprocessing like change gamma, contract...

#     dilation, make the line and circles connect if there are some space between there does
#     problem: it should be called dilation however its erode here.
    target = src.copy()
    kernel = np.ones((5, 5), np.uint8)
    target = cv2.erode(target, kernel, iterations=1)

    # convert to gray
    grayTarget = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)
    cv2.imshow("gray", grayTarget)
    ret, resTarget = cv2.threshold(grayTarget, 127, 255, cv2.THRESH_BINARY_INV)
    resTarget = (resTarget < 0.5) * 1
    resTarget = 1- resTarget
    res = morphology.skeletonize(resTarget)
    res = res.astype(np.uint8)
    res = res * 255
    cv2.imshow("target", res)
    cv2.imwrite("C:/Users/47902/Desktop/outp.png",res)
    return res



def findCircle(src):
    gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
    output = src.copy()

    # detect circles in the image
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        CIRCLES = circles
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 1)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (255, 0, 0), -1)

        # show the output image
        cv2.imshow("output", output)
    else:
        print("not found circle")

def line_detection(src):
    edges = cv2.Canny(src, 50, 150)
    cv2.imshow("edges", edges)

    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 80)
    # for rho, theta in lines[0]:
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #
    # for rho, theta in lines[-1]:
    #     a = np.cos(theta)  # theta是弧度
    #     b = np.sin(theta)
    #     x1 = a * rho
    #     y1 = b * rho
    #
    # k = (y1-y0) / (x1-x0)
    # b = y0 - (k * x0)
    # checkRelation(k,b)
    # # cv2.line(image, (x0, y0), (x1, y1), (0, 0, 255), 2)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 60, minLineLength=5, maxLineGap=0)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(src, (x1, y1), (x2, y2), (0, 255, 0), 2)
        print("find one line")
    cv2.imshow("line_detect_possible_demo", src)

# TODO: three circles in one line
def checkRelation(k, b):
    flag = 0
    print(k,' ',b)
    for (x, y, r) in CIRCLES:
        distance = abs(k*x + -1*y + b) / (k ** 2 + 1)**0.5
        print(distance)
        if distance < r:
            flag = flag +1

    if flag == 2:
        print("they have some relation")
    else:
        print("there is no relation")


def arrowDetection(img):
    gray = np.float32(img)

    corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
    corners = np.int0(corners)

    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(img, (x, y), 3, 255, -1)
        print("find a corner")

    cv2.imshow('Corner', img)