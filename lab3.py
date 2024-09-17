import cv2
import numpy as np
import math

def convolution(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))
    padding = math.floor(kernel.shape[0] / 2)
    kh, kw, = kernel.shape
    h = image.shape[0]
    w = image.shape[1]
    outputX = w + 2 * padding
    outputY = h + 2 * padding
    output = np.zeros((outputY, outputX))
    paddedImage = np.zeros((outputY, outputX))

    paddedImage[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
    for i in range(outputY - kh + 1):
        for f in range(outputX - kw + 1):
            v = np.sum(np.multiply(kernel, paddedImage[i:i+kh,f:f+kw]))
            output[i][f] = v
    
    print("Done")
    return output[:h, :w]


def sobel(image, T):
    gradient_x_k = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    gradient_y_k = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ])
    grad_x = convolution(image, gradient_x_k)
    cv2.imwrite("grad_x.png", grad_x)

    grad_y = convolution(image, gradient_y_k)
    cv2.imwrite("grad_y.png", grad_y)

    grad_magnitude = np.sqrt(np.power(grad_x, 2) + np.power(grad_y, 2))
    grad_direction = np.arctan2(grad_y, grad_x + 1e-10)
    cv2.imwrite("gradient_direction.png", grad_direction)
    grad_magnitude = (grad_magnitude > T) * 255
    cv2.imwrite("gradient_magnitude.png", grad_magnitude)
    return (pixel_loc_threshold(grad_magnitude, T), grad_direction)

def pixel_loc_threshold(image, T):
    locs = []
    for y in range(len(image)):
        for x in range(len(image[0])):
            if (image[y][x] > T):
                locs.append((y, x))
    return locs

def hough(gradient):
    grad_mag, grad_dir = gradient
    H = np.zeros((700, 700, 100))
    for pixel in grad_mag:
        (y, x) = pixel
        for r in range(10, 100):
            x_comp = int(r * math.cos(grad_dir[y][x]))
            y_comp = int(r * math.sin(grad_dir[y][x]))
            H[y + y_comp][x + x_comp][r] += 1
            H[y - y_comp][x - x_comp][r] += 1   

    summed = np.sum(H, axis=2)
    cv2.imwrite("hough_space.png", summed)
    return H

def get_circles_from_hough(H, T, image, image_name):
    circles = np.argwhere(H > T)

    for (y, x, r) in circles:
        image = cv2.circle(image, (x, y), r, (0, 0, 255), 1)
    cv2.imwrite(image_name.split(".png")[0] + "_detected.png", image)


image_name = "coins3.png"
image_gray = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
gradient = sobel(image_gray, 200)
H = hough(gradient)

image = cv2.imread(image_name)
get_circles_from_hough(H, 10, image, image_name)