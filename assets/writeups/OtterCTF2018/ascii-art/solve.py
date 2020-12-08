import skimage
from skimage.viewer import ImageViewer
import numpy as np

img = skimage.io.imread('1e0a220ee5875bcae68df3e5bc288896.png')


# Rotate image
rot = skimage.transform.rotate(img, 270, clip=False, resize=True)

## Rearrange by columns
chunks = [ rot[i:i+5] for i in range(0,rot.shape[0],5) ]

even = chunks[::2]
odds = chunks[1::2]
odds = [ np.roll(e[::, ::-1],-11, axis=1) for e in odds]

chunks = []
for i in range(len(odds)):
    chunks.append(even[i])
    chunks.append(odds[i])

chunks.append(even[-1])
# chunks = even + odds

columns = [e for chunk in chunks for e in chunk]

img = np.array(columns)


viewer = ImageViewer(img)
viewer.show()



img = skimage.transform.rotate(img, -90, clip=False, resize=True)

## Rearrange by rows

chunks = [ img[i:i+5] for i in range(0,img.shape[0],5) ]

even = chunks[::2]
even = [ e for e in even]
odds = chunks[1::2]
odds = [ np.roll(e[::, ::-1], -9, axis=1) for e in odds]

chunks = []
for i in range(len(odds)):
    chunks.append(even[i])
    chunks.append(odds[i])

chunks.append(even[-1])
# chunks = even + odds

columns = [e for chunk in chunks for e in chunk]

img = np.array(columns)

viewer = ImageViewer(img)
viewer.show()
