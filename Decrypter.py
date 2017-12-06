from __future__ import print_function
import sys


def rsaDecrypt(cipherText, p, q, d):

    n = p * q
    print(n)

    b1 = d % (p - 1)                # 8268073946895032669 mod 4294404460 = 1776994949
    b2 = d % (q - 1)                # 8268073946895032669 mod 4294929630 = 1629111239

    b1_0 = b1 % 100                         # 49
    b1_2 = b1 % 10000 // 100                # 49
    b1_4 = b1 % 1000000 // 10000            # 99
    b1_6 = b1 % 100000000 // 1000000        # 76
    b1_8 = b1 % 10000000000 // 100000000    # 17

    b2_0 = b2 % 100                         # 39
    b2_2 = b2 % 10000 // 100                # 12
    b2_4 = b2 % 1000000 // 10000            # 11
    b2_6 = b2 % 100000000 // 1000000        # 29
    b2_8 = b2 % 10000000000 // 100000000    # 16

    c1_0 = cipherText % p                 # 21 % 4294404461 = 21
    c2_0 = cipherText % q                 # 21 % 4294929631 = 21
    c1_2 = pow(c1_0, 100) % p             # 21^100 % 4294404461 = 741943163
    c2_2 = pow(c2_0, 100) % q             # 21^100 % 4294929631 = 1195161872
    c1_4 = pow(c1_2, 100) % p             # 21^10000 % 4294404461 = 2873263239
    c2_4 = pow(c2_2, 100) % q             # 21^10000 % 4294929631 = 1888612520
    c1_6 = pow(c1_4, 100) % p             # 21^1000000 % 4294404461 = 102100368
    c2_6 = pow(c2_4, 100) % q             # 21^1000000 % 4294929631 = 1006495491
    c1_8 = pow(c1_6, 100) % p             # 21^100000000 % 4294404461 = 4146719637
    c2_8 = pow(c2_6, 100) % q             # 21^100000000 % 4294929631 = 2319405837

    # 21^1776994949 mod p = [(21 mod p)^49 * (21^100 mod p)^49 * (21^10000 mod p)^99 * (21^1000000 mod p)^76 * (21^100000000 mod p)^17] mod p
    # 21^1629111239 mod q = [(21 mod q)^39 * (21^100 mod q)^12 * (21^10000 mod q)^11 * (21^1000000 mod q)^29 * (21^100000000 mod q)^16] mod q

    print("a1 & a2")
    a1_0 = (pow(c1_0, b1_0)) % p        # ((21 mod p)^49) mod p
    a1_2 = (pow(c1_2, b1_2)) % p        # ((21^100 mod p)^49) mod p
    a1_4 = (pow(c1_4, b1_4)) % p        # ((21^10000 mod p)^99) mod p
    a1_6 = (pow(c1_6, b1_6)) % p        # ((21^1000000 mod p)^76) mod p
    a1_8 = (pow(c1_8, b1_8)) % p        # ((21^100000000 mod p)^17) mod p
    a1 = (a1_0 * a1_2 * a1_4 * a1_6 * a1_8) % p
    print(a1)

    a2_0 = (pow(c2_0, b2_0)) % q        # ((21 mod p)^49) mod p
    a2_2 = (pow(c2_2, b2_2)) % q        # ((21^100 mod p)^49) mod p
    a2_4 = (pow(c2_4, b2_4)) % q        # ((21^10000 mod p)^99) mod p
    a2_6 = (pow(c2_6, b2_6)) % q        # ((21^1000000 mod p)^76) mod p
    a2_8 = (pow(c2_8, b2_8)) % q        # ((21^100000000 mod p)^17) mod p
    a2 = (a2_0 * a2_2 * a2_4 * a2_6 * a2_8) % q
    print(a2)

    print("w1 & w2")
    w1 = q * (modinv(q, p))             # 4294929631 * 4294929631^(-1) mod 4294404461
    print(w1)

    w2 = p * (modinv(p, q))             # 4294404461 * 4294404461^(-1) mod 4294929631
    print(w2)

    h = (a1 * w1) + (a2 * w2)

    result = h % n

    return result


