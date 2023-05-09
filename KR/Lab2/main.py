class NodArbore:
    def __init__(self, info, parinte=None):
        self.info = info
        self.parinte = parinte

    def drumRadacina(self) :
        l=[]
        nod=self
        while nod is not None:
            l.insert(0,nod)
            nod=nod.parinte
        return l

    def vizitat(self) :
        nod=self.parinte
        while nod is not None:
            if nod.info==self.info:
                return True
            nod=nod.parinte
        return False

    def __str__(self):
        return str(self.info)

    def __repr__(self):
        return "({}, ({}))".format(self.info, "->".join([str(x) for x in self.drumRadacina()]))

    def afisSolFisier(self, fisier):
        for x in self.drumRadacina():
            if x.info[2] == 1:
                cond_mal = f"(Stanga:<barca>) {x.info[1]} canibali, {x.info[0]} misionari ..... " \
                           f"(Dreapta) {Graf.N - x.info[1]} canibali, {Graf.N - x.info[0]} misionari"
            else:
                cond_mal = f"(Stanga) {x.info[1]} canibali, {x.info[0]} misionari ..... " \
                           f"(Dreapta:<barca>) {Graf.N - x.info[1]} canibali, {Graf.N - x.info[0]} misionari"

            if x.parinte is not None:
                if x.info[2] == 1:
                    fisier.write(
                        f">>> Barca s-a deplasat de la malul drept la malul stang cu {abs(x.parinte.info[1] - x.info[1])} "
                        f"canibali si {abs(x.parinte.info[0] - x.info[0])} misionari.\n")
                else:
                    fisier.write(
                        f">>> Barca s-a deplasat de la malul stang la malul drept cu {abs(x.parinte.info[1] - x.info[1])} "
                        f"canibali si {abs(x.parinte.info[0] - x.info[0])} misionari.\n")

            fisier.write(f"{cond_mal}\n\n")


class Graf:
    def __init__(self, start, scopuri):
        self.start = start
        self.scopuri = scopuri

    def scop(self, infoNod):
        return infoNod in self.scopuri

    def succesori(self, nod):
        def test(m, c):
            return m == 0 or m >= c

        l = []
        if nod.info[2] == 1:  # malul initial= malul cu barca (curent)
            misMalCurent = nod.info[0]
            canMalCurent = nod.info[1]
            misMalOpus = Graf.N - nod.info[0]
            canMalOpus = Graf.N - nod.info[1]
        else:
            misMalCurent = Graf.N - nod.info[0]
            canMalCurent = Graf.N - nod.info[1]
            misMalOpus = nod.info[0]
            canMalOpus = nod.info[1]

        maxMisBarca = min(Graf.M, misMalCurent)
        for mb in range(maxMisBarca + 1):
            if mb == 0:
                minCanBarca = 1
                maxCanBarca = min(Graf.M, canMalCurent)
            else:
                minCanBarca = 0
                maxCanBarca = min(mb, Graf.M - mb, canMalCurent)

            for cb in range(minCanBarca, maxCanBarca + 1):
                misMalCurentNou = misMalCurent - mb
                canMalCurentNou = canMalCurent - cb
                misMalOpusNou = misMalOpus + mb
                canMalOpusNou = canMalOpus + cb
                if not test(misMalCurentNou, canMalCurentNou):
                    continue
                if not test(misMalOpusNou, canMalOpusNou):
                    continue

                if nod.info[2] == 1:
                    infoNodNou = (misMalCurentNou, canMalCurentNou, 0)
                else:
                    infoNodNou = (misMalOpusNou, canMalOpusNou, 1)
                nodNou = NodArbore(infoNodNou, nod)

                if not nodNou.vizitat():
                    l.append(nodNou)
        return l


def breadth_first(gr, nsol):
    c = [NodArbore(gr.start)]
    while c:
        nodCurent = c.pop(0)
        if gr.scop(nodCurent.info):
            print(repr(nodCurent))
            fisier = open("KR\Lab2\output.txt", "a")
            nodCurent.afisSolFisier(fisier)
            nsol -= 1
            if nsol == 0:
                fisier.close()
                return
        lSuccesori = gr.succesori(nodCurent)
        c += lSuccesori


def depth_first(gr):
    start = NodArbore(gr.start)
    dfs_recursiv(start)


def dfs_recursiv(nod):
    global nsol
    if gr.scop(nod.info):
        print(repr(nod))
        nsol -= 1
        if nsol == 0:
            return
    lSuccesori = gr.succesori(nod)
    for s in lSuccesori:
        dfs_recursiv(s)


f = open("KR\Lab2\input.txt", "r")
continut = f.read().strip().split()
Graf.N = int(continut[0])
Graf.M = int(continut[1])

start = (Graf.N, Graf.N, 1)
scopuri = [(0, 0, 0)]

gr = Graf(start, scopuri)
breadth_first(gr, 1)
