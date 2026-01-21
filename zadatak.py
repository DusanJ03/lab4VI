import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def showImages(img1, img2, img3):
    plt.figure(figsize=(15, 5))  # Dodao sam malo veci prozor
    plt.subplot(131)
    plt.imshow(img1)
    plt.axis("off")
    plt.subplot(132)
    plt.imshow(img2)
    plt.axis("off")
    plt.subplot(133)
    plt.imshow(img3)
    plt.axis("off")
    plt.show()


def findMatches(dst1, dst2):
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(dst1, dst2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    return good


def findMatrix(k1, k2, g, minMatch):
    if len(g) > minMatch:
        src_pts = np.float32([k1[m.queryIdx].pt for m in g]).reshape(-1, 1, 2)
        dst_pts = np.float32([k2[m.trainIdx].pt for m in g]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    else:
        return None
    return M


# --- OVO JE IZMENJENA FUNKCIJA ---
def transformImage(i1, i2, m):
    width = i1.shape[1] + i2.shape[1]
    height = i1.shape[0] + int(i2.shape[0] / 2)

    # 1. Warpujemo desnu sliku (i2) na veliko platno
    outimg = cv.warpPerspective(i2, m, (width, height))

    # 2. Izdvajamo region (ROI) gde treba da "nalepimo" levu sliku (i1)
    # ROI mora biti istih dimenzija kao i1
    roi = outimg[0:i1.shape[0], 0:i1.shape[1]]

    # 3. Pravimo MASKU: Gde god leva slika (i1) NIJE CRNA, tu cemo je nalepiti.
    # np.any(i1 > 0, axis=2) proverava da li je piksel obojen (nije [0,0,0])
    mask = np.any(i1 > 0, axis=2)

    # 4. Pametno lepljenje:
    # U ROI prebacujemo piksele iz i1 SAMO TAMO gde je maska True (gde ima slike).
    # Tamo gde je maska False (gde je i1 crna/prazna), ostaju pikseti iz outimg (warpovane desne slike).
    roi[mask] = i1[mask]

    # 5. Vracamo izmenjeni ROI nazad u glavnu sliku
    outimg[0:i1.shape[0], 0:i1.shape[1]] = roi

    return outimg


# ---------------------------------

def trimImage(img):
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    colorRows = np.any(imgGray != 0, axis=1)
    colorColumns = np.any(imgGray != 0, axis=0)
    trimmed = img[colorRows, :]
    trimmed = trimmed[:, colorColumns]
    return trimmed


def formPanorama(imgL, imgR):
    detector = cv.SIFT_create()
    kp1, des1 = detector.detectAndCompute(imgR, None)
    kp2, des2 = detector.detectAndCompute(imgL, None)
    good = findMatches(des1, des2)

    # Smanjio sam minMatch sa 10 na 4 za svaki slucaj, ali 10 je ok
    mat = findMatrix(kp1, kp2, good, 10)

    if mat is None:
        print("Nije pronadjena dovoljno dobra matrica za spajanje!")
        return imgL  # Vrati bar nesto da ne pukne

    mergedImage = transformImage(imgL, imgR, mat)
    mergedImage = trimImage(mergedImage)
    return mergedImage


# Ucitavanje slika
img3 = cv.imread('3.jpg')
img3 = cv.cvtColor(img3, cv.COLOR_BGR2RGB)
img1 = cv.imread('1.jpg')
img1 = cv.cvtColor(img1, cv.COLOR_BGR2RGB)
img2 = cv.imread('2.jpg')
img2 = cv.cvtColor(img2, cv.COLOR_BGR2RGB)

showImages(img1, img2, img3)

# Formiranje panorame
res12 = formPanorama(img1, img2)
res = formPanorama(res12, img3)

plt.figure(figsize=(12, 6))
plt.imshow(res)
plt.axis("off")
plt.show()