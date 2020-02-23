# Module imports
import numpy as np
import cv2
import warnings

# Some warning filters to avoid console overload
warnings.simplefilter('ignore', np.RankWarning)
warnings.simplefilter('ignore', RuntimeWarning)


def gaussian(img, p):
    blur = cv2.GaussianBlur(img, (p, p), 0)
    return blur


def canny(img, low_threshold, high_threshold):
    edges = cv2.Canny(img, low_threshold, high_threshold)
    return edges

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255, ) * channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

#   [justLines = False]: if true, doesn't output the masked image
# Outputs:
#   average_lines: lines' array (only if justLines = False)
#   line_image: masked image (only if justLines = True)
def hough(img_bk, img_bd, a, b, c, justLines = False):
    lines = cv2.HoughLinesP(img_bd, 2, np.pi / 180, a, np.array([]), minLineLength = b, maxLineGap = c)
    if justLines:
        if lines is not None:
            average_lines = average_slope_intercept(np.copy(img_bk), lines)
        else:
            average_lines = []
        return average_lines
    else:
        line_image = np.copy(img_bk) * 0
        average_lines = None
        if lines is not None:
            average_lines = average_slope_intercept(np.copy(img_bk), lines)
            for line in average_lines:
                x1, y1, x2, y2 = line.reshape(4)
                try:
                    cv2.line(line_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
                except OverflowError:
                    pass
                color_edges = np.dstack((img_bd, img_bd, img_bd))
                line_image = cv2.addWeighted(color_edges, 1, line_image, 1, 0)
        return line_image, average_lines

left_fit_average = [0,0]
right_fit_average = [0,0]
def average_slope_intercept(image, lines):
    global left_fit_average, right_fit_average
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    if (len(left_fit) != 0):
    	left_fit_average = np.average(left_fit, axis = 0)

    if (len(right_fit) != 0):
    	right_fit_average = np.average(right_fit, axis = 0)

    left_line = make_coordinate(image, left_fit_average)
    right_line = make_coordinate(image, right_fit_average)
    average_lines = np.array([left_line, right_line])
    return average_lines

x1 = 0
x2 = 0
def make_coordinate (image, line_parameters):
    global x1,x2
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1 * (1 / 2))
    try :
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
    except ZeroDivisionError:
        pass

    if (x1 < 320):
        x1 = 100
    else:
        x1 = 600


    coordinates = np.array([x1, y1, x2, y2])

    return coordinates

def warp(img, src_coordinates=None, dst_coordinates=None):
    # Define source and destination coordinates to perform Warp transform
    if src_coordinates is None:
        src_coordinates = np.float32(
            [[0,  300],  # Bottom left
            [220,  150],  # Top left
            [420,  150],  # Top right
            [600, 300]]) # Bottom right
    if dst_coordinates is None:
        dst_coordinates = np.float32(
            [[0,  480],  # Bottom left
            [0,    0],  # Top left
            [640,   0],  # Top right
            [640, 480]]) # Bottom right

    # Use cv2.getPerspectiveTransform() to get M, the transform matrix
    M = cv2.getPerspectiveTransform(src_coordinates, dst_coordinates)
    Minv = cv2.getPerspectiveTransform(dst_coordinates, src_coordinates)
    # Use cv2.warpPerspective() to warp your image to a top-down view
    img_size = (img.shape[1], img.shape[0])
    warped = cv2.warpPerspective(img, M, img_size, flags=cv2.INTER_LINEAR)

    return warped, M, Minv

def punto_medio(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            #x1 = int(lines[0])
            #y1 = int(lines[1])
            x1 = 320
            y1 = 480
            x2 = int(lines[2])
            y2 = int(lines[3])
        try:
	        cv2.line(line_image, (x1,y1),(x2,y2),(255,0,0),10)
        except OverflowError:
	        pass

    return line_image
