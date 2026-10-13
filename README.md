# Uji COPR

Fedora packages for [uji](https://github.com/uji-labs/uji).

## Installation

```sh
sudo dnf copr enable @uji-labs/Uji
sudo dnf install uji
```

## Usage

```sh
uji
uji --help
```

See the [uji documentation](https://docs.uji.sh) for configuration.

## Uninstallation

```sh
sudo dnf remove uji
sudo dnf copr disable @uji-labs/Uji
```

## Building / contributing

Use Docker to build the source package:

```sh
docker build -t uji-copr-build .
docker run --rm -v "$PWD:/packaging" uji-copr-build bash scripts/build-srpm.sh
```

The source package goes into `dist/`.
Remove `dist/` before another build.
Update the version, commit, and changelog in `uji.spec` for each release.
GitHub Actions checks Fedora 43, 44, 45, and Rawhide builds on `x86_64` without network access.
Use `--build-arg FEDORA=43`, `45`, or `rawhide` to select another Docker image.
Submit packaging changes through a pull request.

See [Publishing](docs/publishing.md) for release instructions and API token replacement.

## License

uji uses [GPL-3.0-or-later](https://github.com/uji-labs/uji/blob/main/LICENSE).
Bundled dependencies retain their own licenses.
