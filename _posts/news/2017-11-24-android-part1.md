---
title:  Android Security - Part 1
author: zangobot
layout: post
category: class
tags: [ ctf, class, zenhack, android ]
---

[Android](https://www.android.com) is such a beautiful world, full of unicorns and...

Wait a minute, is that so?

What is hidden under the hood? This is the core of lesson 2: **Android Security, Part 1**.

[Simone Aonzo (packmad)](https://packmad.github.io/), our Android guru, charmed the audience with his lesson, uncovering what's inside the Android operating system.

Everyone knows that Android applications are written in Java.

This is compiled into Dalvik bytecode, which is executed by a virtual machine.

Bytecode can be decompiled: each .apk can be opened and modified as you please.

**Trust me, I'm not joking at all.**

This is the crucial point of this class: it is easily possible to open an application, modify it and re-compile it again.

This pipeline produces a brand-new application, which could probably behave differently in respect to the original one.
Aren't you satisfied yet?

It's time to dirty your hands! [Here](/assets/news/android_part1/17-11-24.zip) you can download a simple .apk file, crafted by packmad himself.

Using [apk-tools](https://ibotpeaches.github.io/Apktool/) you can decompile it and edit the code... and do very very mean things.

There are hidden flags in that application, can you collect all of them? :-)

Next lesson will cover aspects of Reverse Engineering, stay tuned!

`146 154 141 147 173 142 145 137 163 155 141 162 164 137 142 145 137 141 156 144 162 157 151 144 175` :-D

![alt text](/assets/news/android_part1/cinema.jpg "Android Versions")
* Can you remember each of those Android Version?

![alt text](/assets/news/android_part1/behind.jpg "Is it really Java?")
* Java seen from the cameraman.

![alt text](/assets/news/android_part1/process.jpg "Android processes")
* How Android manages processes.

![alt text](/assets/news/android_part1/blackboard.jpg "Because slides are not enough")
* Connections explained fast.

![alt text](/assets/news/android_part1/hacking-time.jpg "... have you ever seen Kung-Fury?")
* Lesson is over, it's time for a break!

![alt text](/assets/news/android_part1/aonzo.jpg "Our guru in action")
* packmad hacking the application.

![alt text](/assets/news/android_part1/hack.jpg "Thank you!")
* See you next time!
