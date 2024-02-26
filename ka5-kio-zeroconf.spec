#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.01.95
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		kio-zeroconf
Summary:	kio zeroconf
Summary(pl.UTF-8):	kio zeroconf
Name:		ka5-%{kaname}
Version:	24.01.95
Release:	0.1
License:	GPL v2+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	23714f64488ef1c8a52b35715cad40d3
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdnssd-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= 5.9.0
BuildRequires:	rpmbuild(macros) >= 1.164
Obsoletes:	ka5-zeroconf-ioslave < 22.08.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kio Zeroconf.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DQT_MAJOR_VERSION=6
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/dnssdwatcher.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/zeroconf.so
%{_datadir}/dbus-1/interfaces/org.kde.kdnssd.xml
%{_datadir}/remoteview/zeroconf.desktop
%{_datadir}/metainfo/org.kde.kio_zeroconf.metainfo.xml
