import random


def lenDigits(x):
    x = abs(x)
    if x < 10:
        return 1
    return 1 + lenDigits(x / 10)


def A3(Ki, Rand):
    kbl = Ki[0:64]
    kbr = Ki[64:]
    mbr = Rand[0:64]
    mbl = Rand[64:]
    a1 = int(kbl, 2) ^ int(mbr, 2)
    a2 = int(kbr, 2) ^ int(mbl, 2)
    a3 = a1 ^ a2
    a4 = bin(a3)[2:].zfill(64)
    a5 = a4[0:32]
    a6 = a4[32:]
    a7 = int(a5, 2) ^ int(a6, 2)
    SRES = bin(a7)[2:].zfill(len(a5))
    return SRES


def A8(Ki, Rand):
    Kc = Ki+Rand
    return Kc


def Auc(ki, pin):
    if len(ki) == 128 and pin == 1234:
        print("User Authenticated")
        m = random.getrandbits(128)
        Rand = bin(m)[2:]
        print("128 Random Bits Generated = ", Rand)
        SRES = A3(Ki, Rand)
        print("Sres Generated = ", SRES)
        Kc = A8(Ki, Rand)
        print("Cipher Generated = ", Kc)
        return Kc, SRES, Rand
    else:
        print("Fake User")
        return 0, 0, 0


def MscStore(Kc, SRES, Rand, stored):
    stored.append(SRES)
    stored.append(Kc)
    return Rand, stored


def MscAuc(Received, stored):
    if Received == stored:
        print("Call Successful")
    else:
        print("MSC Authenication Unsuccesful")


print("Assume you have a MS")
k = random.getrandbits(127) + (1 << 127)
Ki = bin(k)[2:]
print("This MS has key ki: ", Ki)
print("length: ", len(Ki))
pin = 1234

print("And pin= ", pin)
option = int(input("Using this u can call jhon or not press 1 to call jhon: "))
if option == 1:
    stored = []
    Received = []
    Kc, SRES, Rand = Auc(Ki, pin)
    if Kc == 0:
        print("Error")
    else:
        MscStore(Kc, SRES, Rand, stored)
        print("MS only Receives Random number = ", Rand)
        print("MS uses this Random Number With the Key to generate SRES and Ciper key using A3 and A8 algoritms")
        A3 = A3(Ki, Rand)
        A8 = A8(Ki, Rand)
        print("Generated SRES: ",A3)
        print("Generated Cipher key: ",A8)
        Received.append(A3)
        Received.append(A8)
        print("MS sends them to the MSC to authenticate and connect the call")
        MscAuc(Received, stored)
else:
    print("Run app again to call")
