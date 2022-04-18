from PIL import Image, ImageFilter
import qrcode
import cv2 as cv


class QR_Operation():
    def __init__(self, qr_name):
        self.qr_name = qr_name

    def qr_coder(self, text='Pass'): # Никита, что будет здесь? Название или текст?
        img = qrcode.make(text) # при помощи библиотеки qrcode делаем qr из введённого текста
        img.save(self.qr_name + '.png') # сохраняем

    def im_to_qr(self, image_name='image'):
        im = Image.open(image_name + '.png') # открываем фоновое изображение(предлагаю изображение, привязанное к пользователю)
        im2 = Image.open(self.qr_name + '.png') # открываем qr
        x, y = im2.size # получаем размер qr для ресайза изображения пользователя
        pixels_qr = im2.load() # получаем список пикселей изображения
        im = im.resize((x, y)) # приводим изображение к одному размеру с qr
        pixels_im = im.load() # получаем список пикселей изображения
        im.putalpha(115) # меняем прозрачность изображения для черных фотографий, иначе qr будет нечитаем

        for i in range(1, x - 1): # проходим циклом по изображению пользователя
            for j in range(1, y - 1):
                if pixels_qr[i, j] == 0:
                    pixels_im[i, j] = (0, 0, 0) # перерисовываем черные пиксели c qr на изображение пользователя
                else:
                    for p in range(-1, 2):
                        for t in range(-1, 2):
                            if pixels_qr[i + p, j + t] == 0:
                                pixels_im[i, j] = (255, 255, 255) # делаем окантовку вокруг черных пикселей qr
        im.save(f"qr_{image_name + '.png'}") # сохраняем

    def qr_decode(self):
        im = cv.imread(self.qr_name + '.png') # читаем qr
        det = cv.QRCodeDetector()

        text, points, straight_qrcode = det.detectAndDecode(im) # получаем данные о qr с помощью машинного зрения
        return text # возращаем только текст

    def make_gif(self, name='gif', name_fon='fon'):
        gif_base = Image.open(f'gif/{name}.jpg')
        gif_base = gif_base.resize((500, 500))
        fon = Image.open(f'gif/{name_fon}.jpg')
        fon = fon.resize((500, 500))

        frames = [] # список кадров

        for i in range(10):
            gif_base2 = gif_base
            pixels_gif = gif_base2.load()
            fon.rotate(36) # вращаем изображение
            pixels_fon = fon.load()

            for x in range(500):
                for y in range(500):
                    if pixels_gif[x, y] == (0, 255, 0):
                        pixels_gif[x, y] = pixels_fon[x, y]

            frames.append(gif_base2) # добавляем изображения в список

        frames[0].save(
            f'{name}.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=1000,
            loop=0
        ) # сохраняем с нужными параметрами (через параметр duration можно ускорить или замедлить гиф)

'''
x = QR_Operation()
x = QR_Operation(input('Your text '), input('File name '))
print(x.qr_decode(input('File name ')))
x.im_to_qr(input('Image name '), input('Qr name '))
x.make_gif(input('Frame names '), int(input('Frame number ')))'''
