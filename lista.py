from pathlib import Path
import hashlib
import mimetypes

BACKUP_DIR = Path(r"C:\HalloweenBackup")
OUTPUT_FILE = BACKUP_DIR / "LISTADO_COMPLETO.txt"

TEXT_EXTENSIONS = {
    ".html", ".htm", ".js", ".mjs", ".css", ".json", ".txt",
    ".xml", ".svg", ".webmanifest", ".map", ".glsl", ".frag", ".vert"
}

def sha256(path):
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "ERROR"

def inspect_text(path):
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
        lines = data.splitlines()

        urls = []
        keywords = []

        for line in lines:
            low = line.lower()

            if any(x in low for x in (
                "https://", "http://", "fetch(", "xhr", "xmlhttprequest",
                "websocket", ".json", ".js", ".css", ".png", ".jpg",
                ".jpeg", ".gif", ".webp", ".svg", ".mp3", ".wav",
                ".ogg", ".woff", ".woff2", ".wasm"
            )):
                urls.append(line.strip())

            if any(x in low for x in (
                "iframe", "canvas", "webgl", "serviceworker",
                "import(", "worker", "audio", "preload"
            )):
                keywords.append(line.strip())

        return len(lines), urls[:50], keywords[:50]

    except Exception:
        return 0, [], []

def main():
    if not BACKUP_DIR.exists():
        print(f"No existe: {BACKUP_DIR}")
        input("\nEnter para salir...")
        return

    files = [p for p in BACKUP_DIR.rglob("*") if p.is_file()]

    files.sort(key=lambda p: str(p).lower())

    total_size = sum(p.stat().st_size for p in files)

    with OUTPUT_FILE.open("w", encoding="utf-8") as out:

        out.write("=== BACKUP HALLOWEEN 2022 ===\n")
        out.write(f"Directorio: {BACKUP_DIR}\n")
        out.write(f"Archivos encontrados: {len(files)}\n")
        out.write(f"Tamaño total: {total_size / 1024 / 1024:.2f} MB\n\n")

        for i, path in enumerate(files, 1):

            rel = path.relative_to(BACKUP_DIR)
            size = path.stat().st_size
            ext = path.suffix.lower()
            mime = mimetypes.guess_type(path.name)[0] or "desconocido"

            out.write("\n" + "=" * 90 + "\n")
            out.write(f"[{i}/{len(files)}]\n")
            out.write(f"ARCHIVO : {rel}\n")
            out.write(f"TAMAÑO  : {size:,} bytes ({size / 1024:.2f} KB)\n")
            out.write(f"EXT     : {ext or '[sin extensión]'}\n")
            out.write(f"MIME    : {mime}\n")
            out.write(f"SHA256  : {sha256(path)}\n")

            if ext in TEXT_EXTENSIONS or size < 200_000:
                lines, urls, keywords = inspect_text(path)

                if lines:
                    out.write(f"LÍNEAS  : {lines}\n")

                if urls:
                    out.write("\n--- REFERENCIAS / LLAMADAS DETECTADAS ---\n")
                    for line in urls:
                        out.write(line + "\n")

                if keywords:
                    out.write("\n--- ESTRUCTURAS INTERESANTES ---\n")
                    for line in keywords:
                        out.write(line + "\n")

    print()
    print("LISTADO GENERADO")
    print(f"Archivos: {len(files)}")
    print(f"Tamaño : {total_size / 1024 / 1024:.2f} MB")
    print()
    print(f"Resultado:")
    print(OUTPUT_FILE)
    print()

    input("Enter para salir...")

if __name__ == "__main__":
    main()