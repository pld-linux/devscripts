# TODO
# - bash-completions subpackage
# - some junk installed to root: "/devscripts.*"
Summary:	Scripts for Debian Package maintainers
Name:		devscripts
Version:	2.18.6
Release:	4
License:	GPL v2+
Group:		Development
Source0:	http://ftp.debian.org/debian/pool/main/d/devscripts/%{name}_%{version}.tar.xz
# Source0-md5:	999be6ee14d60fade4d173283152dd2e
Patch0:		%{name}_docbook.patch
Patch1:		%{name}_install-layout.patch
Patch2:		%{name}_install-man.patch
URL:		https://packages.debian.org/unstable/admin/devscripts
BuildRequires:	docbook-dtd42-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	dpkg
BuildRequires:	gettext-tools
BuildRequires:	libxslt
BuildRequires:	libxslt-progs
BuildRequires:	perl-DB_File
BuildRequires:	perl-File-DesktopEntry
BuildRequires:	perl-TimeDate
BuildRequires:	perl-base
BuildRequires:	perl-libwww
BuildRequires:	perl-modules
BuildRequires:	pkgconfig
BuildRequires:	po4a
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.673
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
BuildArch:	noarch

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

# python paths
%{__sed} -i -e 's#setup.py install #setup.py install --prefix=%{_prefix} --install-purelib=%{py3_sitescriptdir} --install-platlib=%{py3_sitedir} #g' scripts/Makefile

%build
# LIBDIR determines where libvfork gets installed, see scripts/Makefile for LIBDIR
%{__make} \
	LIBDIR=%{_libdir}/%{name} \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="$RPM_LD_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR=%{_libdir}/%{name}

