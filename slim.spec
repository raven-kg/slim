%define __cmake /usr/bin/cmake28

Name:           slim
Version:        1.3.5
Release:        1%{?dist}
Summary:        Simple Login Manager
Group:          User Interface/X
License:        GPLv2+
URL:            http://slim.berlios.de/
Source0:        http://download.berlios.de/slim/%{name}-%{version}.tar.gz
# stolen from xdm
Source1:        %{name}.pam
# adapted from debian to use freedesktop
Source2:        slim-update_slim_wmlist
Source3:        slim-dynwm
Source4:        slim-readme.txt
# logrotate entry (see bz#573743)
Source5:        slim.logrotate.d
# config file for autostart slim
Source6:        slim.config

# Fedora-specific patches
Patch1:         slim-1.3.3-fedora.patch
Patch2:         slim-1.3.2-selinux.patch

BuildRequires:  libXmu-devel libXft-devel libXrender-devel
BuildRequires:  libpng-devel libjpeg-devel freetype-devel fontconfig-devel
BuildRequires:  pkgconfig gettext libselinux-devel pam-devel cmake28
BuildRequires:  xwd xterm freeglut-devel
Requires:       xwd xterm /sbin/shutdown
Requires:       %{_sysconfdir}/pam.d
# we use 'include' in the pam file, so
Requires:       pam >= 0.80
# reuse the images
Requires:       redhat-logos
# for anaconda yum
Provides:       service(graphical-login)

%description
SLiM (Simple Login Manager) is a graphical login manager for X11.
It aims to be simple, fast and independent from the various
desktop environments.
SLiM is based on latest stable release of Login.app by Per Lidén.

In the distribution, slim may be called through a wrapper, slim-dynwm,
which determines the available window managers using the freedesktop
information and modifies the slim configuration file accordingly,
before launching slim.

%prep
%setup -q -n %{name}-%{version}

%patch1 -p0 -b .fedora
%patch2 -p1 -b .selinux
cp -p %{SOURCE4} README.Fedora

%build
CXXFLAGS="%{optflags}" %{__cmake} -DUSE_PAM=yes -DCMAKE_INSTALL_PREFIX=%{_prefix} .
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL='install -p' MANDIR=%{_mandir}
install -p -m755 %{SOURCE2} %{buildroot}%{_bindir}/update_slim_wmlist
install -p -m755 %{SOURCE3} %{buildroot}%{_bindir}/slim-dynwm
chmod 0644 %{buildroot}%{_sysconfdir}/slim.conf
install -d -m755 %{buildroot}%{_sysconfdir}/pam.d
install -p -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/slim
mkdir -p %{buildroot}%{_localstatedir}/run/slim
# remove garbage
rm -f %{buildroot}/usr/usr/lib/systemd/system/slim.service
# adapt default theme image
rm -f %{buildroot}%{_datadir}/slim/themes/default/background.png
ln -s /usr/share/backgrounds/default.png %{buildroot}%{_datadir}/slim/themes/default/background.png
# install logrotate entry
install -m0644 -D %{SOURCE5} %{buildroot}/%{_sysconfdir}/logrotate.d/slim

# install autostart file
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m0644 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/desktop

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog README* THEMES TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pam.d/slim
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/slim.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/logrotate.d/slim
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/sysconfig/desktop
%ghost %dir %{_localstatedir}/run/slim
%{_bindir}/slim*
%{_bindir}/update_slim_wmlist
%{_mandir}/man1/slim*.1*
%dir %{_datadir}/slim
%{_datadir}/slim/themes/


%changelog
* Tue Feb 12 2013 Raven <raven_kg@megaline.kg> - 1.3.5-1
- Update to 1.3.5.

* Tue Jan 08 2013 Raven <raven_kg@megaline.kg> - 1.3.2-2
- changed interface settings to system defaults

* Mon Jan 07 2013 Raven <raven_kg@megaline.kg> - 1.3.2-1
- Initial packaging for el6
