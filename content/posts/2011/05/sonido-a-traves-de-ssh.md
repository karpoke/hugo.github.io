---
title: "Sonido a través de SSH"
date: 2011-05-05T22:23:00+01:00
categories: ["admin"]
tags: ["alsa", "alsamixer", "altavoz", "aplay", "arecord", "dd", "esd", "esddsp", "espeak", "festival", "micrófono", "mp3", "mplayer", "ogg", "ogv", "oss", "padsp", "pulseaudio", "sonido", "ssh", "text-to-speech", "tts"]
slug: "sonido-a-traves-de-ssh"
---
Si tenemos [acceso por `ssh`][acceso por ssh] a otro ordenador, ambos con micrófono y
altavoces, podemos redirigir el sonido en ambos sentidos, es decir,
podemos conseguir cosas como:

-   que lo que capta nuestro [micrófono][] se escuche en los altavoces
```
del otro ordenador y [viceversa][]
```
-   que lo que se [escribe][] en un ordenador se escuche en el otro y
```
[viceversa][1]
```
-   que el contenido de un [fichero de texto][escribe] se oiga en los
```
altavoces remotos y [viceversa][1]
```
-   que un archivo de [audio][] se escuche en los altavoces remotos y
```
[viceversa][2]
```
-   que el audio de un archivo de [vídeo][] se escuche en los altavoces
```
remotos y [viceversa][3]
```


Dispositivos de sonido en Ubuntu Maverick Meerkat
-------------------------------------------------

Uno de los cambios de Ubuntu Maverick Meerkat (10.10) fue la
desaparición del dispositivo `/dev/dsp` y otros, como `/dev/mixer`,
`/dev/sndstat` y `/dev/audio`, al utilizar la [interfaz ALSA en
detrimento de la OSS API][].

Para los programas que tengan problemas para utilizar la API ALSA,
existen los comandos `esddsp`, que permite redirigir datos de audio
no-esd a través de [esd][] y `padsp`, que permite lo mismo pero mediante
PulseAudio.

![Pulseaudio diagram]({static}/images/Pulseaudio-diagram-246x300.png)

_Fuente: [es.wikipedia.org][]_


Redirigir el micrófono local a los altavoces remotos
----------------------------------------------------

Si disponemos de `/dev/dsp` en ambas máquinas podemos utilizar `dd`:

```
$ dd if=/dev/dsp | ssh -c arcfour -C user@host dd of=/dev/dsp
```

La opción `-c` permite especificar el tipo de cifrado, y la opción `-C`
que se utilice compresión de datos, utilizando el mismo algoritmo
empleado por `gzip`.

También podemos utilizar `aplay`:

```
$ arecord -f dat | ssh -C user@host aplay -f dat
```

La opción `-f` permite especificar el formato:

-   `-f cd` (16 bit little endian, 44100, stereo) [-f S16_LE -c2
```
-r44100]
```
-   `-f cdr` (16 bit big endian, 44100, stereo) [-f S16_BE -c2 -f44100]
-   `-f dat` (16 bit little endian, 48000, stereo) [-f S16_LE -c2
```
-r48000]
```
-   Por defecto, se utiliza (8 bit little endian, 8000, mono) [-f U8 -c1
```
-r8000]
```


Redirigir el micrófono remoto a los altavoces locales
-----------------------------------------------------

Como en el caso anterior, pero a la inversa:

```
$ ssh -C user@host arecord -f dat | aplay -f dat
```

Si queremos guardar el audio que recibimos mientras lo escuchamos:

```
$ ssh -C user@host arecord -f dat | tee audio.wav | aplay -f dat
```

Supongo que también se debe poder utilizar `dd` para traer el sonido
captado por un micrófono remoto, pero no lo he podido probar.


Enviar texto y que se oiga por los altavoces remotos
----------------------------------------------------

El texto puede ser algo que acabemos de escribir, el contenido de un
fichero o la salida por `stdout` de un _script_.

Para esto, podemos utilizar cualquier sintentizador de voz, por ejemplo,
`espeak` o `festival`.

```
$ echo "Hola, mundo" | ssh user@host espeak -ves
$ echo "Hello, world" | ssh user@host espeak
$ echo "I am an alien" | ssh user@host festival --tts
$ echo "Una ranita iba caminando" | ssh user@host festival --tts --language spanish
$ cat textos.txt | ssh user@host espeak -ves
$ w3m -dump http://www.gnu.org/licenses/gpl-2.0.txt | ssh user@host espeak
```

Si queremos parar la locución, deberemos iniciar sesión en la máquina
remota y matar el proceso `espeak` o `festival`. Dicho sea de paso, para
escuchar la voz en castellano usando el `festival` hay que instalar el
paquete `festvox-ellpc11k`.


Recibir texto y que se oiga por nuestros altavoces
--------------------------------------------------

El caso inverso al anterior:

```
$ ssh user@host cat textos.txt | espeak -ves
$ ssh user@host w3m -dump http://www.gnu.org/licenses/gpl-2.0.txt | espeak
```


Reproducir un archivo de audio en los altavoces remotos
-------------------------------------------------------

Para escuchar un archivo de audio remoto utilizaremos `mplayer`:

```
$ cat podcast.ogg | ssh -C user@host mplayer -
```


Reproducir un archivo de audio de la máquina remota en local
------------------------------------------------------------

Al revés del caso anterior.

```
$ ssh -C user@host cat podcast.ogg | mplayer -
```


Reproducir el sonido de un video en los altavoces remotos
---------------------------------------------------------

Es idéntico al caso de un archivo de audio, pero le pasamos a `mplayer`
el argumento `-vc null` para que no decodifique el vídeo.

```
$ ssh -C user@host cat podcast.ogg | mplayer -vc null -
```


Reproducir el sonido de un vídeo remoto en nuestra máquina
----------------------------------------------------------

Podemos conseguir que se vea y escuche el vídeo:

```
$ ssh -C user@host cat movie.ogv | mplayer -
```

O que sólo se escuche el audio:

```
$ ssh -C user@host cat movie.ogv | mplayer -vc null -
```

  [acceso por ssh]: {{< relref "/posts/admin/conectarse-por-ssh-solo-usando-la-clave.md" >}}
  [micrófono]: #microfono-local-altavoces-remotos
  [viceversa]: #microfono-remoto-altavoces-locales
  [escribe]: #texto-local-altavoces-remotos
  [1]: #texto-remoto-altavoces-locales
  [audio]: #fichero-audio-local-altavoces-remotos
  [2]: #fichero-audio-remoto-altavoces-locales
  [vídeo]: #fichero-video-local-altavoces-remotos
  [3]: #fichero-video-remoto-altavoces-locales
  [interfaz ALSA en detrimento de la OSS API]: http://bugs.launchpad.net/ubuntu/+source/linux/+bug/634211
  [esd]: http://en.wikipedia.org/wiki/Enlightened_Sound_Daemon
  [es.wikipedia.org]: http://es.wikipedia.org/wiki/Archivo:Pulseaudio-diagram.svg
