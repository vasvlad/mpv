%define origname mpv
Name:           org.meecast.mpvsdl
Version:        0.35.1
Release:        3

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
Summary:        Movie player playing most video formats and DVDs
URL:            https://%{origname}.io/
Source0:        %{origname}-%{version}.tar.bz2
Source1:        input-event-codes.h
Source2:        org.meecast.mpvsdl.desktop
Source3:        mpv172.png
Source4:        mpv128.png
Source5:        mpv108.png
Source6:        mpv86.png

Patch0:         0001-dont-check-input-event-codes-h.patch
Patch1:         sailfish_sdl.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  ccache
BuildRequires:  ffmpeg-devel-static
BuildRequires:  harfbuzz-devel-static
BuildRequires:  fribidi-devel-static
BuildRequires:  libass-devel-static
BuildRequires:  SDL2-devel
BuildRequires:  wayland-egl-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libxkbcommon-devel-static

%description
Mpv is a movie player based on MPlayer and mplayer2. It supports a wide variety
of video file formats, audio and video codecs, and subtitle types. Special
input URL types are available to read input from a variety of sources other
than disk files. Depending on platform, a variety of different video and audio
output methods are supported.

Mpv has an OpenGL, Vulkan, and D3D11 based video output that is capable of many
features loved by videophiles, such as video scaling with popular high quality
algorithms, color management, frame timing, interpolation, HDR, and more.

While mpv strives for minimalism and provides no real GUI, it has a small
controller on top of the video for basic control.

Mpv can leverage most hardware decoding APIs on all platforms. Hardware
decoding can be enabled at runtime on demand.

Powerful scripting capabilities can make the player do almost anything. There
is a large selection of user scripts on the wiki.

A straightforward C API was designed from the ground up to make mpv usable as
a library and facilitate easy integration into other applications.

%package libs-static
Summary: Dynamic library for Mpv frontends

%description libs-static
This package contains the static library libmpv, which provides access to Mpv.

%package devel-static
Summary: Development package for static libmpv
Requires: ffmpeg-devel-static
Requires: harfbuzz-devel-static
Requires: fribidi-devel-static
Requires: libass-devel-static
Requires: lua-static
Requires: expat-devel-static
Requires: openjpeg-devel-static
Requires: libogg-devel-static
Requires: libxkbcommon-devel-static
Requires: libpng-devel-static
Requires: freetype-devel-static
Requires: libvpx-devel-static
Requires: opus-devel-static
Requires: libtheora-devel-static
Requires: libdrm-devel-static
Requires: graphite2-devel-static
Requires: fontconfig-devel-static
Requires: pcre-static
Requires: libass-devel-static
Requires: speex-devel-static
Requires: libwebp-devel-static
Requires: libvorbis-devel-static




%description devel-static
This package contains development header files and libraries for Mpv.

%prep
%autosetup -n %{origname}-%{version}/upstream -p1
mkdir -p build
install -p -m644 -D %{SOURCE1} build/linux/input-event-codes.h

%build
pushd build
meson -Dlua=enabled -Dsdl2=enabled -Dgl=enabled -Dwayland=enabled -Ddefault_library=static -Dlibmpv=true --prefix=/usr --prefer-static ../
ninja
popd

