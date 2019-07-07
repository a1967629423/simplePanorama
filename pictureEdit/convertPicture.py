import sys
import os
from PIL import Image
from math import pi, sin, cos, tan, atan2, hypot, floor
from numpy import clip
import re
import concurrent.futures
# get x,y,z coords from out image pixels coords
# i,j are pixel coords
# faceIdx is face number
# faceSize is edge length
def outImgToXYZ(i, j, faceIdx, faceSize):
    a = 2.0 * float(i) / faceSize
    b = 2.0 * float(j) / faceSize

    if faceIdx == 0: # back
        (x,y,z) = (-1.0, 1.0 - a, 1.0 - b)
    elif faceIdx == 1: # left
        (x,y,z) = (a - 1.0, -1.0, 1.0 - b)
    elif faceIdx == 2: # front
        (x,y,z) = (1.0, a - 1.0, 1.0 - b)
    elif faceIdx == 3: # right
        (x,y,z) = (1.0 - a, 1.0, 1.0 - b)
    elif faceIdx == 4: # top
        (x,y,z) = (b - 1.0, a - 1.0, 1.0)
    elif faceIdx == 5: # bottom
        (x,y,z) = (1.0 - b, a - 1.0, -1.0)

    return (x, y, z)

# convert using an inverse transformation
def convertFace(imgIn, imgOut, faceIdx,fileName,out_path,faceNmae,fileType):
    x=0
    inSize = imgIn.size
    outSize = imgOut.size
    inPix = imgIn.load()
    outPix = imgOut.load()
    faceSize = outSize[0]
    for xOut in range(faceSize):
        for yOut in range(faceSize):
            (x,y,z) = outImgToXYZ(xOut, yOut, faceIdx, faceSize)
            theta = atan2(y,x) # range -pi to pi
            r = hypot(x,y)
            phi = atan2(z,r) # range -pi/2 to pi/2

            # source img coords
            uf = 0.5 * inSize[0] * (theta + pi) / pi
            vf = 0.5 * inSize[0] * (pi/2 - phi) / pi

            # Use bilinear interpolation between the four surrounding pixels
            ui = floor(uf)  # coord of pixel to bottom left
            vi = floor(vf)
            u2 = ui+1       # coords of pixel to top right
            v2 = vi+1
            mu = uf-ui      # fraction of way across pixel
            nu = vf-vi

            # Pixel values of four corners
            A = inPix[int(ui % inSize[0]) , int(clip(vi, 0, inSize[1]-1))]
            B = inPix[int(u2 % inSize[0]), int(clip(vi, 0, inSize[1]-1)) ]
            C = inPix[int(ui % inSize[0]) , int(clip(v2, 0, inSize[1]-1)) ]
            D = inPix[int(u2 % inSize[0]) , int(clip(v2, 0, inSize[1]-1)) ]

            # interpolate
            (r,g,b) = (
              A[0]*(1-mu)*(1-nu) + B[0]*(mu)*(1-nu) + C[0]*(1-mu)*nu+D[0]*mu*nu,
              A[1]*(1-mu)*(1-nu) + B[1]*(mu)*(1-nu) + C[1]*(1-mu)*nu+D[1]*mu*nu,
              A[2]*(1-mu)*(1-nu) + B[2]*(mu)*(1-nu) + C[2]*(1-mu)*nu+D[2]*mu*nu )

            outPix[xOut, yOut] = (int(round(r)), int(round(g)), int(round(b)))
    imgOut.save(os.path.join(out_path,fileName + "_" + faceNmae + "." + fileType))
FACE_NAMES = {
  0: 'back',
  1: 'left',
  2: 'front',
  3: 'right',
  4: 'top',
  5: 'bottom'
}
def callback(rst):
    print('error:'+rst.result())
def main(in_path,out_path):
    imgIn = Image.open(in_path)
    inSize = imgIn.size
    faceSize = inSize[0] // 4
    regex = re.compile(r'([^\\\/]*)\.(\w*)$')
    result = regex.search(in_path)
    fileName = result.group(1)
    fileType = result.group(2)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        imageOuts = []
        params = [[imgIn for i in range(6) ],imageOuts,[fileName for i in range(6)],[i for i in range(6)],[out_path for i in range(6)],[FACE_NAMES[i] for i in FACE_NAMES],[fileType for i in range(6)]]
        for face in range(6):
            print('convert face:'+FACE_NAMES[face])
            imgOut = Image.new("RGB", (faceSize, faceSize), "black")
            convertFace(imgIn,imgOut,face,fileName,out_path,FACE_NAMES[face],fileType)
            #params.append([imgIn,imgOut,fileName,face,out_path,FACE_NAMES[face],fileType])
        #     imageOuts.append(imgOut)
        # for item in executor.map(convertFace,*params):
        #     print(item)
            

if __name__ == "__main__":
    main(sys.argv[0],sys.argv[1] or './')