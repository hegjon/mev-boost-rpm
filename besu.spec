Name:    besu
Version: 23.7.1
Release: 1%{?dist}
Summary: An enterprise-grade Java-based Ethereum client

License: Apache-2.0
URL:     https://www.hyperledger.org/projects/besu

Source0:  https://github.com/hyperledger/besu/archive/refs/tags/%{version}.tar.gz

Source1:  besu.service
Source2:  besu.conf

Requires: java-headless
Requires: javapackages-tools
BuildRequires: javapackages-tools

#Debugging the build
BuildRequires: tree

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
./gradlew --no-daemon --console plain installDist

tree build

%install
install -dD -m 755 %{buildroot}%{_bindir}

install -m 0755 build/install/besu/bin/besu %{buildroot}%{_bindir}/besu
install -m 0755 build/install/besu/bin/evmtool %{buildroot}%{_bindir}/evmtool

install -dD -m 755 %{buildroot}%{_javadir}/%{name}/
install -m 644 build/install/besu/lib/*.jar %{buildroot}%{_javadir}/%{name}/

install -dD -m 755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

install -D -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/besu.conf

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
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/besu.conf
%{_bindir}/besu
%{_bindir}/evmtool
%{_unitdir}/besu.service
%{_datadir}/besu
%{_javadir}/%{name}/


%changelog
* Thu Aug 24 2023 Jonny Heggheim <hegjon@gmail.com> - 23.7.1-1
- Inital packaging
