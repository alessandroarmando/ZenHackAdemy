---
title:  Binary Reversing - Part 2
author: zangobot
layout: post
category: class
tags: [ ctf, class, zenhack, binary, reversing ]
---

The fourth lesson is the natural consequence of its predecessor: **Binary Reversing, Part 2**.

[zxgio](https://csec.it/people/giovanni_lagorio/) begins with the whole suite of [IOLI Crackme binaries](https://github.com/Maijin/Workshop2015/tree/master/IOLI-crackme), using Radare2 to pwn them.

What does `mov` instruction do? And `cmp`?

Or what is that strange `lea eax, [ebp - 120]`?

The ultimate secret to reversing a binary lies in only one word: **Assembly**.

[Assembly](https://en.wikipedia.org/wiki/Assembly_language) (often abbreviated to **asm**) is the nearest programming language to machine instructions.
In the end, every program is translated into Assembly: if you know how to deal with it, you're done with reversing.

Why is Radare2 so useful? It offers a disassembler, a step-by-step debugger, interaction with system registers and so on.
In order to crack the password from those binaries, you need to interact with Radare2, which is not easy at all.

![alt text](https://www.megabeets.net/uploads/r2_learning_curve.png "Radare2 learning curve")

**Want more?** Here you can find [zxgio Radare2 cheatsheet](https://github.com/zxgio/r2-cheatsheet) (for free, of course), which is a useful summary of Radare2 commands. No need to feel lost, just read that sheet!

IOLI Crackme-s were fun to hack, but what about something more difficult?
Just look up at [learning](/learning) section of this website to consider more challenging tasks...

Binary reversing classes are over! Web Security - Part2 is the next lesson to come!

Have fun with Radare2 ;-)

`@iH<,{5vLRWsjmzhZ}L=a^w:H` T.T

![alt text](/assets/news/binary_reversing_part2/adv.jpg "Pre movie advertising")
* A brief introduction before the class.

![alt text](/assets/news/binary_reversing_part2/zxpwn.jpg "zxgio unleashed!")
* zxgio showing how to pwn a binary.

![alt text](/assets/news/binary_reversing_part2/hard_work.jpg "Working hard.")
* Students are working hard. Keep calm and reverse that binary.

![alt text](/assets/news/binary_reversing_part2/ribba2.jpg "AH!")
* Even Prof. Ribaudo has been spotted reversing binaries!

![alt text](/assets/news/binary_reversing_part2/glibberish.jpg "Another point of view")
* Radare2 here, Radare2 there.

![alt text](/assets/news/binary_reversing_part2/zxgiopwn2.jpg "The power of Radare2!")
* Assembly is strong in this man.

![alt text](/assets/news/binary_reversing_part2/thankyou.jpg "Thank you!")
* See you next class!
