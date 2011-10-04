Summary: A version control system
Name: cvs
Version: 1.11.23
Release: 8
License: GPL+
Group: Development/Tools
Source0: ftp://ftp.gnu.org/non-gnu/cvs/source/stable/%{version}/cvs-%{version}.tar.bz2
Source1: cvs.xinetd
Source2: cvs.pam
Source3: cvs.sh
Source4: cvs.csh
URL: http://www.cvshome.org/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Requires: nano
BuildRequires: autoconf >= 2.58, automake >= 1.7.9, libtool, zlib-devel, nano
Patch0: cvs-1.11.22-cvspass.patch
Patch1: cvs-1.11.19-extzlib.patch
Patch2: cvs-1.11.19-netbsd-tag.patch
Patch3: cvs-1.11.19-abortabort.patch
Patch4: cvs-1.11.1p1-bs.patch
Patch5: cvs-1.11.21-proxy.patch
Patch7: cvs-1.11.19-logmsg.patch
Patch8: cvs-1.11.19-tagname.patch
Patch9: cvs-1.11.19-comp.patch
Patch11: cvs-1.11.19-tmp.patch
Patch13: cvs-1.11.21-diff.patch
Patch14: cvs-1.11.21-diff-kk.patch
Patch15: cvs-1.11.21-sort.patch
Patch17: cvs-1.11.22-ipv6-proxy.patch
Patch19: cvs-1.11.23-getline64.patch
Patch20: cvs-1.11.22-stdinargs.patch
Patch21: cvs-1.11.23-null.patch
Patch22: cvs-1.11.23-rcs.patch

%description
CVS (Concurrent Versions System) is a version control system that can
record the history of your files (usually, but not always, source
code). CVS only stores the differences between versions, instead of
every version of every file you have ever created. CVS also keeps a log
of who, when, and why changes occurred.

CVS is very helpful for managing releases and controlling the
concurrent editing of source files among multiple authors. Instead of
providing version control for a collection of files in a single
directory, CVS provides version control for a hierarchical collection
of directories consisting of revision controlled files. These
directories and files can then be combined together to form a software
release.

%prep
%setup -q
%patch0 -p1 -b .cvspass
%patch1 -p1 -b .extzlib
%patch2 -p1 -b .netbsd-tag
%patch3 -p1 -b .abortabort
%patch4 -p1 -b .bs
%patch5 -p1 -b .proxy
%patch7 -p1 -b .log
%patch8 -p1
%patch9 -p1
%patch11 -p1 -b .tmp

%patch13 -p1 -b .diff
%patch14 -p1 -b .diff-kk
%patch15 -p1 -b .env
%patch17 -p1 -b .ipv6
%patch19 -p1 -b getline64
%patch20 -p1 -b .stdinargs
%patch21 -p1
%patch22 -p1 -b .rcs

%build
%reconfigure CFLAGS="$CFLAGS $RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE" \
  CSH=/bin/csh \
  --with-editor

make


%install
rm -rf $RPM_BUILD_ROOT
%make_install

# forcefully compress the info pages so that install-info will work properly
# in the %%post
gzip $RPM_BUILD_ROOT/%{_infodir}/cvs* || true
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
install -D -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/xinetd.d/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/%{name}
install -D -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/cvs.sh
install -D -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/cvs.csh
# Don't let find provides to add csh to automatic requires
chmod a-x $RPM_BUILD_ROOT/%{_datadir}/%{name}/contrib/sccs2rcs

%check
if [ `id -u` -ne 0 ] ; then
	make check
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info /%{_infodir}/cvs.info.gz /%{_infodir}/dir &> /dev/null
/sbin/install-info /%{_infodir}/cvsclient.info.gz /%{_infodir}/dir &> /dev/null
:

%preun
if [ $1 = 0 ]; then
	/sbin/install-info --delete /%{_infodir}/cvs.info.gz /%{_infodir}/dir &> /dev/null
	/sbin/install-info --delete /%{_infodir}/cvsclient.info.gz /%{_infodir}/dir &> /dev/null
fi
:

%files
%defattr(-,root,root)
%doc AUTHORS BUGS COPYING* DEVEL-CVS FAQ HACKING MINOR-BUGS NEWS
%doc PROJECTS TODO README
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/*.info*
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/xinetd.d/%{name}
%dir %{_localstatedir}/%{name}
%{_sysconfdir}/profile.d/*

