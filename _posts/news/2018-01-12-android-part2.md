---
title:  Android Security - Part 2
author: zangobot
layout: post
category: class
tags: [ ctf, class, zenhack, android ]
---

You learned that Android is not the peaceful world it was supposed to be.

But you keep believing that there are still plenty of polite ladies and gentleman outside your room.

**Maybe on the internet?**

What do you know about [Man in the Middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack)?

 If this doesn't sound any bell in your head, you should check it out now...

Luckily for you, here we come: **Android Security, Part 2**.

[packmad](https://packmad.github.io/) explains what a  Man in the Middle attack is.  

Basically, it is just someone who is overhearing your private conversation with others.

Who knows what happens in the middle of the communication channel? Have we a chance to discover if our communication has been intercepted?

If your data are not encrypted, and someone or something is spying on the internet, all your secrets are revealed.

Encryption needs to be used! In this lesson we will see how interact:
1. [Symmetric-key encryption](https://en.wikipedia.org/wiki/Symmetric-key_algorithm)
2. [Public-key cryptography](https://en.wikipedia.org/wiki/Public-key_cryptography)
3. [Digital Certificates](https://en.wikipedia.org/wiki/Public_key_certificate).

Long story short: a certificate is a file which delivers a public key to be used for exchanging a symmetric key.

Only the ones with the counterpart private key will be able to decrypt the message. If you trust the use of a certificate, then you can assume that digital certificate is not compromised. But there are subtle details!

**Or should you?**

This concludes the final lesson on Android.

Next class will deal with CTFs writeups and maybe something more...

See you next Friday!

`['0x66', '0x6d', '0x63', '0x6a', '0x7f', '0x74', '0x7c', '0x6c', '0x7a', '0x71', '0x6f', '0x6c', '0x7e', '0x76', '0x7c', '0x76', '0x6f', '0x7a', '0x85', '0x72', '0x76', '0x76', '0x7a', '0x94']` ^.^

![alt text](/assets/news/android_part2/starting.jpg "packmad starts the class")
* First memorable slide.

![alt text](/assets/news/android_part2/mitm.jpg "A blackboard.")
* MITM explained on a blackboard.

![alt text](/assets/news/android_part2/traffic.jpg "... what does A said?")
* There are packets in the air!

![alt text](/assets/news/android_part2/certificate.jpg "Asymmetrical encryption")
* Digital certificates are the answer... or maybe not?

![alt text](/assets/news/android_part2/behind.jpg "See you next time!")
* Thank you, see you soon ;-)
