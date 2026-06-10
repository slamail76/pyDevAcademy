#!/usr/bin/env python3
"""
scarica_musica.py
Scarica musica da YouTube con selezione interattiva del formato.
Cartella di destinazione fissa: D:/download/musica
"""

import os
from yt_dlp import YoutubeDL

CARTELLA = "D:/download/musica"

PRESET = [
    {
        "etichetta": "MP3  320 kbps  (migliore qualita', file piu' grande)",
        "opts": {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"}],
        },
    },
    {
        "etichetta": "MP3  192 kbps  (buona qualita', bilanciato)",
        "opts": {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        },
    },
    {
        "etichetta": "MP3  128 kbps  (qualita' standard, file piccolo)",
        "opts": {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "128"}],
        },
    },
    {
        "etichetta": "M4A / AAC  (formato nativo YouTube, nessuna ricodifica - non richiede FFmpeg)",
        "opts": {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
        },
    },
    {
        "etichetta": "OPUS  (alta qualita', file piccolo)",
        "opts": {
            "format": "bestaudio[ext=webm]/bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "opus"}],
        },
    },
    {
        "etichetta": "FLAC  (lossless, massima fedelta', file grande)",
        "opts": {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "flac"}],
        },
    },
]


def mostra_formati(info: dict):
    """Stampa i formati audio disponibili sul server."""
    audio = [
        f for f in info.get("formats", [])
        if f.get("acodec") not in (None, "none")
        and f.get("vcodec") in (None, "none", "")
    ]
    print("\n" + "=" * 65)
    print("  FORMATI AUDIO DISPONIBILI SUL SERVER")
    print("=" * 65)
    if audio:
        print(f"  {'ID':<12} {'EXT':<8} {'CODEC':<14} {'BITRATE':>10}  {'PROTO'}")
        print("  " + "-" * 55)
        for f in sorted(audio, key=lambda x: x.get("abr") or 0, reverse=True):
            abr   = f.get("abr")
            bitrate = f"{int(abr)} kbps" if abr else "?"
            print(f"  {f.get('format_id','?'):<12} {f.get('ext','?'):<8} "
                  f"{f.get('acodec','?'):<14} {bitrate:>10}  {f.get('protocol','?')}")
    else:
        print("  (nessun formato solo-audio trovato)")
    print("=" * 65)


def scegli_preset() -> dict:
    print("\n" + "=" * 65)
    print("  OPZIONI DI DOWNLOAD")
    print("=" * 65)
    for i, p in enumerate(PRESET, 1):
        print(f"  [{i}]  {p['etichetta']}")
    print("  [0]  Formato manuale (inserisci ID dalla lista sopra)")
    print("=" * 65)

    while True:
        scelta = input("\n  Scegli un'opzione: ").strip()
        if scelta == "0":
            fmt_id = input("  Inserisci ID formato (es. 251): ").strip()
            return {"etichetta": f"Formato manuale: {fmt_id}", "opts": {"format": fmt_id}}
        if scelta.isdigit() and 1 <= int(scelta) <= len(PRESET):
            return PRESET[int(scelta) - 1]
        print("  Scelta non valida, riprova.")


def main():
    print("\n" + "=" * 65)
    print("       SCARICA MUSICA DA YOUTUBE")
    print(f"       Cartella: {CARTELLA}")
    print("=" * 65)

    url = input("\n  Incolla l'URL di YouTube: ").strip()
    if not url:
        print("  URL non fornito. Uscita.")
        return

    # — Recupera info (stesso approccio base che funziona) —
    print("\n  Recupero informazioni sul video...")
    base = {"format": "bestaudio/best", "noplaylist": True, "quiet": True}
    with YoutubeDL(base) as ydl:
        info = ydl.extract_info(url, download=False)

    print(f"\n  Titolo  : {info.get('title', '?')}")
    print(f"  Canale  : {info.get('uploader', '?')}")
    print(f"  Durata  : {info.get('duration_string', '?')}")

    mostra_formati(info)
    preset = scegli_preset()
    print(f"\n  Selezionato: {preset['etichetta']}")

    if input("\n  Avviare il download? [S/n]: ").strip().lower() in ("n", "no"):
        print("  Annullato.")
        return

    # — Download: stesse opzioni base che funzionano + preset scelto —
    os.makedirs(CARTELLA, exist_ok=True)
    ydl_opts = {
        "noplaylist": True,
        "outtmpl": os.path.join(CARTELLA, "%(title)s.%(ext)s"),
    }
    ydl_opts.update(preset["opts"])

    print()
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"\n  File salvato in: {CARTELLA}")
    print("  Fatto!\n")


if __name__ == "__main__":
    main()
