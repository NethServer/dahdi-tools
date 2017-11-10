Summary: The DAHDI project
Name: dahdi-tools
Version: 2.11.1
Release: 1%{dist}
License: GPL
Group: Utilities/System
Source0: https://downloads.asterisk.org/pub/telephony/dahdi-tools/dahdi-tools-%{version}.tar.gz
Patch0: echocan_oslec.patch
Patch1: init_unload_oslec.patch
Patch2: 0001-blacklist.sample.patch
Patch3: 0001-Chans.pm.patch
Patch4: 0001-modules.sample.patch
Patch5: 0001-PCI.pm.patch
Patch6: 0001-Span.pm.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
URL: http://www.asterisk.org/
Vendor: Digium, Inc.
Packager: NethServer <info@nethesis.it>
%{!?_without_newt:Requires: newt}
%{!?_without_newt:BuildRequires: newt-devel}
BuildRequires: libusb-devel
Requires: dahdi-linux
BuildRequires: dahdi-linux-devel

%description
The open source DAHDI project

%package doc
Summary: Documentation files for DAHDI
Group: Development/Libraries

%description doc
The Documentation files for DAHDI

%package -n libtonezone
Summary: Libtonezone, from the open source DAHDI project
Group: Development/Libraries

%description -n libtonezone
libtonezone is a component from the open source DAHDI project

%package -n libtonezone-devel
Summary: Libtonezone libraries and header files for libtonezone development
Group: Development/Libraries
Requires: libtonezone = %{version}-%{release}

%description -n libtonezone-devel
The static libraries and header files needed for building additional plugins/modules

%package        libs
Summary:        Library files for DAHDI
Group:          Development/Libraries
Conflicts:      zaptel-lib

%description    libs
The dahdi-tools-libs package contains libraries for accessing DAHDI hardware.

%package        devel
Summary:        Development files for DAHDI
Group:          Development/Libraries
Requires:       dahdi-tools-libs%{?_isa} = %{version}-%{release}

%description    devel
The dahdi-devel package contains libraries and header files for
developing applications that use DAHDI hardware.

%prep
%setup -n %{name}-%{version}
%patch0
%patch1
%patch2 -p1
%patch3 -p1
%patch4 -p1 -F2
%patch5 -p1
%patch6 -p1

%build
echo %{version} > .version
%configure
make

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/network-scripts/
mkdir -p $RPM_BUILD_ROOT/$(sysconfdir)/modprobe.d/
mkdir -p $RPM_BUILD_ROOT/{_sysconfdir}/dahdi/
make DESTDIR=$RPM_BUILD_ROOT install
make DESTDIR=$RPM_BUILD_ROOT install-config
make DESTDIR=$RPM_BUILD_ROOT config
cp dahdi.init $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/dahdi
cp modules.sample $RPM_BUILD_ROOT/%{_sysconfdir}/dahdi/modules

%post
# Dahdi is started by fwconsole, via systemd
chkconfig --del dahdi

%clean
cd $RPM_BUILD_DIR
%{__rm} -rf %{name}-%{version}
%{__rm} -rf /var/log/%{name}-sources-%{version}-%{release}.make.err
%{__rm} -rf $RPM_BUILD_ROOT

%files
%{_sbindir}/*
#%config %{_sysconfdir}/hotplug/
%config(noreplace) %{_sysconfdir}/dahdi/
%config %{_sysconfdir}/init.d/dahdi
%config %{_sysconfdir}/modprobe.d/dahdi.conf
%config %{_sysconfdir}/modprobe.d/dahdi-blacklist.conf
%config %{_sysconfdir}/udev/rules.d/dahdi.rules
%config %{_sysconfdir}/udev/rules.d/xpp.rules
%config %{_sysconfdir}/sysconfig/network-scripts/ifup-hdlc
%config %{_sysconfdir}/bash_completion.d/dahdi
/usr/share/dahdi/
%{perl_sitelib}

%files doc
%{_mandir}/man8/

%files -n libtonezone
%defattr(-, root, root)
%{_libdir}/libtonezone.so
%{_libdir}/libtonezone.so.2
%{_libdir}/libtonezone.so.2.0
#%{_libdir}/libtonezone.so.1
#%{_libdir}/libtonezone.so.1.0
%{_libdir}/libtonezone.la
%{_libdir}/libtonezone.so.2.0.0

%files -n libtonezone-devel
%defattr(-, root, root)
%{_includedir}/dahdi/tonezone.h
%{_libdir}/libtonezone.a

%files libs
%defattr(-,root,root,-)
%doc LICENSE LICENSE.LGPL
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE LICENSE.LGPL
%{_includedir}/*
%{_libdir}/*.so
