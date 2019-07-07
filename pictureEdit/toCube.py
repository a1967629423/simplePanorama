import convertPicture as convert
import os
import sys
import re


def getAllPictureInDir(path):
    findFiles = []
    for root, dirs, files in os.walk(path):
        for file in files:
            mathObjt = re.match(r".*\.(png|jpge?|bmp)$", file, re.M | re.I)
            if(mathObjt):
                absFilename = os.path.join(root, file)
                
                findFiles.append([absFilename,file])
    return findFiles


def main(in_path, out_path, size, in_type, out_type):
    print(str.format('input: {input} output: {output}',
                     input=in_path, output=out_path))
    pictures = getAllPictureInDir(in_path)

    for filePath, fileName in pictures:
            print('convert: '+filePath)
            convert.main(filePath,out_path)
    print('done')


if __name__ == "__main__":
    actuallyArg = {
        'input': './',
        'output': './',
        'size': [300, 300],
        'intype': 'equirectangular',  # future cubemap connected-cubemap
        'outtype': 'cubemap'  # connected-cubemap future equirectangular
    }
    argv = sys.argv
    while(len(argv)):
        val = argv.pop(0)
        if(val == "-i"):
            actuallyArg['input'] = argv.pop(0)
        if(val == "-o"):
            actuallyArg['output'] = argv.pop(0)
        if(val == "-s"):
            val_first = argv.pop(0)
            if(str(val_first).isnumeric()):
                actuallyArg['size'][0] = int(val_first)
            else:
                raise Exception('type of size arg1 should be number')
            val_next = argv.pop(0)
            if(str(val_next).isnumeric()):
                actuallyArg['size'][1] = int(val_next)
            else:
                raise Exception('type of size arg2 should be number')
    main(actuallyArg['input'], actuallyArg['output'],
         actuallyArg['size'], actuallyArg['intype'], actuallyArg['outtype'])
