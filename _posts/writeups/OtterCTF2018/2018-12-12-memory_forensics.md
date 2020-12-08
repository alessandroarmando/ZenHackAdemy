---
author: Giotino - Killua 
ctf: OtterCTF
challenge: Memory Forensics
categories: [forensics]
tags: [ ctf, challenge, write-up, forensics, volatility ]
layout: writeup
---

In this write up we will discuss all the moemry forensic challenges, and you can find [here](https://mega.nz/#!sh8wmCIL!b4tpech4wzc3QQ6YgQ2uZnOmctRZ2duQxDqxbkWYipQ) all the memory dumps produced using [volatility](https://www.volatilityfoundation.org/) (and strings command :P). 

A special thanks to dfirfpi (our guru in memory forensics) who solved and helped us to solve most of these challenges.
We will only show a correct way to solve it, not all the failed attempts. 

First of all, we need to find the **image profile**:

```console
$ vol.py -f OtterCTF.vmem imageinfo

INFO    : volatility.debug    : Determining profile based on KDBG search...
          Suggested Profile(s) : Win7SP1x64, Win7SP0x64, Win2008R2SP0x64, Win2008R2SP1x64_24000, Win2008R2SP1x64_23418, Win2008R2SP1x64, Win7SP1x64_24000, Win7SP1x64_23418
                     AS Layer1 : WindowsAMD64PagedMemory (Kernel AS)
```

We are now ready to solve the challenges!


## 1 - What the password? - 100 Points
>You got a sample of rick's PC's memory. can you get his user password? 
>Format: CTF{...}

Let's start with a simple one, dfirfpi developed a plugin for volatility that basically did the entire job: [mimikatz](https://github.com/sans-dfir/sift-files/blob/master/volatility/mimikatz.py)

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 mimikatz

Module   User             Domain           Password                                
-------- ---------------- ---------------- ----------------------------------------
wdigest  Rick             WIN-LO6FAF3DTFE  MortyIsReallyAnOtter                    
wdigest  WIN-LO6FAF3DTFE$ WORKGROUP
```
Hurray! First flag: `CTF{MortyIsReallyAnOtter}`


## 2 - General Info - 75 Points
>Let's start easy - whats the PC's name and IP address?

One of them was already found using mimikatz `CTF{WIN-LO6FAF3DTFE}`  
The other one could be found using the netscan plugin for volatility

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 netscan

Offset(P)          Proto    Local Address                  Foreign Address      State            Pid      Owner          Created
0x7d60f010         UDPv4    0.0.0.0:1900                   *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
0x7d62b3f0         UDPv4    192.168.202.131:6771           *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:22 UTC+0000
0x7d62f4c0         UDPv4    127.0.0.1:62307                *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
0x7d62f920         UDPv4    192.168.202.131:62306          *:*                                   2836     BitTorrent.exe 2018-08-04 19:27:17 UTC+0000
...
0x7d9e19e0         TCPv4    0.0.0.0:20830                  0.0.0.0:0            LISTENING        2836     BitTorrent.exe 
0x7d9e19e0         TCPv6    :::20830                       :::0                 LISTENING        2836     BitTorrent.exe 
0x7d9e1c90         TCPv4    0.0.0.0:20830                  0.0.0.0:0            LISTENING        2836     BitTorrent.exe 
0x7d42ba90         TCPv4    -:0                            56.219.196.26:0      CLOSED           2836     BitTorrent.exe 
0x7d6124d0         TCPv4    192.168.202.131:49530          77.102.199.102:7575  CLOSED           708      LunarMS.exe    
```

Here it is `CTF{192.168.202.131}`


## 3 - Play Time - 50 Points
>Rick just loves to play some good old videogames. can you tell which game is he playing? whats the IP address of the server?

Two other flags for free:
- `CTF{LunarMS}` from process list
- `CTF{77.102.199.102}` from netscan


## 4 - Name Game - 100 Points
>We know that the account was logged in to a channel called Lunar-3. what is the account name?

A very naive way to solve this challenge is to invoke the **strings** command:

```console
$ strings OtterCTF.vmem | grep username

...
usernamerickopicko@mail.com
username
/username:%s
staticusername:
secure.toolbarhost.com/_scripts/checktb.php?username=
Digest username=
https://www.mail.com/int/usernamepasswordhttps://www.mail.com/
?	http://lunarms.zapto.org/username0tt3r8r33z3passwordhttp://lunarms.zapto.org/
.top .info .username lEv)$
username=%s&number=%s&dialerid=%s&maxtime=%d
wait_for_username
form_contains_fillable_username_field
username_field_name empty
...
```

There are two options: `rickopicko@mail.com` and `0tt3r8r33z3`. 
Only the second one is the correct answer: `CTF{0tt3r8r33z3}`


## 5 - Name Game 2 - 150 Points
>From a little research we found that the username of the logged on character is always after this signature: 0x64 0x??{6-8} 0x40 0x06 0x??{18} 0x5a 0x0c 0x00{2}>What's rick's character's name? format:

The username should be in the dump of the client memory, so let's get it.
```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 memdump -D . -p 708
```
Then we search the signature (we use a portion of the real signature, that is `5A 0C 00 00` beacause it was easier) with an hexeditor and read the following bytes.
There are only 185 occurency: by reading them one by one we find that the 40th is the correct one: `5A 0C 00 00 4D 30 72 74 79 4C 30 4C`.
Here's the flag: `CTF{M0rtyL0L}`


## 6 - Silly Rick - 100 Points
>Silly rick always forgets his email's password, so he uses a Stored Password Services online to store his password. He always copy and paste the password so he will not get it wrong. whats rick's email password?

Another challenge, another volatility's plugin: clipboard

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 clipboard

Session    WindowStation Format                         Handle Object             Data                                              
---------- ------------- ------------------ ------------------ ------------------ --------------------------------------------------
         1 WinSta0       CF_UNICODETEXT                0x602e3 0xfffff900c1ad93f0 M@il_Pr0vid0rs                                    
         1 WinSta0       CF_TEXT                          0x10 ------------------                                                   
         1 WinSta0       0x150133L              0x200000000000 ------------------                                                   
         1 WinSta0       CF_TEXT                           0x1 ------------------                                                   
         1 ------------- ------------------           0x150133 0xfffff900c1c1adc0                                                   
```

Flag: `CTF{M@il_Pr0vid0rs}`


## 7 - Hide And Seek - 100 Points
>The reason that we took rick's PC memory dump is because there was a malware infection. Please find the malware process name (including the extension)

Let's have a look into the running processes:

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 pstree

Name                                                  Pid   PPid   Thds   Hnds Time
-------------------------------------------------- ------ ------ ------ ------ ----
 0xfffffa801b27e060:explorer.exe                     2728   2696     33    854 2018-08-04 19:27:04 UTC+0000
. 0xfffffa801b486b30:Rick And Morty                  3820   2728      4    185 2018-08-04 19:32:55 UTC+0000
.. 0xfffffa801a4c5b30:vmware-tray.ex                 3720   3820      8    147 2018-08-04 19:33:02 UTC+0000
. 0xfffffa801b2f02e0:WebCompanion.e                  2844   2728      0 ------ 2018-08-04 19:27:07 UTC+0000
. 0xfffffa801a4e3870:chrome.exe                      4076   2728     44   1160 2018-08-04 19:29:30 UTC+0000
.. 0xfffffa801a4eab30:chrome.exe                     4084   4076      8     86 2018-08-04 19:29:30 UTC+0000
.. 0xfffffa801a5ef1f0:chrome.exe                     1796   4076     15    170 2018-08-04 19:33:41 UTC+0000
.. 0xfffffa801aa00a90:chrome.exe                     3924   4076     16    228 2018-08-04 19:29:51 UTC+0000
.. 0xfffffa801a635240:chrome.exe                     3648   4076     16    207 2018-08-04 19:33:38 UTC+0000
.. 0xfffffa801a502b30:chrome.exe                      576   4076      2     58 2018-08-04 19:29:31 UTC+0000
.. 0xfffffa801a4f7b30:chrome.exe                     1808   4076     13    229 2018-08-04 19:29:32 UTC+0000
.. 0xfffffa801a7f98f0:chrome.exe                     2748   4076     15    181 2018-08-04 19:31:15 UTC+0000
. 0xfffffa801b5cb740:LunarMS.exe                      708   2728     18    346 2018-08-04 19:27:39 UTC+0000
. 0xfffffa801b1cdb30:vmtoolsd.exe                    2804   2728      6    190 2018-08-04 19:27:06 UTC+0000
. 0xfffffa801b290b30:BitTorrent.exe                  2836   2728     24    471 2018-08-04 19:27:07 UTC+0000
.. 0xfffffa801b4c9b30:bittorrentie.e                 2624   2836     13    316 2018-08-04 19:27:21 UTC+0000
.. 0xfffffa801b4a7b30:bittorrentie.e                 2308   2836     15    337 2018-08-04 19:27:19 UTC+0000
 0xfffffa8018d44740:System                              4      0     95    411 2018-08-04 19:26:03 UTC+0000
...               
```

Do you notice something? What about vmware-tray.exe, it could be a genuine process, but it's PPid is Rick & Morty, that's odd, and probably that's our malware `CTF{vmware-tray.exe}`.

## 8 - Path To Glory - 150 Points
>How did the malware got to rick's PC? It must be one of rick old illigal habits...

Well we thought that obviously it got to rick's PC via `torrent`, judging by the traces found in the other challenges, so we tried `CTF{torrent}`, but nothing... 
Let's go deeper in the torrent file.

First find the torrent file:

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 filescan | grep "Rick And Morty"

0x000000007d63dbc0     10      0 R--r-d \Device\HarddiskVolume1\Torrents\Rick And Morty season 1 download.exe
0x000000007d8813c0      2      0 RW-rwd \Device\HarddiskVolume1\Users\Rick\Downloads\Rick And Morty season 1 download.exe.torrent
0x000000007da56240      2      0 RW-rwd \Device\HarddiskVolume1\Torrents\Rick And Morty season 1 download.exe
0x000000007dae9350      2      0 RWD--- \Device\HarddiskVolume1\Users\Rick\AppData\Roaming\BitTorrent\Rick And Morty season 1 download.exe.1.torrent
0x000000007dcbf6f0      2      0 RW-rwd \Device\HarddiskVolume1\Users\Rick\AppData\Roaming\BitTorrent\Rick And Morty season 1 download.exe.1.torrent
0x000000007e710070      8      0 R--rwd \Device\HarddiskVolume1\Torrents\Rick And Morty season 1 download.exe    
```

Let's extract it and fetch all strings:

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 dumpfiles -Q 0x000000007dae9350 -D .

DataSectionObject 0x7dae9350   None   \Device\HarddiskVolume1\Users\Rick\AppData\Roaming\BitTorrent\Rick And Morty season 1 download.exe.1.torrent


$ strings file.None.0xfffffa801b42c9e0.dat

d8:announce44:udp://tracker.openbittorrent.com:80/announce13:announce-listll44:udp://tracker.openbittorrent.com:80/announceel42:udp://tracker.opentrackr.org:1337/announceee10:created by17:BitTorrent/7.10.313:creation datei1533150595e8:encoding5:UTF-84:infod6:lengthi456670e4:name36:Rick And Morty season 1 download.exe12:piece lengthi16384e6:pieces560:\I
!PC<^X
B.k_Rk
0<;O87o
!4^"
3hq,
&iW1|
K68:o
w~Q~YT
$$o9p
bwF:u
e7:website19:M3an_T0rren7_4_R!cke
```

Mmm the final strings looks suspicious, that's the flag! `CTF{M3an_T0rren7_4_R!ck}`.


## 9 - Path To Glory 2 - 200 Points
>Continue the search after the the way that malware got in.
 
The torrent file has to come from somewhere, looking at the processes I think Chrome is the best option.

After dumping the memory of all Chrome's processes we proceed to search for the file name:

```console
$ strings ./dumps/* | grep "download\.exe\.torrent"

...
Content-Disposition: attachment; filename="Rick And Morty season 1 download.exe.torrent"
attachment; filename="Rick And Morty season 1 download.exe.torrent"
Download complete: Rick And Morty season 1 download.exe.torrent. Press Shift+F6 to cycle to the downloads bar area.
```

These last three results are important, because now we know for sure that the torrent file was downloaded using the chrome web browser.

So let's inspect the output of grep, by including more lines to the result: 

```console
$ strings ./dumps/* | grep -B12 -A12 "download\.exe\.torrent"

SPnvideo-label video-title trc_ellipsis  ]"sAE=
display:inline;width:56px;height:200px;m>
Hum@n_I5_Th3_Weak3s7_Link_In_Th3_Ch@inYear
//sec-s.uicdn.com/nav-cdn/home/preloader.gif
simple-icon_toolbar-change-view-horizontal
 nnx-track-sec-click-communication-inboxic.com
nx-track-sec-click-dashboard-hide_smileyable
Nftd-box stem-north big fullsize js-focusable
js-box-flex need-overlay js-componentone
Jhttps://search.mail.com/web [q origin ]Year
ntrack-and-trace__delivery-info--has-iconf
Rick And Morty season 1 ESC[01;31mESC[Kdownload.exe.torrentESC[mESC[K
tbl_1533411035475_7.0.1.40728_2033115181
panel-mail-display-table-mail-default35"
Cnpanel-mail-display-table-mail-horizontal.js
trc_rbox text-links-a trc-content-sponsored
...
```

Luckily near the first result we see something that seems to be our flag `Hum@n_I5_Th3_Weak3s7_Link_In_Th3_Ch@inYear`.
Hence, the correct answer is `CTF{Hum@n_I5_Th3_Weak3s7_Link_In_Th3_Ch@in}`.


## 10 - Bit 4 Bit - 100 Points
>We've found out that the malware is a ransomware. Find the attacker's bitcoin address.

Well, usally ransomware leave some file with instructions on Desktop

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 filescan | grep Desktop

0x000000007d660500      2      0 -W-r-- \Device\HarddiskVolume1\Users\Rick\Desktop\READ_IT.txt
0x000000007d74c2d0      2      1 R--rwd \Device\HarddiskVolume1\Users\Rick\Desktop
0x000000007d7f98c0      2      1 R--rwd \Device\HarddiskVolume1\Users\Rick\Desktop
0x000000007d864250     16      0 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop\desktop.ini
0x000000007d8a9070     16      0 R--rwd \Device\HarddiskVolume1\Users\Rick\Desktop\desktop.ini
0x000000007d8ac800      2      1 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop
0x000000007d8ac950      2      1 R--rwd \Device\HarddiskVolume1\Users\Public\Desktop
0x000000007e410890     16      0 R--r-- \Device\HarddiskVolume1\Users\Rick\Desktop\Flag.txt
0x000000007e5c52d0      3      0 R--rwd \Device\HarddiskVolume1\Users\Rick\AppData\Roaming\Microsoft\Windows\SendTo\Desktop.ini
0x000000007e77fb60      1      1 R--rw- \Device\HarddiskVolume1\Users\Rick\Desktop
```

There is something great, Flag.txt is for the challenge #13, let's see READ_IT.txt

```console
$ cat READ_IT.txt

Your files have been encrypted.
Read the Program for more information
read program for more information.
```

Ok, we have to dump the malware (be careful it's a real malware) 

```console
$ vol.py -f OtterCTF.vmem --profile=Win7SP1x64 procdump -D dump/ -p 3720
```

Open it using [ILSpy](https://github.com/icsharpcode/ILSpy) (a .NET disassembler), and in the Form3 (which is the one where the user is asked to pay to get his file back) there is something that look like a BTC address. 

![Bitcoin address](https://i.imgur.com/Iary8PU.png)
Here it is the flag `CTF{1MmpEmebJkqXG8nQv4cjJSmxZQFVmFo63M}`!


## 11 - Graphic's For The Weak - 150 Points
>There's something fishy in the malware's graphics.

Nothing strange in the form in decompiled code, so there must be some particoular image in the executable, .

```console
$ foremost executable.3720.exe -v

Num	 Name (bs=512)	       Size	 File Offset	 Comment 

0:	00000000.exe 	     414 KB 	          0 	 06/02/2017 15:44:57
1:	00000672.png 	      14 KB 	     344098 	  (800 x 600)
*|
```

00000672.png contains the flag `CTF{S0_Just_M0v3_Socy}`.


## 12 - Recovery - 300 Points
>Rick got to have his files recovered! What is the random password used to encrypt the files?


Using ILSpy, we found this particular function, which it has been modified to not send the password:

```
public void SendPassword(string password)
{
	string text = computerName + "-" + userName + " " + password;
}
```

So we search for `strings OtterCTF.vmem | grep WIN-LO6FAF3DTFE-Rick`... but nothing happened :-( .  
By default, .NET encodes string as UTF-16, hence we need to specify this behaviour to the strings command:

```console
$ strings -el OtterCTF.vmem | grep WIN-LO6FAF3DTFE-Rick

WIN-LO6FAF3DTFE-Rick aDOBofVYUNVnmp7
```

`CTF{aDOBofVYUNVnmp7}`


## 13 - Closure - 400 Points
>Now that you extracted the password from the memory, could you decrypt rick's files?

We have access to the cryptolocker source code and the password, so we can easily write a decoder.  
But, looking at the PDB path: 

```console
$ strings vmware-tray.exe | grep pdb

C:\Users\Tyler\Desktop\hidden-tear-master\hidden-tear\hidden-tear\obj\Debug\VapeHacksLoader.pdb
```

we notice `hidden-tear-master`, that's the name of an opensource cryptolocker on GitHub ([Link to repo](https://github.com/goliate/hidden-tear))  
So, downloading the decoder included in the repo, and spending 5 minutes adapting it to our case, we are able to dechiper the encrypted file and get the flag: `CTF{Im_Th@_B3S7_RicK_0f_Th3m_4ll}`
