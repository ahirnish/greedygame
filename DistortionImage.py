import cv2
import numpy as np
import sys
 
def warpImage( imagePath, p1, p2, p3, p4 ):
 
    # Read source image.
    im_src = cv2.imread( imagePath )
    width = im_src.shape[ 1 ]
    height = im_src.shape[ 0 ]
    
    pts_src = np.array([[0, 0], [width-1, 0], [width-1, height-1],[0, height-1]], dtype = "float32")

    pts_dst = np.array([ p1, p2, p3, p4 ], dtype = "float32")
 
    # Calculate Homography
    h, status = cv2.findHomography(pts_src, pts_dst)
     
    # Warp source image to destination based on homography
    dest_canvas_width = 1000
    dest_canvas_height = 1000
    im_out = cv2.warpPerspective(im_src, h, (dest_canvas_width, dest_canvas_height))
     
    # Display image
    cv2.imwrite("WarpedImage.jpg", im_out)
 
def main( argv ):
    imagePath = str( argv[0] )
    point1 = []
    point1.append( argv[1] )
    point1.append( argv[2] )
    point2 = []
    point2.append( argv[3] )
    point2.append( argv[4] )
    point3 = []
    point3.append( argv[5] )
    point3.append( argv[6] )
    point4 = []
    point4.append( argv[7] )
    point4.append( argv[8] )
    warpImage( imagePath, point1, point2, point3, point4 )
    print "Result image is saved as WarpedImage.jpg in the current folder."

if __name__ == "__main__":
    main( sys.argv[ 1: ] )

    
    
