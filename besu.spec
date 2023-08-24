Name:    besu
Version: 23.7.1
Release: 1%{?dist}
Summary: An enterprise-grade Java-based Ethereum client

License: Apache-2.0
URL:     https://www.hyperledger.org/projects/besu

Source0:  https://github.com/hyperledger/besu/archive/refs/tags/%{version}.tar.gz

Source1:  besu.service

Requires: java-headless
Requires: javapackages-tools
BuildRequires: javapackages-tools


%if 0%{?mageia} > 0
BuildRequires: systemd
%else
BuildRequires: systemd-rpm-macros
%endif

%{?systemd_requires}

%description
Besu is an Apache 2.0 licensed, MainNet compatible, Ethereum client written in Java.


%prep
%setup -n %{name}-%{version}


%build
./gradlew installDist

%install
install -dD -m 755 %{buildroot}%{_bindir}


install -dD -m 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

install -dD -m 0755 %{buildroot}%{_sharedstatedir}/besu


install -dD -m 0750 %{buildroot}%{_sysconfdir}/storj-storagenode

%pre
getent group besu >/dev/null || groupadd -r besu
getent passwd besu >/dev/null || \
  useradd -r -g besu -s /sbin/nologin \
    -d %{_sharedstatedir}/besu \
    -c 'Besu' besu
exit 0


%post
%systemd_post besu.service

%preun
%systemd_preun besu.service

%postun
%systemd_postun_with_restart besu.service


%files
%config %dir %attr(-,-,besu) %{_sysconfdir}/besu
%{_bindir}/besu
%{_unitdir}/besu.service
%attr(0755,besu,besu) %{_sharedstatedir}/besu
%{_datadir}/besu


%changelog
* Thu Aug 24 2023 Jonny Heggheim <hegjon@gmail.com> - 23.7.1-1
- Inital packaging
