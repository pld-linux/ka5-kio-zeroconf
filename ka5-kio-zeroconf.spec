#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	22.08.1
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kio-zeroconf
Summary:	kio zeroconf
Summary(pl.UTF-8):	kio zeroconf
Name:		ka5-%{kaname}
Version:	22.08.1
Release:	1
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	cdbd931a7edaf7411f704ef658610186
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel
BuildRequires:	gettext-devel
BuildRequires:	kf5-extra-cmake-modules >= %{kframever}
BuildRequires:	kf5-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf5-kdnssd-devel >= %{kframever}
BuildRequires:	kf5-ki18n-devel >= %{kframever}
BuildRequires:	kf5-kio-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt5-build >= 5.9.0
BuildRequires:	rpmbuild(macros) >= 1.164
Obsoletes:	ka5-zeroconf-ioslave < 22.08.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kio Zeroconf.

%prep
%setup -q -n %{kaname}-%{version}

%build
install -d build
cd build
%cmake \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%if %{with tests}
ctest
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_libdir}/qt5/plugins/kf5/kded/dnssdwatcher.so
%{_libdir}/qt5/plugins/kf5/kio/zeroconf.so
%{_datadir}/dbus-1/interfaces/org.kde.kdnssd.xml
%{_datadir}/remoteview/zeroconf.desktop
%{_datadir}/metainfo/org.kde.kio_zeroconf.metainfo.xml
