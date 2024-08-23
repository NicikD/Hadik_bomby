from collections import deque

class level:
    def __init__(self):
        self.steny = None
        self.had = None
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0

class objekt:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class stena(objekt):
    def __init__(self, x, y):
        super().__init__(x, y)

    def vytvorit(self, c, offsetx, offsety, blok):
        c.create_rectangle(offsetx + blok*(self.x)
                           , offsety + blok*(self.y)
                           , offsetx + blok*(self.x + 1)
                           , offsety + blok*(self.y + 1), outline="black", fill="black")


class had(objekt):
    def __init__(self, clanky):
        super().__init__(None, None)
        self.clanky = deque()
        self.clanky.extend(clanky)

    def vytvorit(self, c, offsetx, offsety, blok):
        for i, (x, y) in enumerate(self.clanky):
            if i == 0:
                farba = "RoyalBlue4"
            elif i + 1 == len(self.clanky):
                farba = "RoyalBlue1"
            else:
                farba = "RoyalBlue3"
            c.create_rectangle(offsetx + blok*(x)
                               , offsety + blok*(y)
                               , offsetx + blok*(x + 1)
                               , offsety + blok*(y + 1), fill = farba, outline = farba)

