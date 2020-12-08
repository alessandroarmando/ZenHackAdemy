---
ctf: Flare-On Challenge 7
challenge: 09 - crackinstaller
author: Firpo7
layout: writeup
categories: [rev]
tags: [ ctf, challenge, write-up, binary, reverse engineer, Malware Analysis]
---

>What kind of crackme doesn't even ask for the password? We need to work on our COMmunication skills.
>
>* Bug Notice: Avoid a possible blue-screen by debugging this on a single core VM


The challenge provides you with an executable `crackinstaller.exe`, it was a kind of crackme that doesn't ask you for input but you have to provide the "password" through registers. The goal was to find the right password so that it decrypts the flag.

The first thing done was to setup an environment to analyze the behavior of the program. Using Procmon it can be seen that it creates and interacts with the register:

`HKEY_CLASSES_ROOT\CLSID\{CEEACC6E-CCB2-4C4F-BCF6-D2176037A9A7}`

![COM register](/assets/writeups/FlareOn7/crackinstaller/com.png)

This register refers to a COM object which implementation could be found in the dll pointed by the key `InProcServer32\Default`.

Furthermore, there is also a `Config` key containing two subkeys _Flag_ and _Password_.

![Flag and Password keys](/assets/writeups/FlareOn7/crackinstaller/flag_pwd_reg.png)

The `credHelper.dll` exposes two interfaces, one it's the most generic one `IUnkown` while the other one is not provided. By looking at the objects in the executable containing the function pointers of the interfaces, can be inferred that there are other 2 functions.

Reverse engineering those functions it can be retrieved that the second interface is something like:

```cpp
[object, uuid(e27297b0-1e98-4033-b389-24eca246002a),
oleautomation, helpstring("CustomInterface")]
interface ICustomInterface : IUnknown
{
    HRESULT GetAndProcessPassword([in, out] byte* param);
    HRESULT ProcessAndSetFlag([in, out] byte* param);
};
```

Procmon also reveals that the program creates another file, `C:\Windows\System32\cfs.dll`. Looking at the interactions with this file suggests that it is a driver. IDA itself detected also it was a driver and the imports of the dll confirmed the assumption.

Debugging a driver needs to enter in kernel debugging by putting the VM in Test Mode and then attaching a remote WinDbg debugger to it. After that the following steps let me break to the first instruction of the driver:
* `sxe ld cfs.dll` : break the execution when cfs.dll will be loaded in memory
* `lm` : once stopped this command will show you the address where the driver is loaded
* `bp <base_driver_address> + <offset_to_the_entrypoint>` : this will put a breakpoint to the first instruction of the entrypoint
* `g` : continue the execution until it encounters the breakpoint set before

![WinDbg Driver Debugging](/assets/writeups/FlareOn7/crackinstaller/windbg.png)

Following the execution of the driver will jump back to `crackinstaller.exe` at offset 0x2a10. By debugging carefully this part of the execution the string `H@n $h0t FiRst!` show up in memory after some decryptions.

Trying to set the Password key in the COM register and write a COM client to interact with `credHelper.dll`, after doing a `GetAndProcessPassword` and passing the bytes obtained to the `ProcessAndSetFlag` in memory we can found the flag.

**`S0_m@ny_cl@sse$_in_th3_Reg1stry@flare-on.com`**
