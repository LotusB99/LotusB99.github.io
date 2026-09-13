from pathlib import Path
import shutil

SOURCE = Path(r"C:\HalloweenBackup")
DEST = Path(r"C:\HalloweenGitHub")

HOST_MAPPINGS = {
    "www.google.com": "",
    "www.gstatic.com": "",
    "fonts.gstatic.com": "",
}

EXCLUDE_NAMES = {
    "manifest.json",
    "LISTADO_COMPLETO.txt",
    "lista.py",
}

EXCLUDE_PATH_PARTS = (
    "\\async\\",
    "\\gen_204",
)

def should_skip(rel):
    s = "\\" + str(rel).replace("/", "\\").lower()
    name = Path(rel).name.lower()

    if name in {x.lower() for x in EXCLUDE_NAMES}:
        return True

    return any(x.lower() in s for x in EXCLUDE_PATH_PARTS)

def main():
    if not SOURCE.exists():
        print(f"No existe el backup: {SOURCE}")
        input("Enter para salir...")
        return

    if DEST.exists():
        print(f"El destino ya existe: {DEST}")
        print("Borrándolo para generar una copia limpia...")
        shutil.rmtree(DEST)

    DEST.mkdir(parents=True)

    copied = 0
    skipped = 0

    for src in SOURCE.rglob("*"):
        if not src.is_file():
            continue

        rel = src.relative_to(SOURCE)

        if should_skip(rel):
            skipped += 1
            continue

        parts = rel.parts

        if parts[0] in HOST_MAPPINGS:
            new_parts = parts[1:]
        else:
            new_parts = parts

        if not new_parts:
            continue

        dst = DEST.joinpath(*new_parts)
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(src, dst)
        copied += 1

    index = DEST / "index.html"

    index.write_text(
        """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Halloween 2022 Google Doodle</title>
</head>
<body style="margin:0;background:#000">
<script>
location.href="./logos/2021/halloween21/v81123/halloween21.html";
</script>
</body>
</html>
""",
        encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("COPIA PREPARADA PARA GITHUB PAGES")
    print("=" * 60)
    print(f"Origen : {SOURCE}")
    print(f"Destino: {DEST}")
    print(f"Copiados : {copied}")
    print(f"Omitidos : {skipped}")
    print()
    print("Juego:")
    print(
        "logos\\2021\\halloween21\\v81123\\halloween21.html"
    )
    print()
    print("Subí TODO el contenido de:")
    print(DEST)
    print()
    input("Enter para salir...")

if __name__ == "__main__":
    main()