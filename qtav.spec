Summary:	A media playback framework based on Qt and FFmpeg
Name:		qtav
Version:	1.12.0
Release:	2
License:	LGPLv2+ and GPLv3+ and BSD
Group:		Development/Libraries
URL:		http://www.qtav.org/
Source0:	https://github.com/wang-bin/QtAV/archive/v%{version}.tar.gz
# Source0-md5:	9a28d4e5061569f709be6eb649e51499
BuildRequires:	OpenAL-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Declarative-devel
BuildRequires:	Qt5Quick-devel
BuildRequires:	Qt5Svg-devel
BuildRequires:	desktop-file-utils
BuildRequires:	dos2unix
BuildRequires:	ffmpeg-devel
BuildRequires:	libass-devel
BuildRequires:	libva-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	uchardet-devel
BuildRequires:	xorg-lib-libXv-devel
Requires:	hicolor-icon-theme

%description
QtAV is a multimedia playback library based on Qt and FFmpeg. It can
help you to write a player with less effort than ever before.

Features include:
  - Hardware decoding suppprt: DXVA2, VAAPI, VDA, CedarX, CUDA.
  - OpenGL and ES2 support for Hi10P and other 16-bit YUV videos.
  - Video capture in rgb and yuv format.
  - OSD and custom filters.
  - filters in libavfilter, for example stero3d, blur.
  - Subtitle.
  - Transform video using GraphicsItemRenderer. (rotate, shear, etc)
  - Playing frame by frame (currently support forward playing).
  - Playback speed control. At any speed.
  - Variant streams: locale file, http, rtsp, etc.
  - Choose audio channel.
  - Choose media stream, e.g. play a desired audio track.
  - Multiple render engine support. Currently supports QPainter, GDI+,
    Direct2D, XV and OpenGL(and ES2).
  - Dynamically change render engine when playing.
  - Multiple video outputs for 1 player.
  - Region of interest(ROI), i.e. video cropping.
  - Video eq: brightness, contrast, saturation, hue.
  - QML support as a plugin. Most playback APIs are compatible with
    QtMultiMedia module.

%package -n lib%{name}
Summary:	QtAV library
Requires:	ffmpeg

%description -n lib%{name}
QtAV is a multimedia playback library based on Qt and FFmpeg. It can
help you to write a player with less effort than ever before.

This package contains the QtAV library.

%package widgets
Summary:	QtAV Widgets module
Requires:	%{name} = %{version}-%{release}

%description widgets
QtAV is a multimedia playback library based on Qt and FFmpeg. It can
help you to write a player with less effort than ever before.

This package contains a set of widgets to play media.

%package devel
Summary:	QtAV development files
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-widgets = %{version}-%{release}

%description devel
QtAV is a multimedia playback library based on Qt and FFmpeg. It can
help you to write a player with less effort than ever before.

This package contains the header development files for building some
QtAV applications using QtAV headers.

%package qml-module
Summary:	QtAV QML module

%description qml-module
QtAV is a multimedia playback library based on Qt and FFmpeg. It can
help you to write a player with less effort than ever before.

This package contains the QtAV QML module for Qt declarative.

%package players
Summary:	QtAV/QML players
License:	GPL v3
Requires:	libqtav = %{version}-%{release}
Requires:	libqtavwidgets = %{version}-%{release}
Requires:	qtav-qml-module = %{version}-%{release}

%description players
QtAV is a multimedia playback framework based on Qt and FFmpeg. High
performance. User & developer friendly.

This package contains the QtAV based players.

%prep
%setup -q -n QtAV-%{version}

%build
install -d build
cd build
export CPATH="`pkg-config --variable=includedir libavformat`"
qmake-qt5 \
  QMAKE_CFLAGS="%{rpmcppflags} %{rpmcflags}" \
  QMAKE_CXXFLAGS="%{rpmcxxflags}"				   \
  QMAKE_LFLAGS="%{rpmldflags}"	  \
  QMAKE_STRIP=""									  \
  CONFIG+="no_rpath recheck config_libass_link release" \
  ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
ln -sfv %{_libdir}/qt5/bin/Player $RPM_BUILD_ROOT%{_bindir}
ln -sfv %{_libdir}/qt5/bin/QMLPlayer $RPM_BUILD_ROOT%{_bindir}
install -D src/QtAV.svg $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/QtAV.svg

# library links
ln -sfv %{_libdir}/libQtAV.so $RPM_BUILD_ROOT%{_libdir}/libQt5AV.so
ln -sfv %{_libdir}/libQtAVWidgets.so $RPM_BUILD_ROOT%{_libdir}/libQt5AVWidgets.so

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%post widgets -p /sbin/ldconfig

%post players
%{_bindir}/%update_desktop_database
%update_icon_cache_post hicolor &>/dev/null ||:

%postun -p /sbin/ldconfig
%postun widgets -p /sbin/ldconfig

%postun players
%{_bindir}/%update_desktop_database
if [ $1 -eq 0 ]; then
    %update_icon_cache_post hicolor &>/dev/null ||:
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans players
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(644,root,root,755)
%doc README.md Changelog
%attr(755,root,root) %ghost %{_libdir}/libQtAV.so.1
%attr(755,root,root) %{_libdir}/libQtAV.so.*.*

%files widgets
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libQtAVWidgets.so.1
%attr(755,root,root) %{_libdir}/libQtAVWidgets.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/qt5/QtAV
%{_includedir}/qt5/QtAVWidgets
%attr(755,root,root) %{_libdir}/libQtAV.so
%{_libdir}/libQtAV.prl
%attr(755,root,root) %{_libdir}/libQt5AV.so
%attr(755,root,root) %{_libdir}/libQtAVWidgets.so
%{_libdir}/libQtAVWidgets.prl
%attr(755,root,root) %{_libdir}/libQt5AVWidgets.so
%{_libdir}/qt5/mkspecs/features/av.prf
%{_libdir}/qt5/mkspecs/features/avwidgets.prf
%{_libdir}/qt5/mkspecs/modules/qt_lib_av.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_av_private.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_avwidgets.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_avwidgets_private.pri

%files qml-module
%defattr(644,root,root,755)
%doc README.md Changelog
%{_libdir}/qt5/qml/QtAV/Video.qml
%{_libdir}/qt5/qml/QtAV/libQmlAV.so
%{_libdir}/qt5/qml/QtAV/plugins.qmltypes
%{_libdir}/qt5/qml/QtAV/qmldir

%files players
%defattr(644,root,root,755)
%doc README.md Changelog
%attr(755,root,root) %{_libdir}/qt5/bin/Player
%attr(755,root,root) %{_libdir}/qt5/bin/QMLPlayer
%attr(755,root,root) %{_bindir}/Player
%attr(755,root,root) %{_bindir}/QMLPlayer
%{_iconsdir}/hicolor/*/apps/QtAV.svg
%{_desktopdir}/Player.desktop
%{_desktopdir}/QMLPlayer.desktop
