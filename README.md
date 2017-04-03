# greedygame

Question1 - DistortionImage.py
Usage: python DistortionImage.py testimage1.jpg 0 0 500 200 1000 1000 100 800 1000 1000
        testimage1.jpg - should be in the same directory. as the python file.
        Next 8 arguments are 4 (x,y) co-ordinates in the new image into which the image is to be mapped.
        Last 2 arguments are canvas/window size into which resultant image will be projected. Make sure it's larger than resultant image
        
Question 2 - ZoomWindow.py
Requirement - Pillow package. Used only for opening and saving the image.
Usage - python ZoomWindow.py testimage1.jpg 2.43 100 100 0
        testimage1.jpg - should be in the same directory. as the python file.
        Next argument is magnification factor. For factors which are power of 2, Weighet Median Interpolation is used. For others, Nearest            Neighbor Interpolation is used.
        Next 2 arguments are pivot point of zoom.
        Last argument is a flag whether image should be converted to grayscale or not. (0 - load colored image, 1 - load greyscale image)
