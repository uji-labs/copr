ARG FEDORA=44
FROM registry.fedoraproject.org/fedora:${FEDORA}

RUN dnf install -y --setopt=install_weak_deps=False \
        ca-certificates \
        cargo \
        cargo-rpm-macros \
        curl \
        gcc \
        git-core \
        gzip \
        make \
        mock \
        pkgconf-pkg-config \
        python3 \
        redhat-rpm-config \
        rpm-build \
        rpmlint \
        rust \
        shared-mime-info \
        tar \
    && dnf clean all

WORKDIR /packaging
