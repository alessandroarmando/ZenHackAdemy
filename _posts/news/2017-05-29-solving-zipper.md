---
layout: post
author: AvalZ
title: Zipper
category: challenges
tags: [ misc, challenge ]
---

PlaidCTF 2017, [Zipper](/assets/news/zipper/zipper_50d3dc76dcdfa047178f5a1c19a52118.zip), 50 pts.

<!--more-->

# Intro

In questo esercizio utilizzeremo la "soluzione da segretaria", come riportato [sulle slide](https://drive.google.com/open?id=1Riqet3yeoKQBsBv54Jl4RhLhLRVLAh3TdpKd2hFKI1Y).

Dovete usare tutto quello che avete per trovare la flag, ma spesso i *tool automatici* non funzionano.
Controllate sempre le **Rules of Engagement**, potrebbe non essere permesso utilizzare *tool* automatici.

**CTFTime.org**: si registrano le persone e i team e potete trovare tutte le CTF.
Sul sito vengono anche pubblicate le classifiche (noi siamo al 133esimo posto).
Trovate anche i "task", ovvero le sfide presenti nella CTF, e i **write-up**, ovvero le soluzioni relative a ogni singolo task.

**PlaidCTF** è organizzata da PPP, un team americano vincitore di DEF CON, primi in classifica globale.

CTFTime reindirizza al sito della singola CTF, dove occorre registrarsi come singolo e inseguito entrare in un Team.
Il sito è normalmente diviso in due: una pagina che contiene la lista dei *task* e poi una o più pagine

I *task* sono divisi per punteggio (più alto il punteggio, più difficile la sfida) e poi per categoria, che può essere per esempio:
* Web
* Crypto
* Pwnable
* Misc
* ...

Per ogni *task* è normalmente presente una descrizione che spiega come risolvere lo stesso e contiene degli indizi, ma può essere molto fuorviante.

Oltre a questi, di solito troviamo un *sanity check* da 1 punto, un task dove viene fornita la flag in chiaro per verificare la
disponibilità del sistema.

Sulla pagina della lista dei task è normalmente presente un form per contattare gli organizzatori e un form dove è possibile sottomettere le flag trovate;
se corretta, il sistema di *scoring* assegna il punteggio al partecipante (e al suo team).

La CTF normalmente dura 48 ore, ma un team non riesce spesso a partecipare negli stessi orari, quindi è necessario utilizzare strumenti
di condivisione e documentazione del lavoro per potersi sincronizzare.

A fine CTF bisogna produrre un **write-up** da sottomettere agli organizzatori per validare la classifica (in modo da dimostrare che le flag sono
effettivamente state trovate dal team e non "rubate" da altri).

# Approccio

[Write-up](https://github.com/ResultsMayVary/ctf/blob/master/PlaidCTF-2017/misc50_zipper/zipper_50d3dc76dcdfa047178f5a1c19a52118.zip)

La sfida **Zipper** fornisce un file zip impossibile da aprire.
Il suggerimento fa capire che è necessario aprire lo ZIP per trovare la flag.

Facendolo partire, il messaggio di errore su Windows è "La cartella compressa [...] non è valida".

Su Linux, da linea di comando, dà errore su `Extra field length`. ATTENZIONE: l'errore in realtà è sul campo prima: `File name len`

## Formato ZIP

Il file ZIP è molto particolare: mette in testa i dati sui file, poi i dati sui file e in fondo mette come è organizzato l'archivio.

I file ZIP però sono sempre in Little Endian, indipendentemente dall'architettura, in quanto viene definito nel protocollo.

![Zip Format](/assets/news/zipper/zip_format.png)

## Soluzione

Partiamo da **Local File Header**: trovo la lunghezza del file su 0x001A-0x001B come `2923`, ma essendo in Little Endian va fatto `2329`.
Va modificato in base alla lunghezza del nome del file, che troviamo 2 byte dopo.
Quanto è lungo il nome del file? Va ricostruito.

Partiamo dagli **Extra Field**: sappiamo che esiste perchè la lunghezza (trovata su 0x001C-0x001D) è di 001C (sempre in Little Endian),
ma sappiamo anche che gli Extra Field iniziano con l'header `5455`, quindi possiamo vedere dove termina il nome del file.

Con alcuni semplici tentativi notiamo che lo spazio dedicato al nome del file è quello tra 0x001E e 0x0025, quindi la dimensione va
modificata in 8 byte, cioè in `0800`, mentre il nome del file può essere qualunque stringa di 8 caratteri.

La stessa cosa va fatta su 0x00A4-0x00A5, dove `2923` diventa `0800`, mentre in 0x00B6-0x00BD, alla stringa di `00` va sostituita nuovamente
con una stringa casuale.

A questo punto si può aprire il file ZIP per ottenere

```
Huzzah, you have captured the flag:
PCTF{f0rens1cs_yay}
```

Qui potete trovare il file di [Zipper fixed](/assets/news/zipper/zipper_fixed.zip).
