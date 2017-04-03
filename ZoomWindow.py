from PIL import Image
import numpy as np
import sys, random
from datetime import datetime

def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def create_image( width, height, greyScale ):
  if greyScale:
    imgType = "L"
  else:
    imgType = "RGB"
  image = Image.new( imgType, ( width, height ), "white" )
  return image

def get_pixel( pixel, i, j, c, w, h ):
  if(i>=w or i<0 or j>=h or j<0):
    return None
  if c == -1:
    return pixel[ i,j ]
  if isinstance( pixel[ i,j ], int ):
    return pixel[ i,j ]
  return pixel[ i,j ][ c ]

def get_image( imagePath, greyScale=False ):
  image = Image.open( imagePath )
  if greyScale:
    return image.convert( 'L' )
  return image

def zoom( image, greyScale=False ):
  width, height = image.size

  zimg = create_image( width*2, height*2, greyScale )
  pix = image.load()
  zpix = zimg.load()

  if greyScale:
    colors = 1
  else:
    colors = 3

  for i in range( width ):
    for j in range( height ):
      zpix[ 2*i, 2*j ] = pix[ i, j ]

  for i in range( width ):
    for j in range( height ):
      med = []
      for c in xrange( colors ):
        val = []
        val1 = get_pixel( pix, i, j, c, width, height )
        if val1:
          val.append( val1 )
        val2 = get_pixel( pix, i, j+1, c, width, height )
        if val2:
          val.append( val2 )
        val3 = get_pixel( pix, i+1, j, c, width, height )
        if val3:
          val.append( val3 )
        val4 = get_pixel( pix, i+1, j+1, c, width, height )
        if val4:
          val.append( val4 )
        med.append( int( np.median( val ) ) )
      zpix[ (2*i)+1, (2*j)+1 ] = tuple( med )

  for i in range( width ):
    for j in range( height ):
      med = []
      for c in xrange( colors ):
        val = []
        val1 = get_pixel( pix, i, j, c, width, height )
        if val1:
          val.append( val1 )
        val2 = get_pixel( pix, i+1, j, c, width, height )
        if val2:
          val.append( val2 )
        val3 = get_pixel( zpix, (2*i) + 1, (2*j) - 1, c, 2*width, 2*height )
        if val3:
          m1=val1 if val1 else 255
          m2=val2 if val2 else 255
          min = m1 if m1<m2 else m2
          max = m1 if m1>m2 else m2
          if val3 >= min and val3 <= max:
            val.append( val3 )
          else:
            val.append( ( min + max )/2 )
        val4 = get_pixel( zpix, (2*i) + 1, (2*j) + 1, c, 2*width, 2*height )
        if val4:
          m1=val1 if val1 else 255
          m2=val2 if val2 else 255
          min = m1 if m1<m2 else m2
          max = m1 if m1>m2 else m2
          if val4 >= min and val4 <= max:
            val.append( val4 )
          else:
            val.append( ( min + max )/2 )
        med.append( int( np.median( val ) ) )
      zpix[ (2*i) + 1, 2*j ] = tuple( med )

  for i in range( width ):
    for j in range( height ):
      med = []
      for c in xrange( colors ):
        val = []
        val1 = get_pixel( pix, i, j, c, width, height )
        if val1:
          val.append( val1 )
        val2 = get_pixel( pix, i, j+1, c, width, height )
        if val2:
          val.append( val2 )
        val3 = get_pixel( zpix, (2*i)-1, (2*j)+1, c, 2*width, 2*height )
        if val3:
          m1=val1 if val1 else 255
          m2=val2 if val2 else 255
          min = m1 if m1 < m2 else m2
          max = m1 if m1 > m2 else m2
          if val3 >= min and val3 <= max:
            val.append( val3 )
          else:
            val.append( ( min + max )/2 )
        val4 = get_pixel( zpix, (2*i)+1, (2*j)+1, c, 2*width, 2*height )
        if val4:
          m1=val1 if val1 else 255
          m2=val2 if val2 else 255
          min = m1 if m1 < m2 else m2
          max = m1 if m1 > m2 else m2
          if val4 >= min and val4 <= max:
            val.append( val4 )
          else:
            val.append( ( min + max )/2 )
        med.append( int( np.median( val ) ) )
      zpix[ 2*i, (2*j)+1 ] = tuple( med )

  return zimg

