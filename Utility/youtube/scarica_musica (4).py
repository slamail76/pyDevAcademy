#!/usr/bin/env python3
"""
scarica_musica.py
Scarica musica da YouTube con selezione interattiva del formato.
Cartella di destinazione fissa: D:/download/musica

PRIMA DI USARE – esporta i cookie da Edge:
  1. Installa l'estensione "Get cookies.txt LOCALLY" su Edge
     https://microsoftedge.microsoft.com/addons/detail/get-cookiestxt-locally/hellfpgpfknfdgcaladpnijhbpedlajn
  2. Vai su youtube.com con Edge (loggato)
  3. Clicca l'icona dell'estensione → Export
  4. Salva il file come:  D:/download/musica/cookies.txt
"""

import sys
import os

try:
    import yt_dlp
except ImportError:
    print("❌  yt-dlp non è installato.")
    print("    Installalo con:  pip install yt-dlp")
    sys.exit(1)

CARTELLA_DOWNLOAD = "D:/download/musica"
COOKIE_FILE       = "D:/Download/musica/cookies.txt"

# ─────────────────────────────────────────────
# Utilità
# ─────────────────────────────────────────────

def formatta_dimensione(bytes_val):
    if bytes_val is None:
        return "sconosciuta"
    if bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.0f} KB"
    return f"{bytes_val / (1024 * 1024):.1f} MB"


def formatta_bitrate(abr):
    if abr is None:
        return "?"
    return f"{int(abr)} kbps"


# ─────────────────────────────────────────────
# Opzioni base yt-dlp
# ─────────────────────────────────────────────

def base_opts() -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
        },
        "retries": 5,
        "fragment_retries": 5,
        # Bypassa errori SSL da proxy/antivirus (es. Kaspersky, Zscaler)
        "nocheckcertificate": True,
    }
    # Usa il file cookie se presente
    if os.path.exists(COOKIE_FILE):
        opts["cookiefile"] = COOKIE_FILE
    return opts


# ─────────────────────────────────────────────
# Step 1 – Recupero informazioni sul video
# ─────────────────────────────────────────────

def recupera_info(url: str) -> dict:
    opts = base_opts()
    opts["skip_download"] = True
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        msg = str(e)
        if "403" in msg or "Forbidden" in msg:
            print("\n  ❌  YouTube ha bloccato la richiesta (HTTP 403).")
            _stampa_guida_cookie()
        raise


def _stampa_guida_cookie():
    print("  ─────────────────────────────────────────────────────────")
    print("  Il file cookie NON è stato trovato oppure non è valido.")
    print()
    print("  Come risolvere:")
    print("  1. Apri Edge e installa l'estensione:")
    print('     "Get cookies.txt LOCALLY"')
    print("     https://microsoftedge.microsoft.com/addons/detail/")
    print("     get-cookiestxt-locally/hellfpgpfknfdgcaladpnijhbpedlajn")
    print()
    print("  2. Vai su  youtube.com  con Edge (assicurati di essere loggato)")
    print("  3. Clicca l'icona dell'estensione → Export")
    print(f"  4. Salva il file come:  {COOKIE_FILE}")
    print("  5. Riavvia il programma")
    print("  ─────────────────────────────────────────────────────────\n")


# ─────────────────────────────────────────────
# Step 2 – Presentazione e scelta del formato
# ─────────────────────────────────────────────

PRESET_AUDIO = [
    {
        "id": "best_mp3_320",
        "etichetta": "🎵  MP3  320 kbps  (migliore qualità, file più grande)",
        "formato": "bestaudio/best",
        "post": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"}],
    },
    {
        "id": "best_mp3_192",
        "etichetta": "🎵  MP3  192 kbps  (buona qualità, bilanciato)",
        "formato": "bestaudio/best",
        "post": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
    },
    {
        "id": "best_mp3_128",
        "etichetta": "🎵  MP3  128 kbps  (qualità standard, file piccolo)",
        "formato": "bestaudio/best",
        "post": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "128"}],
    },
    {
        "id": "best_m4a",
        "etichetta": "🎼  M4A / AAC  (formato nativo YouTube, nessuna ricodifica)",
        "formato": "bestaudio[ext=m4a]/bestaudio/best",
        "post": [],
    },
    {
        "id": "best_opus",
        "etichetta": "🔊  OPUS  (alta qualità, file piccolo, ideale per streaming)",
        "formato": "bestaudio[ext=webm]/bestaudio/best",
        "post": [{"key": "FFmpegExtractAudio", "preferredcodec": "opus"}],
    },
    {
        "id": "best_flac",
        "etichetta": "💿  FLAC  (lossless, massima fedeltà, file grande)",
        "formato": "bestaudio/best",
        "post": [{"key": "FFmpegExtractAudio", "preferredcodec": "flac"}],
    },
]


