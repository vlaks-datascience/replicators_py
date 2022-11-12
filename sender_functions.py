import receiverProperty
import time


def konvertuj_u_receiver_property(data):
    if str(data).rfind(";") == -1:
        return "lose"
    split_karakter = ";"
    podatak = data.split(split_karakter)
    if (len(data.split(split_karakter))) != 2:
        return "lose"
    code = podatak[0]
    c = int(code) if code.isdigit() else 666  # PROVERA DA LI SMO PRIMILI BROJ
    
    value = podatak[1]
    v = int(value) if value.isdigit() else 666  # PROVERA DA LI SMO PRIMILI BROJ
    a = receiverProperty.ReceiverProperty(int(c), int(v))
    return a


def logger(tekst):
    vreme = time.localtime()
    with open("sender.txt", 'a') as f:
        ispis = f"{vreme.tm_mday}.{vreme.tm_mon}.{vreme.tm_hour}, " \
                f"{vreme.tm_hour}:{vreme.tm_min}:{vreme.tm_sec}, {tekst}\n"
        f.write(ispis)
        return ispis