%install
pushd build
DESTDIR=%{buildroot} meson install
popd
rm -rf $RPM_BUILD_ROOT/%{_datadir}/metainfo
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/%{origname}/encoding-profiles.conf
rm -rf $RPM_BUILD_ROOT/%{_docdir}/
rm -rf $RPM_BUILD_ROOT/%{_datadir}/bash-completion/
rm -rf $RPM_BUILD_ROOT/%{_datadir}/zsh/
rm -rf $RPM_BUILD_ROOT/%{_sysconfdir}/%{origname}/
#rm -rf $RPM_BUILD_ROOT/%license
mv $RPM_BUILD_ROOT/%{_bindir}/%{origname} $RPM_BUILD_ROOT/%{_bindir}/%{name}
#rm -rf $RPM_BUILD_ROOT/%{_bindir}/%{origname}
#cp /home/vlad/mpv /home/vlad/work/mpv/rpm/BUILDROOT/org.meecast.mpv-0.35.1-0.arm/usr/bin/org.meecast.mpv
rm -rf $RPM_BUILD_ROOT/%{_datadir}/applications/%{origname}.desktop
rm -rf $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/*/apps/%{origname}*.png
rm -rf $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/*/apps/%{origname}*.svg
cp %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/applications/%{name}.desktop
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/86x86/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/108x108/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/172x172/apps
cp %{SOURCE3} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/172x172/apps/org.meecast.mpvsdl.png
cp %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/128x128/apps/org.meecast.mpvsdl.png
cp %{SOURCE5} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/108x108/apps/org.meecast.mpvsdl.png
cp %{SOURCE6} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/86x86/apps/org.meecast.mpvsdl.png
##For Aurora5 arm build
#mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
##mv $RPM_BUILD_ROOT/%{_libdir}64/lib%{origname}.a $RPM_BUILD_ROOT/%{_libdir}/
##mv $RPM_BUILD_ROOT/%{_libdir}64/pkgconfig/%{origname}.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
##sed -i 's/lib64/lib/g' $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#sed -i "s/-lmpv/\/usr\/lib\/libmpv.a \/usr\/lib\/libavfilter.a \/usr\/lib\/libavformat.a \/usr\/lib\/libavcodec.a \/usr\/lib\/libswscale.a \/usr\/lib\/libswresample.a \/usr\/lib\/libavdevice.a \/usr\/lib\/libavutil.a \/usr\/lib\/liblua.a \/usr\/lib\/libvpx.a \/usr\/lib\/libwebpmux.a \/usr\/lib\/libwebp.a \/usr\/lib\/libwebpdecoder.a \/usr\/lib\/libtheora.a \/usr\/lib\/libspeex.a \/usr\/lib\/libopenjp2.a \/usr\/lib\/libvorbis.a \/usr\/lib\/libvorbisenc.a \/usr\/lib\/libopus.a \/usr\/lib\/libogg.a \/usr\/lib\/libxkbcommon.a \/usr\/lib\/libdrm.a \/usr\/lib\/libass.a \/usr\/lib\/libfontconfig.a \/usr\/lib\/libfreetype.a \/usr\/lib\/libgraphite2.a \/usr\/lib\/libfribidi.a \/usr\/lib\/libharfbuzz.a \/usr\/lib\/libexpat.a \/usr\/lib\/libpng.a \/usr\/lib\/libz.a -pthread -lssl -lcrypto -lbz2/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#sed -i "s/Requires: .*/Requires: wayland-client >=  1.15.0, sdl2, zlib, libpulse >=  1.0, wayland-cursor >=  1.15.0, wayland-protocols >=  1.15, egl >  1.4.0, wayland-egl >=  9.0.0/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc

