# RPM files for Besu

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/package/besu/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/package/besu/)

Built on Fedora Copr at https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/

## How to build the RPM locally

Make srpm:
```
$ make -f .copr/Makefile srpm outdir=. spec=besu.spec
```

Make rpm:
```
$ mock --rebuild --enable-network ./besu-${VERSION}.src.rpm
```
