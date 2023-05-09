from queue import PriorityQueue

class NodArbore:
    def __init__(self, info, parinte=None, g=0, h=0):
        self.info = info
        self.parinte = parinte
        self.g = g
        self.h = h
        self.f = g + h

    def drumRadacina(self):
        l = []
        nod = self
        while nod is not None:
            l.insert(0, nod)
            nod = nod.parinte
        return l

    def vizitat(self):
        nod = self.parinte
        while nod is not None:
            if nod.info == self.info:
                return True
            nod = nod.parinte
        return False

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return "({}, ({}), cost: {})".format(self.info, "->".join([str(x) for x in self.drumRadacina()]), self.f)

    def __eq__(self, other):
        return self.info == other.info

    def __le__(self, other):
        return self.f <= other.f
    def __lt__(self, other):
        return self.f < other.f


class Graf:
    def __init__(self, matr, start, scopuri, h):
        self.matr = matr
        self.start = start
        self.scopuri = scopuri
        self.estimatii = h

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def succesori(self, nod):
        l = []
        for i in range(len(self.matr)):
            if self.matr[nod.info][i] != 0:
                nodNou = NodArbore(i, nod, nod.g + self.matr[nod.info][i], self.calculeaza_h(i))
                if not nodNou.vizitat():
                    l.append(nodNou)
        return l

    def calculeaza_h(self, infonod):
        return self.estimatii[infonod]


def bin_search(listaNoduri, nodNou, ls, ld):
    if len(listaNoduri) == 0:
        return 0
    if ls == ld:
        if nodNou.f < listaNoduri[ls].f:
            return ls
        elif nodNou.f > listaNoduri[ls].f:
            return ld + 1
        else:  # f-uri egale
            if nodNou.g < listaNoduri[ls].g:
                return ld + 1
            else:
                return ls
    else:
        mij = (ls + ld) // 2
        if nodNou.f < listaNoduri[mij].f:
            return bin_search(listaNoduri, nodNou, ls, mij)
        elif nodNou.f > listaNoduri[mij].f:
            return bin_search(listaNoduri, nodNou, mij + 1, ld)
        else:
            if nodNou.g < listaNoduri[mij].g:
                return bin_search(listaNoduri, nodNou, mij + 1, ld)
            else:
                return bin_search(listaNoduri, nodNou, ls, mij)


def aStarSolMultiple(gr, nsol):
    c = [NodArbore(gr.start)]
    while c:
        nodCurent = c.pop(0)
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            nsol -= 1
            if nsol == 0:
                return
        lSuccesori = gr.succesori(nodCurent)
        for s in lSuccesori:
            indice = bin_search(c, s, 0, len(c) - 1)
            if indice == len(c):
                c.append(s)
            else:
                c.insert(indice, s)

def a_star(gr):
    openList = PriorityQueue()
    openList.put(NodArbore(gr.start))
    closedList = []
    while openList:
        nodCurent = openList.get()
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            return
        lSuccesori = gr.succesori(nodCurent)
        closedList.append(nodCurent)
        for s in lSuccesori:
            nod_nou = None
            if s not in nodCurent.drumRadacina():
                if s in openList.queue:
                    nod_open = openList.get(s)
                    if s.f < nod_open.f:
                        s.parinte = nodCurent
                        # costul nodului curent plus costul muchiei de la nodul curent la s
                        s.g = nodCurent.g + gr.matr[nodCurent.info][s.info]
                        s.f = s.g + s.h
                        nod_nou = s
                if s in closedList:
                    index = bin_search(closedList, s, 0, len(closedList) - 1)
                    nod_closed = closedList[index]
                    if s.f < nod_closed.f:
                        s.parinte = nodCurent
                        # costul nodului curent plus costul muchiei de la nodul curent la s
                        s.g = nodCurent.g + gr.matr[nodCurent.info][s.info]
                        s.f = s.g + s.h
                        nod_nou = s
                else:
                    nod_nou = s
                if nod_nou:
                    openList.put(nod_nou)


m = [
    [0, 3, 5, 10, 0, 0, 100],
    [0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 4, 9, 3, 0],
    [0, 3, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 5],
    [0, 0, 3, 0, 0, 0, 0],
]
start = 0
scopuri = [4, 6]
h = [0, 1, 6, 2, 0, 3, 0]

gr = Graf(m, start, scopuri, h)
aStarSolMultiple(gr, 3)
a_star(gr)
