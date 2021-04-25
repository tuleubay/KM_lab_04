import random
from typing import Union
import math
from extended_euclid_integer import euclid
from sympy.ntheory import reduced_totient


def lcm(a, b):
    m = a * b
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return m // (a + b)


def IsPrime(n):
    d = 2
    while d * d <= n and n % d != 0:
        d += 1
    return d * d > n


def jacobi(a: int, n: int) -> int:
    assert (n > a > 0 and n % 2 == 1)
    t = 1
    while a != 0:
        while a % 2 == 0:
            a /= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return t
    else:
        return 0


def from__ascii__to__int(s: str) -> int:
    res = ''
    for i in s:
        res += str(ord(i) + 70)
    return int(res)


def from__int__to__ascii(integer: int) -> str:
    res = ''
    s = str(integer)
    n = int(len(s) / 3)
    try:
        for i in range(n):
            res += chr(int(s[i * 3: i * 3 + 3]) - 70)
    except Exception:
        print('error')
    return res


def carmichael(n: int) -> int:
    coprimes = [x for x in range(1, n) if gcd(x, n) == 1]
    k = 1
    while not all(mod__pow(x, k, n) == 1 for x in coprimes):
        k += 1
    return k


def gen__p__q(l: int) -> int:
    i = '1' + format(random.getrandbits(l - 2), 'b').zfill(l - 2) + '1'
    return int(i, 2)


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def ex__gcd(a: int, b: int) -> Union[tuple[int, int, int], tuple[int, int, Union[int, int]]]:
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = ex__gcd(b, a % b)
        return d, y, x - y * (a // b)


def Miller__Rabin(n: int, r: int, s: int) -> bool:
    a = random.randint(1, n - 1)
    if gcd(a, n) != 1:
        return False
    v = mod__pow(a, r, n)
    if v == 1:
        return True
    for i in range(s):
        if v == n - 1:
            return True
        v = mod__pow(v, 2, n)
    return False


def ferma__test(n: int) -> bool:
    a = random.randint(1, n - 1)
    if mod__pow(a, n - 1, n) != 1:
        return False
    if gcd(a, n) != 1:
        return False
    return True


def Solovay__Strassen(p: int) -> bool:
    a = random.randint(2, p - 1)
    if gcd(a, p) > 1:
        return False
    j = mod__pow(a, (p - 1) // 2, p)
    if j != jacobi(a, p):
        return False
    return True


def final__ferma__and__miller__and__strassen(a: int) -> bool:
    r = a - 1
    s = 0
    while r % 2 == 0:
        s += 1
        r //= 2
    for i in range(100):
        if not ferma__test(a) and not Miller__Rabin(a, r, s) and not Solovay__Strassen(a):
            return False
    return True


def mod__pow(a: int, bits: int, n: int) -> int:
    u = 1
    v = a
    for b in reversed(format(bits, 'b')):
        if b == '1':
            u = (u * v) % n
        v = (v * v) % n
    return u


def Gen(l: int) -> tuple[int, int, int]:
    e = 65537
    if l % 2 == 0:
        q_len = p_len = l >> 1
    else:
        p_len = l >> 1
        q_len = p_len + 1
    p = gen__p__q(p_len)
    q = gen__p__q(q_len)
    while (not final__ferma__and__miller__and__strassen(p)) or gcd(p - 1, e) != 1:
        p = gen__p__q(p_len)
    while (not final__ferma__and__miller__and__strassen(q)) or gcd(q - 1, e) != 1:
        q = gen__p__q(q_len)
    n = p * q
    cc = lcm(carmichael(p), carmichael(q))
    d, x1, y1 = ex__gcd(e, cc)
    # d, x1, y1 = ex__gcd(e, (p - 1) * (q - 1))
    return e, x1, n


def Encr(P: Union[str, int], e: int, n: int) -> int:
    if type(P) is str:
        P = from__ascii__to__int(P)
    return mod__pow(P, e, n)


def Decr(E: int, d: int, n: int, lett: bool) -> Union[str, int]:
    if lett == True:
        return from__int__to__ascii(mod__pow(E, d, n))
    return mod__pow(E, d, n)


def test_gcd():
    print(gcd(879, 978), math.gcd(879, 978))


def test_prime():
    h1 = random.randint(3, 99999)
    h2 = random.randint(3, 99999)
    h3 = 191
    print(final__ferma__and__miller__and__strassen(h1), IsPrime(h1))
    print(final__ferma__and__miller__and__strassen(h2), IsPrime(h2))
    print(final__ferma__and__miller__and__strassen(h3), IsPrime(h3))


def test_mod__pow():
    h1 = random.randint(3, 99999)
    h2 = random.randint(3, 99999)
    h3 = random.randint(3, 99)
    print(mod__pow(h1, h2, h3), pow(h1, h2, h3))


def test_ex():
    h1 = random.randint(3, 99999)
    h2 = random.randint(3, 99999)
    print(ex__gcd(h1, h2), euclid.egcd(h1, h2))


def test_carmichael():
    h1 = random.randint(3, 9999)
    print(carmichael(h1), reduced_totient(h1))


def test_rsa():
    e, d, n = Gen(2048)
    # e = 65537
    # d = 1642554913105628564395954893343539444760772424451951895823770377399415128836648561124357604466515397904620394375421271785745141308240945562133717195154232286835371547054227333987630109832387787351977417242544834829699573958901274186344494836803103698967030384455338013309315576003782935147108783850368336119187022846738806305754290460453987758622620529406505928194827036726039633763251196149598906067362232566424027642649055599294451247684818695173009977236123182498269658742763963617882224224640071409222237549936953869869222961310975543069806457051738982712004100220855393009481519217237257969869051901857691174913
    # n = 30374752071163538155986934493525830866615897963122903892946512196282581630521285764787535080113436690878980470141643309543560757877592226102019589113663352534517422426437047626283102287834423933320130923765423487650683120356803839263673577347507056184876487106673105919371505334243770378311531706320990305938034871925606824969136769844292367164089296122742778406082440766125722538585219362995792313670790133830558171683690413074975370701446843265985790046125139856617634257963802438109041685666526954402999214112724245953069228747348430463570284308777788717956288343197344122639698209305821321211660573627315582159653
    print(Decr(Encr(34567890, e, n), d, n, False))


test_rsa()
