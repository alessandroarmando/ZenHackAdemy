---
title:  Binary Reversing - Part 1
author: zangobot
layout: post
category: class
tags: [ ctf, class, zenhack, binary, reversing ]
---

You successfully downloaded "MoneySafeMultiplier.exe", because you are an optimistic guy who firmly believes that evil things only happen in movies.
Then, your computer is entirely encrypted, and you're asked to send 100 [Bitcoins](https://bitcoin.org/it/) to **3v1lH4ck3r** to restore your files.

That's incredible! Isn't it?

If only you performed a static or dynamic analysis on that binary...  which is the core of the third lesson: **Binary Reversing - Part1**.

Our commander-in-chief [Giovanni Lagorio (zxgio)](https://csec.it/people/giovanni_lagorio/) introduces the audience to [Radare2](http://www.radare.org/r), an open source software which is widely used in binary reversing.

It can disassemble a binary, attach to a debugger, emulate code, rename labels and so on.

Radare2 is hard to master, there are plenty of features that need to be explored.

**But it is a shot worth taking.**

zxgio used some simple binaries to show the potential of Radare2, they can be found on the internet as [IOLI Crackme](https://github.com/Maijin/Workshop2015/tree/master/IOLI-crackme).

IOLI Crackmes are very useful to learn some binary reversing techniques, which don't only concern Radare2, but the UNIX environment itself.

For example, use the `strings` command to search for a hardcoded password in the binary... :-D

Next lesson will cover other aspects of Binary Reversing.
Until then, practice with Radare2 and have fun!

`++++++++++[>+>+++>+++++++>++++++++++<<<<-]>>>>++.++++++.-----------.++++++.++++++++++++++++++++.---------.-----------------.+++.---.+++++++++++++++++.-------------.<<++++++++++++++++++++.>>------.++++++++++.++++++++++.--------------------.++++.+++++.---.----.+++++++++++++++.+++++++++++++.`

O__O

![alt text](/assets/news/binary_reversing_part1/1.jpg "Radare2")
* Radare2 is not an easy task...

![alt text](/assets/news/binary_reversing_part1/2.jpg "Just do it!")
* Binary reversing is challenging!

![alt text](/assets/news/binary_reversing_part1/3.jpg "What is that?")
* Prof. Lagorio explains how things need to be done.

![alt text](/assets/news/binary_reversing_part1/4.jpg "Bye!")
* Thank you and see you soon!
