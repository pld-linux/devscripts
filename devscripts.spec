%include	/usr/lib/rpm/macros.perl
Summary:	Scripts for Debian Package maintainers
Name:		devscripts
Version:	2.13.9
Release:	0.1
License:	GPL v2+
Group:		Development
Source0:	http://ftp.debian.org/debian/pool/main/d/devscripts/%{name}_%{version}.tar.xz
# Source0-md5:	a55e715d41cd45c465fa937683e8e5dd
# Fixes path to xsl-stylesheet manpages docbook.xsl
Patch0:		%{name}_docbook.patch
# Removes the debian-only --install-layout python-setuptools option
Patch1:		%{name}_install-layout.patch
# Install some additional man pages
Patch2:		%{name}_install-man.patch
URL:		http://packages.debian.org/unstable/admin/devscripts
BuildRequires:	docbook-style-xsl
BuildRequires:	dpkg
BuildRequires:	libxslt
BuildRequires:	perl-DB_File
BuildRequires:	perl-File-DesktopEntry
BuildRequires:	perl-Parse-DebControl
BuildRequires:	perl-base
BuildRequires:	perl-libwww
BuildRequires:	perl-modules
BuildRequires:	po4a
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
# man for manpage-alert
Requires:	%{_bindir}/man
Requires:	checkbashisms = %{version}-%{release}
#Requires:	dpkg-dev
Conflicts:	rpmdevtools < 8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scripts to make the life of a Debian Package maintainer easier.

%package -n checkbashisms
Summary:	Check shell scripts for common bash-specific contructs

%description -n checkbashisms
checkbashisms checks whether a /bin/sh script contains any common
bash-specific contructs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# Search for libvfork in %{_libdir}/%{name}
sed -i 's|%{_prefix}/lib/devscripts/libvfork.so.0|%{_libdir}/%{name}/libvfork.so.0|g' scripts/dpkg-depcheck.pl

%build
# LIBDIR determines where libvfork gets installed, see scripts/Makefile for LIBDIR
%{__make} \
	LIBDIR=%{_libdir}/%{name} \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
%make_install \
	LIBDIR=%{_libdir}/%{name}

# Install docs through %doc
rm -rf $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/checkbashisms
%{_mandir}/man1/*
%exclude %{_mandir}/man1/checkbashisms.1*
%{_libdir}/%{name}
%{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}*.egg-info
%{_datadir}/%{name}

%{_sysconfdir}/bash_completion.d/*

%files -n checkbashisms
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/checkbashisms
%{_mandir}/man1/checkbashisms.1*
