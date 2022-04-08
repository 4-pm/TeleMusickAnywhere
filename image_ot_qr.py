from PIL import Image, ImageFilter
import qrcode
import cv2 as cv
from datetime import datetime


class QR_Operation():
    def __init__(self, text='Pass', qr_name='qr'):
        try:
            img = qrcode.make(text)
            img.save(qr_name + '.png')
        except  Exception as error:
            self.error_window(error, type(error).__name__, '__init__', f'{text}, {qr_name}')

    def im_to_qr(self, image_name='image', qr_name='qr'):
        try:
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
        except  Exception as error:
            self.error_window(error, type(error).__name__, 'im_to_qr', f'{image_name}, {qr_name}')

    def qr_decode(self, qr_name='qr'):
        try:
            im = cv.imread(qr_name + '.png')
            det = cv.QRCodeDetector()

            retval, points, straight_qrcode = det.detectAndDecode(im)
            return retval
        except  Exception as error:
            self.error_window(error, type(error).__name__, 'qr_decode', 'qr_name')

    def make_gif(self, name='gif', f_number=10):
        try:
            frames = []

            for i in range(1, f_number + 1):
                f = Image.open(f'gif/{name}-{i}.jpg')
                f = f.resize((500, 500))
                frames.append(f)

            frames[0].save(
                f'{name}.gif',
                save_all=True,
                append_images=frames[1:],
                optimize=True,
                duration=500,
                loop=0
            )
        except  Exception as error:
            self.error_window(error, type(error).__name__, 'make_gif', f'{name}, {f_number}')

    def error_window(self, error, error_name, func_name, func_spis):
        with open('errors.txt', mode='r') as file_with_error_read:
            text = file_with_error_read.read()
        text += f'{datetime.now()}\n\n{error_name}: {error} -----> {func_name}({func_spis})\n\n'
        with open('errors.txt', mode='w') as file_with_error:
            file_with_error.write(text)


x = QR_Operation()
x = QR_Operation(input('Your text '), input('File name '))
print(x.qr_decode(input('File name ')))
x.im_to_qr(input('Image name '), input('Qr name '))
x.make_gif(input('Frame names '), int(input('Frame number ')))