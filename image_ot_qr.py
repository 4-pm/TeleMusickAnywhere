from PIL import Image, ImageFilter
import qrcode
import cv2 as cv


class QR_Operation():
    def __init__(self, text='Pass', qr_name='qr'):
        img = qrcode.make(text)
        img.save(qr_name + '.png')

    def im_to_qr(self, image_name='image', qr_name='qr'):
        im = Image.open(image_name + '.png')
        im2 = Image.open(qr_name + '.png')
        x, y = im2.size
        pixels_qr = im2.load()
        im = im.resize((x, y))
        pixels_im = im.load()
        im.putalpha(115)

        for i in range(1, x - 1):
            for j in range(1, y - 1):
                if pixels_qr[i, j] == 0:
                    pixels_im[i, j] = (0, 0, 0)
                else:
                    for p in range(-1, 2):
                        for t in range(-1, 2):
                            if pixels_qr[i + p, j + t] == 0:
                                pixels_im[i, j] = (255, 255, 255)

        im.save(f"qr_{image_name + '.png'}")

    def qr_decode(self, qr_name='qr'):
        im = cv.imread(qr_name + '.png')
        det = cv.QRCodeDetector()

        retval, points, straight_qrcode = det.detectAndDecode(im)
        return retval


x = QR_Operation(input('Your text '), input('File name '))
print(x.qr_decode(input('File name ')))
x.im_to_qr(input('Image name '), input('Qr name '))