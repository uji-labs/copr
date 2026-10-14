%global commit 9a612f15a772921867f8df688e1630f2ae6aa834

Name:           uji
Version:        0.2.3
Release:        1%{?dist}
Summary:        A coding agent with Lua configuration
# Includes vendored dependencies and embedded syntax definitions.
License:        GPL-3.0-or-later AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND MIT AND MPL-2.0 AND Unicode-3.0 AND Zlib AND LicenseRef-Fedora-Public-Domain AND LicenseRef-Two-Face-assets AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Unlicense OR MIT)
URL:            https://github.com/uji-labs/uji
# scripts/build-srpm.sh adds locked dependencies and their notices to the source.
Source0:        uji-%{version}.tar.gz
ExclusiveArch:  x86_64 aarch64

BuildRequires:  cargo >= 1.88
BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconf-pkg-config
BuildRequires:  rust >= 1.88
Requires:       ca-certificates
Requires:       git-core
Requires:       shared-mime-info

%description
uji is a terminal coding agent with an embedded Lua runtime.
Configure models, tools, and plugins with Lua.

%prep
%autosetup
%cargo_prep -N
cat vendor-config.toml >> .cargo/config.toml
%cargo_vendor_manifest
%cargo_license

%build
%cargo_build -- --frozen --package uji

%install
install -Dpm0755 target/rpm/uji %{buildroot}%{_bindir}/uji

%check
test "$(target/rpm/uji --version)" = "uji %{version}"
target/rpm/uji --help

%files
%license LICENSE cargo-vendor.txt bundled-licenses
%doc README.md
%{_bindir}/uji

%changelog
* Wed Oct 14 2026 github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com> - 0.2.3-1
- Update to v0.2.3.

* Mon Oct 12 2026 PiX <69745008+pixincreate@users.noreply.github.com> - 0.2.2-1
- Package the pinned release with locked dependencies and license notices.
