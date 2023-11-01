Name: kernelshark
Version: 1.2
Release: 10%{?dist}
Epoch: 1

# As of 1.1, only kernelshark.cpp, kshark-record.cpp and examples are GPL-2.0. The rest of kernel-shark is LGPL-2.1.
# See SPDX identifier for most accurate info
License: GPLv2 and LGPLv2
Summary: GUI analysis for Ftrace data captured by trace-cmd

URL: https://kernelshark.org
Source0: https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/trace-cmd-kernelshark-v%{version}.tar.gz
Source1: %{name}.appdata.xml
Patch0: 0001-Do-not-install-trace-cmd-when-only-building-kernelsh.patch

BuildRequires: cmake 
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: graphviz
BuildRequires: libappstream-glib
BuildRequires: pkgconf
BuildRequires: pkgconfig(glut)
BuildRequires: pkgconfig(json-c)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: libtracecmd
BuildRequires: libtracecmd-devel
BuildRequires: xmlto
BuildRequires: make
BuildRequires: asciidoc
Requires: polkit


%description
KernelShark is a front end reader of trace-cmd output. "trace-cmd
record" and "trace-cmd extract" create a trace.dat (trace-cmd.dat)
file. kernelshark can read this file and produce a graph and list
view of its data. 

%prep
%autosetup -n trace-cmd-%{name}-v%{version}

%build
# MANPAGE_DOCBOOK_XSL define is hack to avoid using locate
# -z muldefs to workaround the enforcing multi definition check of gcc10.
#   and it need to be removed once upstream fixed the variable name
# Do not use parallel compile because it makes compiling fail
MANPAGE_DOCBOOK_XSL=`rpm -ql docbook-style-xsl | grep manpages/docbook.xsl`
CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs" BUILD_TYPE=Release \
  make -p V=9999999999 MANPAGE_DOCBOOK_XSL=$MANPAGE_DOCBOOK_XSL \
  prefix=%{_prefix} libdir=%{_libdir} gui doc_gui

%install
make libdir=%{_libdir} prefix=%{_prefix} V=1 DESTDIR=%{buildroot}/ CFLAGS="%{optflags} -D_GNU_SOURCE" LDFLAGS="%{build_ldflags} -z muldefs " BUILD_TYPE=Release install_gui install_doc_gui
find %{buildroot}%{_datadir} -type f | xargs chmod u-x,g-x,o-x
find %{buildroot}%{_libdir} -type f -iname "*.so" | xargs chmod 0755
sed -i '/Version/d' %{buildroot}/%{_datadir}/applications/kernelshark.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/kernelshark.desktop
mkdir -p %{buildroot}%{_metainfodir}/
cp %{SOURCE1} %{buildroot}%{_metainfodir}/
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%files
%license COPYING
%doc COPYING.LIB README
%{_bindir}/kernelshark
%{_bindir}/kshark-record
%{_bindir}/kshark-su-record
%dir %{_libdir}/kernelshark
%{_libdir}/kernelshark/*
%{_datadir}/applications/kernelshark.desktop
%dir %{_datadir}/icons/kernelshark
%{_datadir}/icons/kernelshark/*
%{_datadir}/polkit-1/actions/org.freedesktop.kshark-record.policy
%{_metainfodir}/%{name}.appdata.xml
%docdir %{_datadir}/%{name}/html
%{_datadir}/%{name}/html/*
%{_mandir}/man1/*

%changelog
* Mon Dec 12 2022 Jerome Marchand <jmarchan@redhat.com> - 1:1.2-10
- Add html documentation and man page

* Mon Nov 22 2021 Jerome Marchand <jmarchan@redhat.com> - 1:1.2-9
- Rebuild with latest json-c

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com>
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Mon May 03 21 Jerome Marchand <jmarchan@redhat.com> - 1:1.2-7
- libtracecmd is a subpackage of trace-cmd for now

* Thu Apr 22 2021 Jerome Marchand <jmarchan@redhat.com> - 1:1.2-6
- libtracecmd is not yet available on c9s/el9

* Mon Apr 19 2021 Jerome Marchand <jmarchan@redhat.com> - 1:1.2-5
- Rebuild with external tracing libs
- Misc cleanup

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1:1.2-4
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 Zamir SUN <sztsian@gmail.coom> - 1.2-2
- Bump epoch to allow updating.

* Mon Oct 12 2020 Zamir SUN <sztsian@gmail.com> - 1.2-1
- Update to 1.2
- Uses trace event plugins from old trace-cmd dir

* Thu Sep 24 2020 Zamir SUN <sztsian@gmail.com> - 1.1-1
- Package kernelshark in a standalone package with 1.1

