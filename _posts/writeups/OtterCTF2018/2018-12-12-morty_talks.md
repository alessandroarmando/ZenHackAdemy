---
author: enriquez - zangobot
ctf: OtterCTF
challenge: Morty Talks
categories: [forensics]
tags: [ ctf, challenge, write-up, forensics]
layout: writeup
---

The flag is encrypted inside a pcap file, the encryption algorithm is given as a python program:

```python
data = pickle.load(open(r"1.pc", 'rb'))
KEY = open("key.txt", 'r').read()
p = 0
s = socket.socket()
s.bind(("0.0.0.0", PORT))
s.listen(0)
s, addr = s.accept()
for msg in data:
    res = KEY[p]
    for i in xrange(len(msg)):
        res+= chr(ord(msg[i])^ord(KEY[i % (p+1)]))
    s.send(res)
    KEY = KEY[:p+1] + s.recv(1) + KEY[p+1:]
    p += 2
```
Basically, it opens a file and it xors all the messages contained using a key (which is hidden).
In fact, only part of the key is used for encrypting the message:

```python
res = KEY[p]
for i in xrange(len(msg)):
    res+= chr(ord(msg[i])^ord(KEY[i % (p+1)]))
s.send(res)
KEY = KEY[:p+1] + s.recv(1) + KEY[p+1:]
p += 2
```
at the first iteration, it uses only the **first** byte of the key, then only the first three and so on.
There is more: as you may notice, the first char of the message is the p-th byte of the key, which is not encrypted.
Again, the key is updated with the first char of the incoming message.

To sum up: the even bytes of the key are sent by the server as the first char of the message to send **AND** the odd bytes of the key are sent by the client as the first char of the incoming message.

So, the key is in the pcap file, that is full of browser comunications (someone said [GQUIC](https://www.wireshark.org/docs/dfref/g/gquic.html)?).
The culprit is contained into a TCP connection, hence we are able to collect the key by applying the idea summarized above.
The final key is the following:
```python
FINAL_KEY = [ ord(i) for i in 'Morty Smith (voiced by Justin Roiland[1]) \x96 Rick\'s 14-year-old grandson who is frequently dragged into Rick\'s misadventures. Morty is a good kid but he is easily distressed. He is often reluctant to follow Rick\'s plans, and he often ends up traumatized by the unorthodox and morally questionable methods Rick uses to \'fix\' situations. The main Morty the episodes follow is referred to as the "Mortiest Morty" by Rick due to his courage, which nearly every other Morty lacks due to their main use being makeshift cloaking device']
```
**BUT!** You notice the ```\x96``` char? Well, it is not a single value inside the message, so if you combine the even and odd bytes, those three character will be scrambled across the message, leading to a wrong key.

[Here](/assets/writeups/OtterCTF2018/morty_talks/morty_talks_files.zip) you can have a view to the file we used for the challenge.

By decoding all the messages we obtain the flag:  ```CTF{L0ng_L!v3_Ev!l_M0rtY}```.
