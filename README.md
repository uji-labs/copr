# uji COPR

Fedora packages for [uji](https://github.com/uji-labs/uji).

## Installation

Run these commands after the COPR project is available:

```sh
sudo dnf copr enable @uji-labs/uji
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
sudo dnf copr disable @uji-labs/uji
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

To publish, create a GitHub environment named `copr` and restrict it to `master`.
Set `COPR_TARGET` to `@uji-labs/uji` and add your [COPR API configuration](https://copr.fedorainfracloud.org/api/) as the secret `COPR_CONFIG`.
Enable Fedora 43, 44, 45, and Rawhide builds for `x86_64` and `aarch64` in COPR.
Run **Build Fedora packages** with publication enabled after you review the bundled licenses.

## License

uji uses [GPL-3.0-or-later](https://github.com/uji-labs/uji/blob/main/LICENSE).
Bundled dependencies retain their own licenses.
