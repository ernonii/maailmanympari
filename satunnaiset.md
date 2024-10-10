#Satunnaistapahtumia ja väsymyksen laskenta
def satunnaiset(tired):
    CRED = '\033[91m'
    CEND = '\033[0m'
    CGREEN = '\33[32m'
    roll = random.randint(1, 100)
    if roll <= 20:
        tired += 20
        print(CRED + "Huono sää häiritsi untasi, väsymyksesi nousee" + CEND)
    elif roll > 20 and roll <= 40:
        tired += 30
        print(CRED + "Hätätapaus lentokoneessa, purkautuminen viivästyy. 'Onko täällä lääkäriä paikalla!?'" + CEND)
    elif roll > 50 and roll <= 60:
        tired += 50
        print(CRED + "Ruokamyrkytys! Voit pahoin etkä saa levättyä ollenkaan matkalla." + CEND)
    elif roll > 61 and roll <= 65:
        tired -= 20
        print(CGREEN + "Löysit lennolta Finnairin mustikkamehua, joka virkistää sinua!" + CEND)
    elif roll > 66 and roll <= 80:
        money += 200
        print(CGREEN + "Löysit femman maasta, joka tässä ekonomiassa on oikeasti 200 euroa!" + CEND)
    else:
        return tired


def väsymyksen_kokeilu(tired):
    if tired > 100:
        print("Olet liian väsynyt jatkaaksesi, sinun on pakko levätä ja menetät aikaa...")
        tired -= 100
        input("Olet levännyt, voit jatkaa.")
    return tired

tired = satunnaiset(tired)