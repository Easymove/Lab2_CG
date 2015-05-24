__author__ = 'Alex'

from PIL import Image
import math


def get_step(_from, _to):
    if _from < _to:
        return lambda x, step_size=1: x + step_size
    return lambda x, step_size=1: x - step_size


class SImage(object):

    def __init__(self, mode, size, color, scale=1):
        self.image = Image.new(mode, size, color)
        self.size = size
        self.color = color
        self.scale = scale
        self.mode = mode
        self.pseudo_size = self.get_pseudo_size()

    def show(self):
        self.image.show()

    def get_scale(self):
        return self.scale

    def get_pseudo_size(self):
        self.pseudo_size = (int(self.size[0] / self.scale), int(self.size[1] / self.scale))
        return self.pseudo_size

    def put_pseudo_pixel(self, pseudo_cord, color, gradient=1):
        for real_x in range(int((pseudo_cord[0]) * self.scale), int(pseudo_cord[0] * self.scale + 1)):
            for real_y in range(int((pseudo_cord[1]) * self.scale), int(pseudo_cord[1] * self.scale + 1)):
                self.image.putpixel((real_x, real_y),
                                    (math.ceil(color[0]*gradient),
                                     math.ceil(color[1]*gradient),
                                     math.ceil(color[2]*gradient)))

    def flip_vertically(self):
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    def flip_horizontally(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

    def shift_horizontally(self, pixels):
        if pixels < 0:
            to_shift = self.size[0] + pixels
        else:
            to_shift = pixels
        while abs(to_shift) > self.size[0]:
            if to_shift < 0:
                to_shift += self.size[0]
            else:
                to_shift -= self.size[0]
        arr = []
        for i in range(int(self.size[0] - to_shift), self.size[0]):
            tmp = []
            for j in range(0, self.size[1]):
                tmp.append(self.image.getpixel((i, j)))
            arr.append(tmp)
        arr1 = []
        for i in range(0, int(self.size[0] - to_shift)):
            tmp = []
            for j in range(0, self.size[1]):
                tmp.append(self.image.getpixel((i, j)))
            arr1.append(tmp)
        for i in range(0, int(self.size[0] - to_shift)):
            for j in range(0, self.size[1]):
                self.image.putpixel((i + int(to_shift), j), arr1[i][j])
        for i in range(0, int(to_shift)):
            for j in range(0, self.size[1]):
                self.image.putpixel((i, j), arr[i][j])

    def shift_vertically(self, pixels):
        if pixels < 0:
            to_shift = self.size[1] + pixels
        else:
            to_shift = pixels
        while abs(to_shift) > self.size[1]:
            if to_shift < 0:
                to_shift += self.size[1]
            else:
                to_shift -= self.size[1]
        arr = []
        for i in range(0, self.size[0]):
            tmp = []
            for j in range(int(self.size[1] - to_shift), self.size[1]):
                tmp.append(self.image.getpixel((i, j)))
            arr.append(tmp)
        arr1 = []
        for i in range(0, self.size[0]):
            tmp = []
            for j in range(0, int(self.size[1] - to_shift)):
                tmp.append(self.image.getpixel((i, j)))
            arr1.append(tmp)
        for i in range(0, self.size[0]):
            for j in range(0, int(self.size[1] - to_shift)):
                self.image.putpixel((i, j + int(to_shift)), arr1[i][j])
        for i in range(0, self.size[0]):
            for j in range(0, int(to_shift)):
                self.image.putpixel((i, j), arr[i][j])

    def rotate(self, degree):
        self.image = self.image.rotate(degree)

    def draw_line(self, a, b, color):
        dx = abs(b[0] - a[0])
        dy = abs(b[1] - a[1])
        x_step = get_step(a[0], b[0])
        y_step = get_step(a[1], b[1])
        pdx, pdy = 0, 0

        if dx > dy:
            pdx = x_step(0)
            es = dy
            el = dx
        else:
            pdy = y_step(0)
            es = dx
            el = dy

        current_x = a[0]
        current_y = a[1]
        err = el / 2

        self.put_pseudo_pixel((current_x, current_y), color)

        for _ in range(0, int(el)):
            err -= es
            if err < 0:
                err += el
                current_x = x_step(current_x)
                current_y = y_step(current_y)
            else:
                current_x += pdx
                current_y += pdy
            self.put_pseudo_pixel((current_x, current_y), color)

    @staticmethod
    def get_basis(i, n, t):
        return (math.factorial(n)/(math.factorial(i)*math.factorial(n - i))) * math.pow(t, i)*math.pow(1 - t, n - i)

    @staticmethod
    def get_curve(arr, step=0.01):
        res = []
        t = 0
        while t < 1 + step:
            if t > 1:
                t = 1

            ind = len(res)
            res.append([0, 0])

            for i in range(0, len(arr)):
                b = SImage.get_basis(i, len(arr) - 1, t)
                res[ind][0] += arr[i][0] * b
                res[ind][1] += arr[i][1] * b
            t += step
        return res

    def draw_bezier(self, arr, color):
        i = 0
        while i < len(arr) - 1:
            self.draw_line((arr[i][0], arr[i][1]), (arr[i + 1][0], arr[i + 1][1]), color)
            i += 1

    def draw_bezier_line(self, arr, color):
        flow = SImage.get_curve(arr, 0.01)
        self.draw_bezier(flow, color)


img = SImage("RGB", (400, 200), "black", 1)
img.draw_bezier_line([(50, 150), (200, 70), (150, 40), (300, 50), (100, 200), (20, 90)], (50, 220, 35))
img.shift_vertically(-10)
img.shift_horizontally(60)
img.show()