# Install docs through %doc
rm -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/add-patch
%attr(755,root,root) %{_bindir}/annotate-output
%attr(755,root,root) %{_bindir}/archpath
%attr(755,root,root) %{_bindir}/bts
%attr(755,root,root) %{_bindir}/build-rdeps
%attr(755,root,root) %{_bindir}/chdist
%attr(755,root,root) %{_bindir}/cowpoke
%attr(755,root,root) %{_bindir}/cvs-debi
%attr(755,root,root) %{_bindir}/cvs-debrelease
%attr(755,root,root) %{_bindir}/cvs-debuild
%attr(755,root,root) %{_bindir}/dcmd
%attr(755,root,root) %{_bindir}/dcontrol
%attr(755,root,root) %{_bindir}/dd-list
%attr(755,root,root) %{_bindir}/deb-reversion
%attr(755,root,root) %{_bindir}/debc
%attr(755,root,root) %{_bindir}/debchange
%attr(755,root,root) %{_bindir}/debcheckout
%attr(755,root,root) %{_bindir}/debclean
%attr(755,root,root) %{_bindir}/debcommit
%attr(755,root,root) %{_bindir}/debdiff
%attr(755,root,root) %{_bindir}/debdiff-apply
%attr(755,root,root) %{_bindir}/debi
%attr(755,root,root) %{_bindir}/debpkg
%attr(755,root,root) %{_bindir}/debrelease
%attr(755,root,root) %{_bindir}/debrepro
%attr(755,root,root) %{_bindir}/debrsign
%attr(755,root,root) %{_bindir}/debsign
%attr(755,root,root) %{_bindir}/debsnap
%attr(755,root,root) %{_bindir}/debuild
%attr(755,root,root) %{_bindir}/dep3changelog
%attr(755,root,root) %{_bindir}/desktop2menu
%attr(755,root,root) %{_bindir}/dget
%attr(755,root,root) %{_bindir}/diff2patches
%attr(755,root,root) %{_bindir}/dpkg-depcheck
%attr(755,root,root) %{_bindir}/dpkg-genbuilddeps
%attr(755,root,root) %{_bindir}/dscextract
%attr(755,root,root) %{_bindir}/dscverify
%attr(755,root,root) %{_bindir}/edit-patch
%attr(755,root,root) %{_bindir}/getbuildlog
%attr(755,root,root) %{_bindir}/git-deborig
%attr(755,root,root) %{_bindir}/grep-excuses
%attr(755,root,root) %{_bindir}/hardening-check
%attr(755,root,root) %{_bindir}/list-unreleased
%attr(755,root,root) %{_bindir}/ltnu
%attr(755,root,root) %{_bindir}/manpage-alert
%attr(755,root,root) %{_bindir}/mass-bug
%attr(755,root,root) %{_bindir}/mergechanges
%attr(755,root,root) %{_bindir}/mk-build-deps
%attr(755,root,root) %{_bindir}/mk-origtargz
%attr(755,root,root) %{_bindir}/namecheck
%attr(755,root,root) %{_bindir}/nmudiff
%attr(755,root,root) %{_bindir}/origtargz
%attr(755,root,root) %{_bindir}/plotchangelog
%attr(755,root,root) %{_bindir}/pts-subscribe
%attr(755,root,root) %{_bindir}/rc-alert
%attr(755,root,root) %{_bindir}/reproducible-check
%attr(755,root,root) %{_bindir}/rmadison
%attr(755,root,root) %{_bindir}/sadt
%attr(755,root,root) %{_bindir}/suspicious-source
%attr(755,root,root) %{_bindir}/svnpath
%attr(755,root,root) %{_bindir}/tagpending
%attr(755,root,root) %{_bindir}/transition-check
%attr(755,root,root) %{_bindir}/uscan
%attr(755,root,root) %{_bindir}/uupdate
%attr(755,root,root) %{_bindir}/what-patch
%attr(755,root,root) %{_bindir}/who-permits-upload
%attr(755,root,root) %{_bindir}/who-uploads
%attr(755,root,root) %{_bindir}/whodepends
%attr(755,root,root) %{_bindir}/wnpp-alert
%attr(755,root,root) %{_bindir}/wnpp-check
%attr(755,root,root) %{_bindir}/wrap-and-sort
%{_mandir}/man1/add-patch.1
%{_mandir}/man1/annotate-output.1*
%{_mandir}/man1/archpath.1*
%{_mandir}/man1/bts.1*
%{_mandir}/man1/build-rdeps.1*
%{_mandir}/man1/chdist.1*
%{_mandir}/man1/cowpoke.1*
%{_mandir}/man1/cvs-debc.1*
%{_mandir}/man1/cvs-debi.1*
%{_mandir}/man1/cvs-debrelease.1*
%{_mandir}/man1/cvs-debuild.1*
%{_mandir}/man1/dcmd.1*
%{_mandir}/man1/dcontrol.1*
%{_mandir}/man1/dd-list.1*
%{_mandir}/man1/deb-reversion.1*
%{_mandir}/man1/debc.1*
%{_mandir}/man1/debchange.1*
%{_mandir}/man1/debcheckout.1*
%{_mandir}/man1/debclean.1*
%{_mandir}/man1/debcommit.1*
%{_mandir}/man1/debdiff-apply.1*
%{_mandir}/man1/debdiff.1*
%{_mandir}/man1/debi.1*
%{_mandir}/man1/debpkg.1*
%{_mandir}/man1/debrelease.1*
%{_mandir}/man1/debrepro.1*
%{_mandir}/man1/debrsign.1*
%{_mandir}/man1/debsign.1*
%{_mandir}/man1/debsnap.1*
%{_mandir}/man1/debuild.1*
%{_mandir}/man1/dep3changelog.1*
%{_mandir}/man1/desktop2menu.1*
%{_mandir}/man1/devscripts.1*
%{_mandir}/man1/dget.1*
%{_mandir}/man1/diff2patches.1*
%{_mandir}/man1/dpkg-depcheck.1*
%{_mandir}/man1/dpkg-genbuilddeps.1*
%{_mandir}/man1/dscextract.1*
%{_mandir}/man1/dscverify.1*
%{_mandir}/man1/edit-patch.1*
%{_mandir}/man1/getbuildlog.1*
%{_mandir}/man1/git-deborig.1*
%{_mandir}/man1/grep-excuses.1*
%{_mandir}/man1/hardening-check.1*
%{_mandir}/man1/list-unreleased.1*
%{_mandir}/man1/ltnu.1*
%{_mandir}/man1/manpage-alert.1*
%{_mandir}/man1/mass-bug.1*
%{_mandir}/man1/mergechanges.1*
%{_mandir}/man1/mk-build-deps.1*
%{_mandir}/man1/mk-origtargz.1*
%{_mandir}/man1/namecheck.1*
%{_mandir}/man1/nmudiff.1*
%{_mandir}/man1/origtargz.1*
%{_mandir}/man1/plotchangelog.1*
%{_mandir}/man1/pts-subscribe.1*
%{_mandir}/man1/rc-alert.1*
%{_mandir}/man1/reproducible-check.1*
%{_mandir}/man1/rmadison.1*
%{_mandir}/man1/sadt.1*
%{_mandir}/man1/suspicious-source.1*
%{_mandir}/man1/svnpath.1*
%{_mandir}/man1/tagpending.1*
%{_mandir}/man1/transition-check.1*
%{_mandir}/man1/uscan.1*
%{_mandir}/man1/uupdate.1*
%{_mandir}/man1/what-patch.1*
%{_mandir}/man1/who-permits-upload.1*
%{_mandir}/man1/who-uploads.1*
%{_mandir}/man1/whodepends.1*
%{_mandir}/man1/wnpp-alert.1*
%{_mandir}/man1/wnpp-check.1*
%{_mandir}/man1/wrap-and-sort.1*
%{py3_sitescriptdir}/%{name}
%{py3_sitescriptdir}/%{name}*.egg-info
%{_datadir}/%{name}
%{perl_vendorlib}/Devscripts
%{bash_compdir}/bts
%{bash_compdir}/build-rdeps
%{bash_compdir}/chdist
%{bash_compdir}/checkbashisms
%{bash_compdir}/dch
%{bash_compdir}/dcontrol
%{bash_compdir}/dd-list
%{bash_compdir}/debc
%{bash_compdir}/debchange
%{bash_compdir}/debcheckout
%{bash_compdir}/debdiff
%{bash_compdir}/debi
%{bash_compdir}/debsign
%{bash_compdir}/debsnap
%{bash_compdir}/debuild
%{bash_compdir}/dget
%{bash_compdir}/dscextract
%{bash_compdir}/dscverify
%{bash_compdir}/getbuildlog
%{bash_compdir}/grep-excuses
%{bash_compdir}/list-unreleased
%{bash_compdir}/mass-bug
%{bash_compdir}/mk-build-deps
%{bash_compdir}/mk-origtargz
%{bash_compdir}/pkgnames
%{bash_compdir}/plotchangelog
%{bash_compdir}/pts-subscribe
%{bash_compdir}/pts-unsubscribe
%{bash_compdir}/rc-alert
%{bash_compdir}/rmadison
%{bash_compdir}/transition-check
%{bash_compdir}/uscan
%{bash_compdir}/uupdate
%{bash_compdir}/what-patch
%{bash_compdir}/who-uploads
%{bash_compdir}/whodepends
%{bash_compdir}/wnpp-alert
%{bash_compdir}/wnpp-check

%files -n checkbashisms
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/checkbashisms
%{_mandir}/man1/checkbashisms.1*
