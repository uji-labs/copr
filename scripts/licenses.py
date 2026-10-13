"""Collect dependency notices for the binary package."""

import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import tomllib

source = Path(sys.argv[1])
notices = source / "bundled-licenses"
copies = {}

for crate in sorted((source / "vendor").iterdir()):
    with (crate / "Cargo.toml").open("rb") as file:
        package = tomllib.load(file)["package"]

    for file in sorted(crate.rglob("*")):
        if not file.is_file():
            continue
        relative = file.relative_to(crate)
        is_notice = file.name.lower().startswith(
            ("license", "licence", "copying", "notice", "copyright")
        )
        if not is_notice and relative.as_posix() != package.get("license-file"):
            continue

        destination = notices / crate.name / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        digest = hashlib.sha256(file.read_bytes()).digest()
        if digest in copies:
            destination.symlink_to(os.path.relpath(copies[digest], destination.parent))
        else:
            shutil.copyfile(file, destination)
            copies[digest] = destination

    if package["name"] == "two-face":
        # Syntax definitions have notices separate from the crate license.
        version = quote(package["version"], safe="")
        url = f"https://codeberg.org/CosmicHarper/two-face/raw/tag/v{version}/generated/acknowledgements_full.md"
        destination = notices / "LicenseRef-Two-Face-assets.txt"
        subprocess.run(
            [
                "curl",
                "--fail",
                "--silent",
                "--show-error",
                "--location",
                "--retry",
                "3",
                "--retry-all-errors",
                "--connect-timeout",
                "15",
                "--max-time",
                "60",
                "--retry-max-time",
                "180",
                "--user-agent",
                "OpenAI File Downloader, XaiImageApiFetch/1.0",
                "--output",
                str(destination),
                url,
            ],
            check=True,
        )
        if "# Syntaxes" not in destination.read_text():
            sys.exit("The Two-Face license document is invalid.")
