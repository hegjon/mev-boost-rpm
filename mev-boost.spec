%global debug_package %{nil}
%global _build_id_links none

Name:    mev-boost
Version: 1.8
Release: 1%{?dist}
Summary: An implementation of proposer-builder separation (PBS) for Ethereum

License: MIT
URL:     https://github.com/flashbots/mev-boost

Source0: https://github.com/flashbots/mev-boost/archive/refs/tags/v%{version}.tar.gz

Source1: mev-boost@.service
Source2: mev-boost.conf
Source3: mainnet.conf

BuildRequires: go
BuildRequires: make
BuildRequires: git

%if 0%{?mageia} > 0
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%endif

%{?systemd_requires}

%description
mev-boost is open source middleware run by validators to access a competitive \
block-building market. MEV-Boost is an initial implementation of \
proposer-builder separation (PBS) for proof-of-stake (PoS) Ethereum.

With MEV-Boost, validators can access blocks from a marketplace of builders. \
Builders produce blocks containing transaction orderflow and a fee for the \
block proposing validator. Separating the role of proposers from \
block builders promotes greater competition, decentralization, \
and censorship-resistance for Ethereum.


%prep
%setup -n %{name}-%{version}
cp %{SOURCE2} .

%build
make build VERSION="%{version}-rpm"

%install
install -dD -m 755 %{buildroot}%{_bindir}

install -m 0755 mev-boost %{buildroot}%{_bindir}/mev-boost

install -dD -m 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

install -dD -m 755 %{buildroot}%{_sysconfdir}/mev-boost
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/mev-boost/mainnet.conf

install -dD -m 0755 %{buildroot}%{_sharedstatedir}/mev-boost

%pre
getent group mev-boost >/dev/null || groupadd -r mev-boost
getent passwd mev-boost >/dev/null || \
  useradd -r -g mev-boost -s /sbin/nologin \
    -d %{_sharedstatedir}/mev-boost \
    -c 'MEV-Boost' mev-boost
exit 0


%post
%systemd_post mev-boost@.service

%preun
%systemd_preun mev-boost@.service

%postun
%systemd_postun_with_restart mev-boost@\*.service

%files
%license LICENSE
%doc CODE_OF_CONDUCT.md CONTRIBUTING.md README.md RELEASE.md SECURITY.md
%doc mev-boost.conf
%config %dir %attr(0755,root,root) %{_sysconfdir}/mev-boost/
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/mev-boost/mainnet.conf
%{_bindir}/mev-boost
%{_unitdir}/mev-boost@.service
%attr(0755,mev-boost,mev-boost) %{_sharedstatedir}/mev-boost

%changelog
* Mon Sep 09 2024 Jonny Heggheim <hegjon@gmail.com> - 1.8-1
- Updated to version 1.8

* Sun Mar 03 2024 Jonny Heggheim <hegjon@gmail.com> - 1.7-1
- Updated to version 1.7

* Sat Dec 02 2023 Jonny Heggheim <hegjon@gmail.com> - 1.6-3
- DefaultInstance in systemd unit file belongs to the Install section

* Fri Dec 01 2023 Jonny Heggheim <hegjon@gmail.com> - 1.6-2
- Improved systemd setup

* Thu Nov 30 2023 Jonny Heggheim <hegjon@gmail.com> - 1.6-1
- Inital packaging