def elGamalDecrypt(c1, c2, q, a, yA):

    c1 = int(c1)
    c2 = int(c2)
    x = 1463333871
    a_2 = pow(a, 100) % q           # 43^100 % 1605333871 = 151276390
    a_4 = pow(a_2, 100) % q         # 43^10000 % 1605333871 = 1356017243
    a_6 = pow(a_4, 100) % q         # 43^1000000 % 1605333871 = 637875534
    a_8 = pow(a_6, 100) % q         # 43^100000000 % 1605333871 = 1142500698

    crack = 0
    while yA != crack:

        x -= 1

        x_0 = x % 100
        x_2 = x % 10000 // 100
        x_4 = x % 1000000 // 10000
        x_6 = x % 100000000 // 1000000
        x_8 = x % 10000000000 // 100000000

        if x < 100:
            crack = pow(a, x_0) % q
            if crack < 1000:
                print(crack)
                print("x", end=' = ')
                print(x)

        elif x < 10000:
            crack = ((pow(a, x_0) % q) * (pow(a_2, x_2) % q)) % q
            if crack < 1000:
                print(crack)
                print("x", end='')
                print(x)

        elif x < 1000000:
            crack = ((pow(a, x_0) % q) * (pow(a_2, x_2) % q) * (pow(a_4, x_4) % q)) % q
            if crack < 1000:
                print(crack)
                print("x", end='')
                print(x)

        elif x < 100000000:
            crack = ((pow(a, x_0) % q) * (pow(a_2, x_2) % q) * (pow(a_4, x_4) % q) * (pow(a_6, x_6) % q)) % q
            if crack < 1000:
                print(crack)
                print("x", end='')
                print(x)

        elif x < 10000000000:
            crack = ((pow(a, x_0) % q) * (pow(a_2, x_2) % q) * (pow(a_4, x_4) % q) * (pow(a_6, x_6) % q) * (pow(a_8, x_8) % q)) % q
            if crack < 1000:
                print(crack)
                print("x", end='')
                print(x)

    print("crack = ", end='')
    print(crack)
    print("x = ", end='')
    print(x)

    x_0 = x % 100                       # 57
    x_2 = x % 10000 // 100              # 99
    x_4 = x % 1000000 // 10000          # 15
    x_6 = x % 100000000 // 1000000      # 63
    x_8 = x % 10000000000 // 100000000  # 14

    c1_2 = pow(c1, 100) % q             # c1^100 % 1605333871
    c1_4 = pow(c1_2, 100) % q           # c1^10000 % 1605333871
    c1_6 = pow(c1_4, 100) % q           # c1^1000000 % 1605333871
    c1_8 = pow(c1_6, 100) % q           # c1^100000000 % 1605333871

    k_0 = (pow(c1, x_0)) % q            # ((c1 mod q)^57) mod q
    k_2 = (pow(c1_2, x_2)) % q          # ((c1^100 mod q)^99) mod q
    k_4 = (pow(c1_4, x_4)) % q          # ((c1^10000 mod q)^15) mod q
    k_6 = (pow(c1_6, x_6)) % q          # ((c1^1000000 mod q)^63) mod q
    k_8 = (pow(c1_8, x_8)) % q          # ((c1^100000000 mod q)^14) mod q

    keyK = (k_0 * k_2 * k_4 * k_6 * k_8) % q
    result = (c2 * modinv(keyK, q)) % q

    return result


def extendEuclid(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        q, y, x = extendEuclid(b % a, a)
        return (q, x - (b // a) * y, y)


def modinv(a, m):
    q, x, y = extendEuclid(a, m)
    if q != 1:
        raise Exception('no inverse')
    else:
        return x % m


def main():

    while True:
        print("")
        option = int(input("What would you like to do? : 1 for RSA, 2 for El Gamal, 0 for Exit : "))

        if option == 1:

            print("Enter ciphertext...")
            print("3540 --> 6835383948117812667")
            print("173 --> 10824463971351777081")
            cipherText = int(input("What is the ciphertext? (ex:21) : "))

            e = 29                      # receiver public key
            n = 18444164967047483891    # (64-bit) --> 4294404461, 4294929631 (used magma calculator)
            p = 4294404461
            q = 4294929631

            phi = (p - 1) * (q - 1)
            d = modinv(e, phi)          # 8268073946895032669

            print("")
            print("Decrypting...")

            result = rsaDecrypt(cipherText, p, q, d)

            print("Result : ", end='')
            print(result)

        elif option == 2:

            print("Enter Cipher Text 1...")
            print("79610 --> c1 = 187341129, c2 = 50696994")
            print("21 --> c1 = 187341129, c2 = 1212049520")
            c1 = int(input("What is the c1? (ex:187341129) : "))

            print("Enter Cipher Text 2...")
            c2 = int(input("What is the c2? (ex:881954783) : "))

            q = 1605333871  # 32-bit GF(1605333871)
            a = 43          # primitive root of q
            yA = 22         # receiver public key

            print("")
            print("Decrypting...")

            result = elGamalDecrypt(c1, c2, q, a, yA)

            print("Result : ", end='')
            print(result)

        elif option == 0:
            print("Bye Bye!")
            sys.exit()

        else:
            print("I don't understand...")
            continue

########################################################################


if __name__ == '__main__':
    main()
