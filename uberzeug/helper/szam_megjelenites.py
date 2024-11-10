import string

ELVALASZTO = '.'
TIZEDESJEL = ','
TIZEDESPONT = '.'

def ezresv (szam):
    """ Ezres-elválasztó lebegőpontos számokhoz:
        - tört rész max. háromértékes jegyű, többre nincs szükség"""
    szam = str(szam)
    elojel = ''
    if szam.startswith('-'):
        elojel = '-'
    dzsuva = string.ascii_letters + string.punctuation + string.whitespace
    szam = szam.replace(TIZEDESPONT, TIZEDESJEL) #ha véletlenül pont lenne
    dzsuva = dzsuva.replace(TIZEDESJEL, '')
    for c in dzsuva:
        szam = szam.replace(c, '') #csak számok kellenek
    szam = szam.split(TIZEDESJEL) #szam[0]: egész rész, szam[1]: tört rész
    egeszresz = tordelo(szam[0])
    if not egeszresz:
        egeszresz = '0'
    try:
        tortresz = TIZEDESJEL + szam[1][0:2]
    except:
        tortresz = ''
    return (elojel + egeszresz + tortresz)

def tordelo (szam):
    """Segédfüggvény az ezres-elválasztóhoz"""
    SZAMVEG = ''
    szam = '0' * (3 - len(szam) % 3) + szam
    x = len(szam)
    jel = SZAMVEG
    tordelt = ''
    while (x - 3) > -1:
        szelet = szam[(x - 3) : x]
        tordelt = szelet + jel + tordelt
        x -= 3
        jel = ELVALASZTO
    return tordelt.lstrip(' .0')

def szamot (szoveg):
    """Számot készít a bemenetről"""
    szoveg = szoveg.replace(ELVALASZTO, '') #ezresválasztó eltüntet
    szoveg = szoveg.replace(TIZEDESJEL, TIZEDESPONT) #tizedesjel pontra
    try:
        return (int(szoveg))
    except:
        return (float(szoveg))
    