def weightedMeanInterpolation( imagePath, centreX, centreY, greyScale, factor ):
    print "Using Weighted Mean Interpolation to zoom the image by the factor of %d" % factor
    orig_image = get_image( imagePath, greyScale )
    width, height = orig_image.size
    
    temp_factor = 1
    count = 0 
    while( temp_factor<factor ):
        temp_factor=temp_factor*2
        count = count + 1
  
    zoomImage = orig_image
    for i in xrange( count ):
        zoomImage = zoom( zoomImage, greyScale )
    zoomPixelMap = zoomImage.load()

    return zoomImage

def crop( width, height, factor, centreX, centreY, greyScale, zoomImage ):
    final_img = create_image( width, height, greyScale )
    finalPixelMap = final_img.load()
    offsetX, offsetY = centreX-(width/2), (centreY-height/2)
    zoomPixelMap = zoomImage.load()

    for i in range( width ):
        for j in range( height ):
            val = get_pixel( zoomPixelMap, offsetX + i, offsetY + j, -1, int(factor*width), int(factor*height) )
            finalPixelMap[ i, j ] = val if val else 0
    
    return final_img

def nearestNeighborInterpolation( imagePath, centreX, centreY, greyScale, factor ):
    print "Using Nearest Neighbor Interpolation to zoom the image by the factor of %d" % factor
    orig_image = get_image( imagePath, greyScale )
    width, height = orig_image.size
    
    proportion = 1/float(factor)
    new_width = int( factor*width )
    new_height = int( factor*height )
    temp_image = create_image( new_width, new_height, greyScale )
    temp_pixelMap = temp_image.load()
    orig_pixelMap = orig_image.load()
    
    for i in range( new_width ):
        for j in range( new_height ):
            px = int( i*proportion )
            py = int( j*proportion )
            temp_pixelMap[i,j] = orig_pixelMap[ px, py ]
            
    return temp_image

def powOf2( num ):
    return ( num & num-1 ) == 0

def main( args ):
    if len( args ) != 5:
        print "USAGE: python zoomWindow.py <path_to_image_in_current_directory> <zoom_factor> <zoom_center_x> <zoom_centre _y> <greyscale>"
        return
    path = str( args[ 0 ] )
    if isint( args[ 1 ] ):
        if isfloat( args[ 1 ] ):
            factor = int( float( args[1] ) )
        else:
            factor = int( args[ 1 ] )
    else:
        factor = float( args[ 1 ] )
    centreX = int( args[ 2 ] )
    centreY = int( args[ 3 ] )
    greyScale = True if int( args[ 4 ] ) else False 
    
    if( powOf2( factor ) ):
        zoomImage = weightedMeanInterpolation( path, centreX, centreY, greyScale, factor )
    else:
        zoomImage = nearestNeighborInterpolation( path, centreX, centreY, greyScale, factor )

    originalImage = get_image( path, greyScale )
    width, height = originalImage.size
    finalCropImage = crop( width, height, factor, centreX, centreY, greyScale, zoomImage )
  
    zoomImage.save( 'ZoomImage.jpg', 'JPEG' )
    finalCropImage.save( 'FinalCropImage.jpg', 'JPEG' )
    
    originalImage.show()
    zoomImage.show()
    finalCropImage.show()

    print "Zoomed image is saved as ZoomImage.jpg in the current folder."
    print "Cropped image is saved as FinalCropImage.jpg in the current folder."

if __name__ == "__main__":
    main( sys.argv[ 1: ] )






