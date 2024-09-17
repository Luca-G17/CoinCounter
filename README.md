# Coin Counter
This project was written as part of a university project it can perform Hough Transform to identify and locate circular objects in images.

This project first utilises a sobel edge detection to establish an edge map for each image. This is achieved by computing the derivates in the $x$ and $y$ direction using a sobel filter.
The magnitude of the gradiant is thresholded at each pixel yeilding an edge map:


This is used in conjunction with the direction of each gradient to perform a Hough transform - This method assumes that any edge point in the image is a point on the edge of a circle, the algorithm then marks every possible centre point given the direction of the gradiant at that point. Finally we can threshold the map of cumulative centre points to detect circles.

![coins2_detected](https://github.com/user-attachments/assets/e784ede0-e3c5-43aa-900d-b158902778b6)