def mostra_formati_disponibili(info: dict):
    formati = info.get("formats", [])
    audio_fmt = [
        f for f in formati
        if f.get("acodec") not in (None, "none")
        and f.get("vcodec") in (None, "none", "")
    ]

    print("\n" + "═" * 60)
    print("  FORMATI AUDIO ORIGINALI DISPONIBILI SUL SERVER")
    print("═" * 60)

    if not audio_fmt:
        print("  (Nessun formato solo-audio trovato)")
    else:
        print(f"  {'ID':<12} {'EXT':<8} {'CODEC':<12} {'BITRATE':>10}  {'DIMENSIONE':>12}")
        print("  " + "─" * 56)
        for f in sorted(audio_fmt, key=lambda x: x.get("abr") or 0, reverse=True):
            fmt_id  = f.get("format_id", "?")
            ext     = f.get("ext", "?")
            codec   = f.get("acodec", "?")
            bitrate = formatta_bitrate(f.get("abr"))
            dim     = formatta_dimensione(f.get("filesize") or f.get("filesize_approx"))
            print(f"  {fmt_id:<12} {ext:<8} {codec:<12} {bitrate:>10}  {dim:>12}")

    print("═" * 60)


def scegli_preset() -> dict:
    print("\n" + "═" * 60)
    print("  OPZIONI DI DOWNLOAD")
    print("═" * 60)
    for i, p in enumerate(PRESET_AUDIO, 1):
        print(f"  [{i}]  {p['etichetta']}")
    print("  [0]  Formato personalizzato (inserisci ID formato manualmente)")
    print("═" * 60)

    while True:
        scelta = input("\n  ▶  Scegli un'opzione: ").strip()
        if scelta == "0":
            fmt_id = input("  Inserisci l'ID formato (es. 251): ").strip()
            return {
                "id": "custom",
                "etichetta": f"Formato personalizzato: {fmt_id}",
                "formato": fmt_id,
                "post": [],
            }
        if scelta.isdigit() and 1 <= int(scelta) <= len(PRESET_AUDIO):
            return PRESET_AUDIO[int(scelta) - 1]
        print("  ⚠  Scelta non valida, riprova.")


# ─────────────────────────────────────────────
# Step 3 – Download effettivo
# ─────────────────────────────────────────────

def scarica(url: str, preset: dict, cartella: str):
    os.makedirs(cartella, exist_ok=True)

    def hook(d):
        if d["status"] == "downloading":
            perc  = d.get("_percent_str", "  ?%").strip()
            speed = d.get("_speed_str", "?/s").strip()
            eta   = d.get("_eta_str", "?").strip()
            print(f"\r  ⬇  {perc}  velocità: {speed}  eta: {eta}   ", end="", flush=True)
        elif d["status"] == "finished":
            print(f"\r  ✅  Download completato: {os.path.basename(d['filename'])}" + " " * 20)

    ydl_opts = base_opts()
    ydl_opts.update({
        "format": preset["formato"],
        "outtmpl": os.path.join(cartella, "%(title)s.%(ext)s"),
        "postprocessors": preset["post"],
        "progress_hooks": [hook],
        "quiet": False,
    })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        if "403" in str(e) or "Forbidden" in str(e):
            print("\n  ❌  YouTube ha bloccato il download (HTTP 403).")
            _stampa_guida_cookie()
        raise


# ─────────────────────────────────────────────
# Flusso principale
# ─────────────────────────────────────────────

def main():
    print("\n" + "═" * 60)
    print("       🎶  SCARICA MUSICA DA YOUTUBE  🎶")
    print(f"       Cartella: {CARTELLA_DOWNLOAD}")
    if os.path.exists(COOKIE_FILE):
        print(f"       Cookie:   {COOKIE_FILE}  ✔  (file trovato, verrà usato)")
    else:
        print(f"       Cookie:   ⚠  FILE NON TROVATO in: {COOKIE_FILE}")
        print(f"       Cookie:   Esporta cookies.txt da Chrome/Edge e salvalo lì!")
    print("═" * 60)

    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
        print(f"\n  URL ricevuto come argomento: {url}")
    else:
        url = input("\n  Incolla l'URL di YouTube: ").strip()

    if not url:
        print("  ❌  URL non fornito. Uscita.")
        sys.exit(1)

    print("\n  🔍  Recupero informazioni sul video…")
    try:
        info = recupera_info(url)
    except Exception as e:
        print(f"\n  ❌  Impossibile recuperare il video:\n     {e}")
        sys.exit(1)

    titolo = info.get("title", "Titolo sconosciuto")
    canale = info.get("uploader", "?")
    durata = info.get("duration_string") or f"{info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}"

    print(f"\n  📀  Titolo  : {titolo}")
    print(f"      Canale  : {canale}")
    print(f"      Durata  : {durata}")

    mostra_formati_disponibili(info)

    preset = scegli_preset()
    print(f"\n  ✔  Selezionato: {preset['etichetta']}")

    if preset["post"]:
        print("  ℹ️   Questo formato richiede FFmpeg per la conversione.")
        print("      Se non è installato: https://ffmpeg.org/download.html")

    conferma = input("\n  Avviare il download? [S/n]: ").strip().lower()
    if conferma in ("n", "no"):
        print("  ↩  Download annullato.")
        sys.exit(0)

    print()
    try:
        scarica(url, preset, CARTELLA_DOWNLOAD)
    except Exception as e:
        print(f"\n  ❌  Errore durante il download:\n     {e}")
        sys.exit(1)

    print(f"\n  📁  File salvato in: {CARTELLA_DOWNLOAD}")
    print("  🎉  Fatto!\n")


if __name__ == "__main__":
    main()