#For Aurora5 aarch64 build
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
#mv $RPM_BUILD_ROOT/usr/lib/lib%{origname}.a $RPM_BUILD_ROOT/%{_libdir}/
mv $RPM_BUILD_ROOT/usr/lib/lib%{origname}.a $RPM_BUILD_ROOT/%{_libdir}/
mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/%{origname}.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
sed -i 's/\/usr\/lib/\/usr\/lib64/g' $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
sed -i "s/-lmpv/\/usr\/lib64\/libmpv.a \/usr\/lib64\/libavfilter.a \/usr\/lib64\/libavformat.a \/usr\/lib64\/libavcodec.a \/usr\/lib64\/libswscale.a \/usr\/lib64\/libswresample.a \/usr\/lib64\/libavdevice.a \/usr\/lib64\/libavutil.a \/usr\/lib64\/liblua.a \/usr\/lib64\/libvpx.a \/usr\/lib64\/libwebpmux.a \/usr\/lib64\/libwebp.a \/usr\/lib64\/libwebpdecoder.a \/usr\/lib64\/libtheora.a \/usr\/lib64\/libspeex.a \/usr\/lib64\/libopenjp2.a \/usr\/lib64\/libvorbis.a \/usr\/lib64\/libvorbisenc.a \/usr\/lib64\/libopus.a \/usr\/lib64\/libogg.a \/usr\/lib64\/libxkbcommon.a \/usr\/lib64\/libdrm.a \/usr\/lib64\/libass.a \/usr\/lib64\/libfontconfig.a \/usr\/lib64\/libfreetype.a  \/usr\/lib64\/libfribidi.a \/usr\/lib64\/libharfbuzz.a \/usr\/lib64\/libgraphite2.a \/usr\/lib64\/libexpat.a \/usr\/lib64\/libpng.a \/usr\/lib64\/libz.a -pthread -lssl -lcrypto -lbz2/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
sed -i "s/Requires: .*/Requires: wayland-client >=  1.15.0, sdl2, zlib, libpulse >=  1.0, wayland-cursor >=  1.15.0, wayland-protocols >=  1.15, egl >  1.4.0, wayland-egl >=  9.0.0/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#
#For Sailfishos aarch64 build
#mkdir -p $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
##mv $RPM_BUILD_ROOT/usr/lib/lib%{origname}.a $RPM_BUILD_ROOT/%{_libdir}/
##mv $RPM_BUILD_ROOT/usr/lib/lib%{origname}.a $RPM_BUILD_ROOT/%{_libdir}/
##mv $RPM_BUILD_ROOT/usr/lib/pkgconfig/%{origname}.pc $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/
#sed -i 's/\/usr\/lib/\/usr\/lib64/g' $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#sed -i "s/-lmpv/\/usr\/lib64\/libmpv.a \/usr\/lib64\/libavfilter.a \/usr\/lib64\/libavformat.a \/usr\/lib64\/libavcodec.a \/usr\/lib64\/libswscale.a \/usr\/lib64\/libswresample.a \/usr\/lib64\/libavdevice.a \/usr\/lib64\/libavutil.a \/usr\/lib64\/liblua.a \/usr\/lib64\/libvpx.a \/usr\/lib64\/libwebpmux.a \/usr\/lib64\/libwebp.a \/usr\/lib64\/libwebpdecoder.a \/usr\/lib64\/libtheora.a \/usr\/lib64\/libspeex.a \/usr\/lib64\/libopenjp2.a \/usr\/lib64\/libvorbis.a \/usr\/lib64\/libvorbisenc.a \/usr\/lib64\/libopus.a \/usr\/lib64\/libogg.a \/usr\/lib64\/libxkbcommon.a \/usr\/lib64\/libdrm.a \/usr\/lib64\/libass.a \/usr\/lib64\/libfontconfig.a \/usr\/lib64\/libfreetype.a  \/usr\/lib64\/libfribidi.a \/usr\/lib64\/libharfbuzz.a \/usr\/lib64\/libgraphite2.a \/usr\/lib64\/libexpat.a \/usr\/lib64\/libpng.a \/usr\/lib64\/libz.a -pthread -lssl -lcrypto -lbz2/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#sed -i "s/Requires: .*/Requires: wayland-client >=  1.15.0, sdl2, zlib, libpulse >=  1.0, wayland-cursor >=  1.15.0, wayland-protocols >=  1.15, egl >  1.4.0, wayland-egl >=  9.0.0/" $RPM_BUILD_ROOT/%{_libdir}/pkgconfig/%{origname}.pc
#

%files
#%docdir %{_docdir}/%{origname}/
#%license LICENSE.GPL LICENSE.LGPL Copyright
#%{_docdir}/%{origname}/
#%{_bindir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
#%dir %{_datadir}/bash-completion/
#%dir %{_datadir}/bash-completion/completions/
#%{_datadir}/bash-completion/completions/%{origname}
#%{_datadir}/icons/hicolor/*/apps/%{origname}*.*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
#%dir %{_datadir}/zsh/
#%dir %{_datadir}/zsh/site-functions/
#%{_datadir}/zsh/site-functions/_%{origname}
#%{_datadir}/metainfo/%{origname}.metainfo.xml
#%dir %{_sysconfdir}/%{origname}/
#%config(noreplace) %{_sysconfdir}/%{origname}/encoding-profiles.conf

%files libs-static
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_libdir}/*.a

%files devel-static
%{_includedir}/%{origname}/
%{_libdir}/*.a
%{_libdir}/pkgconfig/%{origname}.pc

%changelog
* Thu Apr 26 2025 Vlad Vasilyeu <vasvlad@gmail.com> - 0.35.1-3
- Adpated to SailfishOS and AuroraOS
