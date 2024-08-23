from game import objekty as obj


def nacitaj(i):
    level = obj.level

    if not (0 < i < 17):
        return None

    with open("resources/{}.hadik".format(i), "r") as f:
        line = f.readline()
        if "#velkost" in line:
            level.x1, level.x2, level.y1, level.y2 = ([int(x) for x in f.readline().split()])

        line = f.readline()
        if "#hadik" in line:
            x, y = ([int(x) for x in f.readline().split()])
            level.had = obj.had(((x, y), (x, y+1), (x-1, y+1), (x-1, y)))

        line = f.readline()
        if "#stena" in line:
            line = f.readline()
            level.steny = []
            while line.strip() != "":
                (x, y) = ([int(x) for x in line.split()])
                level.steny.append(obj.stena(x, y))
                line = f.readline()

    return level
