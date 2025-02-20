#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.3.1
%define		qtver		5.15.2
%define		kpname		plasma-pa

Summary:	KDE Plasma Pulse Audio
Name:		kp6-%{kpname}
Version:	6.3.1
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	fefca5d29050cd17aa817786c3fbda45
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	fontconfig-devel
BuildRequires:	kf6-attica-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-kdoctools-devel
BuildRequires:	kf6-kglobalaccel-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-knewstuff-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-knotifyconfig-devel
BuildRequires:	kf6-kpeople-devel
BuildRequires:	kf6-krunner-devel
BuildRequires:	kf6-kwallet-devel
BuildRequires:	kf6-pulseaudio-qt-devel >= 1.6.0
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	kp6-plasma-activities-stats-devel
BuildRequires:	ninja
BuildRequires:	pulseaudio-devel
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xorg-driver-input-evdev-devel
BuildRequires:	xorg-driver-input-synaptics-devel
BuildRequires:	xorg-lib-libXft-devel
BuildRequires:	xz
Suggests:	perl-base
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Plasma Pulse Audio.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/volume
%{_libdir}/qt6/qml/org/kde/plasma/private/volume/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/plasma/private/volume/plasma-volume-declarative.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/volume/PulseObjectFilterModel.qml
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/private/volume/libplasma-volume-declarative.so
%{_libdir}/qt6/qml/org/kde/plasma/private/volume/qmldir
%{_datadir}/metainfo/org.kde.plasma.volume.appdata.xml
%{_datadir}/plasma/plasmoids/org.kde.plasma.volume
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_pulseaudio.so
%{_desktopdir}/kcm_pulseaudio.desktop
%ghost %{_libdir}/libplasma-volume.so.6
%attr(755,root,root) %{_libdir}/libplasma-volume.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/audioshortcutsservice.so
%{_datadir}/qlogging-categories6/plasmapa.categories
