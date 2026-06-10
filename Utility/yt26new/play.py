#!/usr/bin/env python3
"""
scarica_musica.py
Scarica musica da YouTube - singolo video o playlist intera.
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
    """Raccoglie i formati audio unici da tutti i video e li stampa."""
    # info puo' essere un singolo video o una playlist (entries)
    entries = info.get("entries") or [info]

    # Campiona fino a 3 video per trovare i formati comuni
    campione = [e for e in entries if e is not None][:3]

    formati_visti = {}  # ext+codec -> esempio
    for entry in campione:
        # Se le entries sono stub (solo id/title), recupera i dettagli completi
        if not entry.get("formats"):
            try:
                with YoutubeDL({"quiet": True, "noplaylist": True}) as ydl:
                    entry = ydl.extract_info(
                        f"https://www.youtube.com/watch?v={entry['id']}",
                        download=False
                    )
            except Exception:
                continue
        for f in entry.get("formats", []):
            if f.get("acodec") not in (None, "none") and f.get("vcodec") in (None, "none", ""):
                key = f"{f.get('ext','?')}_{f.get('acodec','?')}"
                if key not in formati_visti:
                    formati_visti[key] = f

    print("\n" + "=" * 65)
    print("  FORMATI AUDIO DISPONIBILI (campione dalla playlist)")
    print("=" * 65)
    if formati_visti:
        print(f"  {'ID':<12} {'EXT':<8} {'CODEC':<14} {'BITRATE':>10}  {'PROTO'}")
        print("  " + "-" * 55)
        for f in sorted(formati_visti.values(), key=lambda x: x.get("abr") or 0, reverse=True):
            abr     = f.get("abr")
            bitrate = f"{int(abr)} kbps" if abr else "?"
            print(f"  {f.get('format_id','?'):<12} {f.get('ext','?'):<8} "
                  f"{f.get('acodec','?'):<14} {bitrate:>10}  {f.get('protocol','?')}")
    else:
        print("  (nessun formato solo-audio trovato nel campione)")
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

    url = input("\n  Incolla l'URL di YouTube (video o playlist): ").strip()
    if not url:
        print("  URL non fornito. Uscita.")
        return

    # — Recupera info (senza scaricare) —
    print("\n  Recupero informazioni...")
    with YoutubeDL({"quiet": True, "extract_flat": "in_playlist"}) as ydl:
        info = ydl.extract_info(url, download=False)

    # — Capisce se e' una playlist o un singolo video —
    is_playlist = info.get("_type") == "playlist" or bool(info.get("entries"))

    if is_playlist:
        entries = [e for e in info.get("entries", []) if e is not None]
        n = len(entries)
        nome_playlist = info.get("title", "Playlist senza titolo")
        print(f"\n  Playlist : {nome_playlist}")
        print(f"  Brani    : {n} video trovati")

        # Sottocartella con il nome della playlist
        cartella_dest = os.path.join(CARTELLA, _nome_sicuro(nome_playlist))
    else:
        entries = [info]
        print(f"\n  Titolo   : {info.get('title', '?')}")
        print(f"  Canale   : {info.get('uploader', '?')}")
        print(f"  Durata   : {info.get('duration_string', '?')}")
        cartella_dest = CARTELLA

    # — Mostra formati e fa scegliere UNA volta —
    mostra_formati(info)
    preset = scegli_preset()
    print(f"\n  Selezionato: {preset['etichetta']}")
    if is_playlist:
        print(f"  Destinazione: {cartella_dest}")

    if input("\n  Avviare il download? [S/n]: ").strip().lower() in ("n", "no"):
        print("  Annullato.")
        return

    os.makedirs(cartella_dest, exist_ok=True)

    # — Download —
    if is_playlist:
        _scarica_playlist(entries, preset, cartella_dest)
    else:
        _scarica_uno(url, preset, cartella_dest)

    print(f"\n  Tutti i file sono stati salvati in: {cartella_dest}")
    print("  Fatto!\n")


def _scarica_uno(url: str, preset: dict, cartella: str):
    ydl_opts = {
        "noplaylist": True,
        "outtmpl": os.path.join(cartella, "%(title)s.%(ext)s"),
    }
    ydl_opts.update(preset["opts"])
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def _scarica_playlist(entries: list, preset: dict, cartella: str):
    totale  = len(entries)
    ok      = 0
    errori  = []

    ydl_opts = {
        "noplaylist": True,
        # Numerazione automatica nella playlist: 01 - Titolo, 02 - Titolo ...
        "outtmpl": os.path.join(cartella, "%(playlist_index)02d - %(title)s.%(ext)s"),
    }
    ydl_opts.update(preset["opts"])

    print()
    with YoutubeDL(ydl_opts) as ydl:
        for i, entry in enumerate(entries, 1):
            titolo = entry.get("title") or entry.get("id") or f"Brano {i}"
            print(f"  [{i}/{totale}]  {titolo}")
            video_url = (
                entry.get("url")
                or entry.get("webpage_url")
                or f"https://www.youtube.com/watch?v={entry['id']}"
            )
            try:
                ydl.download([video_url])
                ok += 1
            except Exception as e:
                print(f"         ERRORE: {e}")
                errori.append((titolo, str(e)))

    # — Riepilogo finale —
    print("\n" + "=" * 65)
    print(f"  RIEPILOGO: {ok}/{totale} brani scaricati correttamente")
    if errori:
        print(f"  Errori ({len(errori)}):")
        for titolo, msg in errori:
            print(f"    - {titolo}: {msg}")
    print("=" * 65)


def _nome_sicuro(nome: str) -> str:
    """Rimuove caratteri non validi per nomi di cartella Windows."""
    for c in r'\/:*?"<>|':
        nome = nome.replace(c, "_")
    return nome.strip()


if __name__ == "__main__":
    main()
