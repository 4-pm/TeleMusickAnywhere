from PIL import Image, ImageFilter
import qrcode


class QR_Operation():
    def __init__():
        pass

    def im_to_qr(image_name='image_test.png', qr_name='qr.png'):
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

    def qr_incode(text, qr_name):
        img = qrcode.make(text)
        img.save(qr_name)


QR_Operation.qr_incode(input('Your text '), input('File name ')) #Указать расширение
QR_Operation.im_to_qr(input('Image name '), input('Qr name ')) #Указать расширение