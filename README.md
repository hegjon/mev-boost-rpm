# RPM files for MEV-Boost

[![Copr build status](https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/package/mev-boost/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/package/mev-boost/)

Built on Fedora Copr at https://copr.fedorainfracloud.org/coprs/jonny/Ethereum/

## How to build the RPM locally

Make srpm:
```
$ make -f .copr/Makefile srpm outdir=. spec=mev-boost.spec
```

Make rpm:
```
$ mock --rebuild --enable-network ./mev-boost-${VERSION}.src.rpm
```
