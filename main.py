import math
import numpy
from abc import abstractmethod


class Figura:

    def __init__(self, koordinate):
        self.koordinate = koordinate

    # proveravamo tip figure na osnovu koordinata, tj. da li je pravougaonik ili kvadar
    # to radim tako sto proveravam da li je u pitanju koordinatni sitem xy ili xyz
    def proveri_tip_figure(self):
        if len(koordinate[0]) > 2:
            return "kvadar"
        else:
            return "pravougaonik"

    # racunamo duzinu izmedju dve tacke
    def duzina_stranica(self, x1, y1, x2, y2):
        return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

    # ovo su abstraktne metode koje child klase moraju da implementiraju
    @abstractmethod
    def proveri_figuru(self):
        raise NotImplementedError("Morate da implementirate ovu metodu")

    @abstractmethod
    def proveri_tacku_x(self):
        raise NotImplementedError("Morate da implementirate ovu metodu")

    @abstractmethod
    def proveri_dijagonalu(self):
        raise NotImplementedError("Morate da implementirate ovu metodu")


# klasa Pravougaonik
class Pravougaonik(Figura):
    def __init__(self, koordinate):
        super().__init__(koordinate)
        # na osnovu koordinata odredjene su tacke u xy koordinatnom sistemu
        (self.xA, self.yA) = self.koordinate[0]
        (self.xB, self.yB) = self.koordinate[1]
        (self.xC, self.yC) = self.koordinate[2]
        (self.xX, self.yX) = self.koordinate[3]

    # funkcija koja proverava da li moze da se kreira pravougaonik na osnovu datih tacaka
    def proveri_figuru(self):
        return self.kvadrat_duzina()

    # funkcija koja ispituje da li su tacke kolinearne, tj. da li se tacke nalaze na istoj pravoj
    # ako se nalaze, pravougaonik se ne moze formirati
    def kolinearnost(self):
        nagib_ab = (self.yB - self.yA) / (self.xB - self.xA)
        nagib_bc = (self.yC - self.yB) / (self.xC - self.xB)

        return nagib_ab == nagib_bc

    # proveravamo da li sa zadatim tackama mozemo da formiramo trougao
    # jer ako ne moze da se formira trougao, onda ne moze da se formira cetvorougao
    def proveri_da_li_je_trougao(self, ab, bc, ac):
        if (ab < (ac + bc)) and (bc < (ac + ac)) and (ac < (ab + bc)):
            return True
        return False

    # funkcija u kojoj dobijamo rastojanja AB, BC, AC
    def kvadrat_duzina(self):
        ab = super().duzina_stranica(self.xA, self.yA, self.xB, self.yB)
        bc = super().duzina_stranica(self.xB, self.yB, self.xC, self.yC)
        ac = super().duzina_stranica(self.xA, self.yA, self.xC, self.yC)

        # na osnovu prethodnih funkcija proveravamo kolinearnost i da li moze da se formira trougao
        # ukoliko su ispunjena oba uslova, proveravamo da li vazi pitagorina teorema
        # ako vazi pitagorina teorema, to znaci da je trougao pravougli, i da se moze formirati prevougaonik
        if not self.kolinearnost() and self.proveri_da_li_je_trougao(ab, bc, ac):
            lista_tacaka = [ab, bc, ac]
            hipotenuza = max(lista_tacaka)
            if hipotenuza == ab:
                return math.isclose((ac ** 2 + bc ** 2), (ab ** 2))
            elif hipotenuza == bc:
                return math.isclose((ab ** 2 + ac ** 2), (bc ** 2))
            else:
                return math.isclose((ab ** 2 + bc ** 2), (ac ** 2))
        else:
            return False

    # metoda proveri_tacku_x
    # prvo pronalazim vektorski proizvod izmedju tacaka ab, ac, ax
    # zatim skalarni proizvod ab_ax, ac_ax, ab_ab, ac_ac
    # zatim proveravam da li je skalarni proizvod ab_ax izmedju 0 i ab ^ 2 i proveravam da li je ac_ax izmedju 0 i ac ^ 2
    # ako je skalarni proizvod pozitivan i manji od kvadrata duzine vektora, to znaci da je tacka unutar pravougaonika
    def proveri_tacku_x(self):
        ab = (self.xB - self.xA, self.yB - self.yA)
        ac = (self.xC - self.xA, self.yC - self.yA)
        ax = (self.xX - self.xA, self.yX - self.yA)

        ab_ax = numpy.dot(numpy.array(ab), numpy.array(ax))
        ac_ax = numpy.dot(numpy.array(ac), numpy.array(ax))
        ab_ab = numpy.dot(numpy.array(ab), numpy.array(ab))
        ac_ac = numpy.dot(numpy.array(ac), numpy.array(ac))

        if 0 < ab_ax < ab_ab and 0 < ac_ax < ac_ac:
            return True
        else:
            return False

    # racunam dijagonalu tako sto odredim rastojanja tacaka. Najvece rastojanje predstavlja dijagonalu
    def proveri_dijagonalu(self):
        ab = super().duzina_stranica(self.xA, self.yA, self.xB, self.yB)
        bc = super().duzina_stranica(self.xB, self.yB, self.xC, self.yC)
        ac = super().duzina_stranica(self.xA, self.yA, self.xC, self.yC)

        lista_tacaka = [ab, bc, ac]
        hipotenuza = max(lista_tacaka)
        return hipotenuza


