from PIL import Image, ImageFilter
import qrcode
import cv2 as cv


class QR_Operation():
    def __init__(self):
        pass

    def im_to_qr(self, image_name='image_test.png', qr_name='qr.png'):
        im = Image.open(image_name)
        im2 = Image.open(qr_name)
        x, y = im2.size
        pixels_qr = im2.load()
        im = im.resize((x, y))
        pixels_im = im.load()
        im.putalpha(115)

        for i in range(1, x - 1):
            for j in range(1, y - 1):
                if pixels_qr[i, j] == 0:
                    pixels_im[i, j] = (0, 0, 0)
                elif pixels_qr[i - 1, j] == 0:
                    pixels_im[i, j] = (255, 255, 255)
                elif pixels_qr[i - 1, j - 1] == 0:
                    pixels_im[i, j] = (255, 255, 255)
                elif pixels_qr[i, j - 1] == 0:
                    pixels_im[i, j] = (255, 255, 255)
                elif pixels_qr[i + 1, j + 1] == 0:
                    pixels_im[i, j] = (255, 255, 255)
                elif pixels_qr[i + 1, j] == 0:
                    pixels_im[i, j] = (255, 255, 255)
                elif pixels_qr[i, j + 1] == 0:
                    pixels_im[i, j] = (255, 255, 255)

        im.save(f"qr_{image_name}")

    def qr_incode(self, text, qr_name):
        img = qrcode.make(text)
        img.save(qr_name)

    def qr_decode(self, qr_name):
        im = cv.imread(qr_name)
        det = cv.QRCodeDetector()

        retval, points, straight_qrcode = det.detectAndDecode(im)
        return retval


#x = QR_Operation()
#x.qr_incode(input('Your text '), input('File name ')) #Указать расширение
#print(x.qr_decode(input('File name '))) #Указать расширение
#x.im_to_qr(input('Image name '), input('Qr name ')) #Указать расширение