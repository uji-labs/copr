#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
spec="$root/uji.spec"
version=$(rpmspec -q --srpm --qf '%{VERSION}' "$spec")
commit=$(sed -n 's/^%global commit //p' "$spec")
output="$root/dist"

if [[ -e $output ]]; then
    echo 'Remove dist before building another source package.' >&2
    exit 1
fi

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
export CARGO_HOME="$work/cargo-home"
export RUSTC=/usr/bin/rustc

source="$work/uji-$version"
git clone --quiet --depth 1 --branch "v$version" https://github.com/uji-labs/uji.git "$source"
if [[ $(git -C "$source" rev-parse HEAD) != "$commit" ]]; then
    echo 'The release tag does not match the commit in uji.spec.' >&2
    exit 1
fi
epoch=$(git -C "$source" show -s --format=%ct HEAD)

cd "$source"
/usr/bin/cargo vendor --locked --versioned-dirs vendor > vendor-config.toml
python3 "$root/scripts/licenses.py" "$source"

mkdir -p "$work/rpmbuild/SOURCES"
# Keep source permissions and use the release time for archive entries.
tar --sort=name --mtime="@$epoch" --owner=0 --group=0 --numeric-owner \
    --exclude=.git -C "$work" -cf - "uji-$version" \
    | gzip -n > "$work/rpmbuild/SOURCES/uji-$version.tar.gz"
rpmbuild -bs --define "_topdir $work/rpmbuild" "$spec"

mkdir "$output"
cp "$work/rpmbuild/SRPMS/"*.src.rpm "$output/"
cd "$output"
sha256sum ./*.src.rpm > SHA256SUMS