class Kvadar(Figura):
    def __init__(self, koordinate):
        super().__init__(koordinate)
        # na osnovu koordinata odredjene su tacke u xy koordinatnom sistemu
        (self.xA, self.yA, self.zA) = self.koordinate[0]
        (self.xB, self.yB, self.zB) = self.koordinate[1]
        (self.xC, self.yC, self.zC) = self.koordinate[2]
        (self.xD, self.yD, self.zD) = self.koordinate[3]
        (self.xX, self.yX, self.zX) = self.koordinate[4]

    # proveravamo da li sa datim koordinatama mozemo da formiramo kvadar
    # racunamo vektorske proizvode ab, ac, ad
    # zatim racunamo skalarne proizvode ab_ac, ab_ad, ac_ad
    # ako su svi skalrni proizvodi jednaki nuli, to znaci da su vektori medjusobno ortogonalni, odnosno da je
    # ugao izmedju njih 90 stepeni. To znaci da moze da se formira kvadar
    def proveri_figuru(self):
        ab_vektor = (self.xB - self.xA, self.yB - self.yA, self.zB - self.zA)
        ac_vektor = (self.xC - self.xA, self.yC - self.yA, self.zC - self.zA)
        ad_vektor = (self.xD - self.xA, self.yD - self.yA, self.zD - self.zA)

        ab_ac_skalar = numpy.dot(numpy.array(ab_vektor), numpy.array(ac_vektor))
        ab_ad_skalar = numpy.dot(numpy.array(ab_vektor), numpy.array(ad_vektor))
        ac_ad_skalar = numpy.dot(numpy.array(ac_vektor), numpy.array(ad_vektor))

        if ab_ac_skalar == 0 and ab_ad_skalar == 0 and ac_ad_skalar == 0:
            return True
        else:
            return False

    # proveravam da li se tacka X nalazi unutar kvadra. To radim na slican nacin kao i za pravougaonik
    # S tim sto je ovde koordinatni sistem XYZ. I imamo jos jednu tacku D
    def proveri_tacku_x(self):
        ab_vektor = (self.xB - self.xA, self.yB - self.yA, self.zB - self.zA)
        ac_vektor = (self.xC - self.xA, self.yC - self.yA, self.zC - self.zA)
        ad_vektor = (self.xD - self.xA, self.yD - self.yA, self.zD - self.zA)
        ax_vektor = (self.xX - self.xA, self.yX - self.yA, self.zX - self.zA)

        ab_ax_skalar = numpy.dot(numpy.array(ab_vektor), numpy.array(ax_vektor))
        ac_ax_skalar = numpy.dot(numpy.array(ac_vektor), numpy.array(ax_vektor))
        ad_ax_skalar = numpy.dot(numpy.array(ad_vektor), numpy.array(ax_vektor))
        ab_ab_skalar = numpy.dot(numpy.array(ab_vektor), numpy.array(ab_vektor))
        ac_ac_skalar = numpy.dot(numpy.array(ac_vektor), numpy.array(ac_vektor))
        ad_ad_skalar = numpy.dot(numpy.array(ad_vektor), numpy.array(ad_vektor))

        return 0 <= ab_ax_skalar <= ab_ab_skalar and 0 <= ac_ax_skalar <= ac_ac_skalar and 0 <= ad_ax_skalar <= ad_ad_skalar

    # racunam dijagonalu preko formule
    def proveri_dijagonalu(self):
        ab = math.sqrt(((self.xB - self.xA) ** 2) + ((self.yB - self.yA) ** 2) + ((self.zB - self.zA) ** 2))
        ad = math.sqrt(((self.xD - self.xA) ** 2) + ((self.yD - self.yA) ** 2) + ((self.zD - self.zA) ** 2))
        ac = math.sqrt(((self.xC - self.xA) ** 2) + ((self.yC - self.yA) ** 2) + ((self.zC - self.zA) ** 2))

        return math.sqrt(ab ** 2 + ac ** 2 + ad ** 2)


koordinate = []
# pristupam fajlu u kojem se nalaze koordinate
# koristim funkciju spilt kako bih odvojio tekst od zareza
# zatim popunjavam listu koordinate sa podacima koje dobijam iz fajla
with open("koordinate.txt") as file:
    for i in file:
        tacka = i.split(",")
        pomocna_lista = []
        for j in tacka:
            pomocna_lista.append(int(j.strip()))
        koordinate.append(tuple(pomocna_lista))

# pravim objekat klase Figura kako bih proverio o kojem se tipu figure radi
figura = Figura(koordinate)
tip_figure = figura.proveri_tip_figure()
# proveravam da li je figura pravougaonik
if tip_figure == "pravougaonik":
    pravougaonik = Pravougaonik(koordinate)
    if pravougaonik.proveri_figuru():
        print("Figura se moze formirati! TIp figure je pravougaonik")
        if pravougaonik.proveri_tacku_x():
            print("Tacka X se nalazi unutar pravougaonika")
        else:
            print("Tacka X se ne nalazi unutar pravougaonika")
        print(f"Dijagonala je: {pravougaonik.proveri_dijagonalu()}")
#ako nije pravougaonik, onda je kvadar
else:
    kvadar = Kvadar(koordinate)
    if kvadar.proveri_figuru():
        print("Figura se moze formirati! Tip figure je kvadar ")
        if kvadar.proveri_tacku_x():
            print("Tacka X se nalazi unutar pravougaonika")
        else:
            print("Tacka X se ne nalazi unutar pravougaonika")
        print(f"Dijagonala je: {kvadar.proveri_dijagonalu()}")
