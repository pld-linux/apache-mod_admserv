%define		apxs		/usr/sbin/apxs
Summary:	mod_admserv - communication link between Console and Directory
Summary(pl):	mod_admserv - po³±czenie komunikacyjne miêdzy konsol± a katalogiem
Name:		apache-mod_admserv
Version:	1.0.3
Release:	0.1
License:	Apache 2.0
Group:		Networking/Daemons
Source0:	http://directory.fedora.redhat.com/sources/mod_admserv-%{version}.tar.gz
# Source0-md5:	793416e0a82b7e7bec42ddaa609e88d9
URL:		http://directory.fedora.redhat.com/wiki/Mod_admserv
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	fedora-adminutil-devel >= 1.0
BuildRequires:	libicu-devel
BuildRequires:	mozldap-devel >= 5.0
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
An Apache 2.0 module for implementing the admin server functionality
required by Fedora Admin Server and Directory Server.

%description -l pl
Modu³ Apache'a 2.0 implementuj±cy funkcjonalno¶æ serwera
administracyjnego wymagan± przez us³ugi Fedora Admin Server i Fedora
Directory Server.

%prep
%setup -q -n mod_admserv-%{version}

%build
# apr-util is missing in configure check
CPPFLAGS="`apu-1-config --includes`"
%configure \
	--with-apr-config \
	--with-apxs=%{apxs} \
	--with-nspr-inc=/usr/include/nspr \
	--with-nspr-lib=%{_libdir} \
	--with-nss-inc=/usr/include/nss \
	--with-nss-lib=%{_libdir} \
	--with-ldapsdk-inc=/usr/include/mozldap \
	--with-ldapsdk-lib=%{_libdir} \
	--with-adminutil=/usr

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install .libs/libmodadmserv.so $RPM_BUILD_ROOT%{_pkglibdir}
# TODO: XX_mod_admserv.conf based on httpd.conf.tmpl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README httpd.conf.tmpl
#%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_admserv.conf
%attr(755,root,root) %{_pkglibdir}/libmodadmserv.so
