# TODO
# - bash-completions subpackage
%include	/usr/lib/rpm/macros.perl
Summary:	Scripts for Debian Package maintainers
Name:		devscripts
Version:	2.15.1
Release:	1
License:	GPL v2+
Group:		Development
Source0:	http://ftp.debian.org/debian/pool/main/d/devscripts/%{name}_%{version}.tar.xz
# Source0-md5:	7c46c0f19205d2022184972ce6390a15
Patch0:		%{name}_docbook.patch
Patch1:		%{name}_install-layout.patch
Patch2:		%{name}_install-man.patch
URL:		https://packages.debian.org/unstable/admin/devscripts
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
#Requires:	sensible-utils
Conflicts:	rpmdevtools < 8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scripts to make the life of a Debian Package maintainer easier.

%package -n checkbashisms
Summary:	Check shell scripts for common bash-specific contructs
Group:		Development
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n checkbashisms
checkbashisms checks whether a /bin/sh script contains any common
bash-specific contructs.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

# PLD package names
# grep -r 'you must have the.*package installed' .
%{__sed} -i -e 's/liburi-perl/perl-URI/g' scripts/*.pl
%{__sed} -i -e 's/liblwp-protocol-https-perl/perl-LWP-Protocol-https/g' scripts/*.pl
%{__sed} -i -e 's/libtimedate-perl/perl-TimeDate/g' scripts/*.pl
%{__sed} -i -e 's/libfile-desktopentry-perl/perl-File-DesktopEntry/g' scripts/*.pl
%{__sed} -i -e 's/libwww-perl/perl-libwww/g' scripts/*.pl
%{__sed} -i -e 's/libdigest-md5-perl/perl-Digest-MD5/g' scripts/*.pl

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
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}/%{name}

# Install docs through %doc
rm -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README COPYING
%attr(755,root,root) %{_bindir}/*
%exclude %{_bindir}/checkbashisms
%{_mandir}/man1/*
%exclude %{_mandir}/man1/checkbashisms.1*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/libvfork.so.0
%{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}*.egg-info
%{_datadir}/%{name}

/etc/bash_completion.d/*

%files -n checkbashisms
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/checkbashisms
%{_mandir}/man1/checkbashisms.1*
