---
ctf: HackCon'18
challenge: Diversity
author: pianka
layout: writeup
categories: [crypto]
tags: [ ctf, challenge, crypto, write-up ]
date: 2018-8-17
---

In this write-up I'll cover how I solved the **Diversity** crypto challenge during HackCon'18.

> So much diversity, my mind boggles..!
>
> ```
b1001000 x69 d33 d32 o127 b1100101 o154 o143 b1101111 o155 o145 d32 o164 d111 d32 x48 b1100001 x63 o153 b1000011 o157 x6e d39 o61 b111000 x2c d32 d111 b1110010 d103 d97 x6e o151 x73 d101 d100 o40 d97 b1110011 b100000 x70 o141 o162 x74 d32 x6f x66 b100000 o105 b1110011 x79 b1100001 d39 d49 b111000 x20 b1100010 d121 b100000 x49 o111 b1001001 x54 b100000 b1000100 x65 x6c o150 x69 b101110 x20 o111 d110 b100000 o143 d97 d115 o145 o40 b1111001 b1101111 x75 b100111 x72 x65 x20 x73 x65 b1100101 b1101011 x69 o156 x67 d32 b1100001 o40 o162 x65 o167 b1100001 o162 o144 d32 x66 d111 x72 b100000 o171 x6f d117 b1110010 o40 d101 x66 x66 x6f x72 d116 o163 x2c b100000 d104 b1100101 d114 o145 x27 d115 x20 b1100001 d32 d102 d108 b1100001 x67 x20 x3a b100000 o144 x34 o162 x6b x7b o151 d95 d87 o151 x73 b100011 d95 x41 o61 x6c d95 b1110100 d52 d115 b1101011 d53 o137 o167 x33 d114 o63 o137 d116 b1101000 o151 o65 x5f x33 d52 o65 o171 o137 x58 b1000100 b1000100 b1111101 x63 d48 d100 d101 d46 b100000 o101 x6e b1111001 d119 b1100001 b1111001 x73 b101100 x20 o150 d111 b1110000 b1100101 o40 x79 o157 d117 b100000 b1101000 o141 x76 x65 b100000 d97 x20 o147 d111 b1101111 d100 b100000 b1110100 b1101001 d109 b1100101 d32 x3b x29
> ```

Just giving a look to this problem I thought those numbers where probably the ASCII representation of a text containing the flag, each number in a different base defined by the first char (b = base 2, o = base 8, d = base 10, x = base 16). I was aware it could also have been encrypted in some way, but why not trying.

The python code is not so difficult and simply checks the first char of each word to get if it is in base 2, 8, 10 or 16. Then convert it in integer and in char.

Note that the `int` function in Python accept the base as the second parameter.

```python
s = 'b1001000 x69 d33 ... d32 x3b x29'

for a in s.split():
    if a[0] == 'b':
        c = chr(int(a[1:], 2))
    elif a[0] == 'x':
        c = chr(int(a[1:], 16))
    elif a[0] == 'd':
        c = chr(int(a[1:]))
    elif a[0] == 'o':
        c = chr(int(a[1:], 8))
    print(c, end='')
print()
```

Simply run it and get

```console
Hi! Welcome to HackCon'18, organised as part of Esya'18 by IIIT Delhi. In case you're seeking a reward for your efforts, here's a flag : d4rk{i_Wis#_A1l_t4sk5_w3r3_thi5_345y_XDD}c0de. AAyways, hope you have a good time ;)
```

Full code on my [GitHub](https://github.com/LorenzoLeonardini/CTF-Solves/tree/master/HackCon2018/Diversity)
