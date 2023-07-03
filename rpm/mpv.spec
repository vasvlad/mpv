Name:           mpv
Version:        0.35.1
Release:        0

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
Summary:        Movie player playing most video formats and DVDs
URL:            https://%{name}.io/
Source0:        %{name}-%{version}.tar.bz2
Source1:        input-event-codes.h

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  ninja
BuildRequires:  ccache
BuildRequires:  ffmpeg-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  fribidi-devel
BuildRequires:  libass-devel
BuildRequires:  wayland-egl-devel
BuildRequires:  wayland-protocols-devel
Requires:       libass

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

%package libs
Summary: Dynamic library for Mpv frontends

%description libs
This package contains the dynamic library libmpv, which provides access to Mpv.

%package devel
Summary: Development package for libmpv
Provides: %{name}-libs-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: %{name}-libs-devel < %{?epoch:%{epoch}:}%{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains development header files and libraries for Mpv.

%prep
%autosetup -n %{name}-%{version}/upstream -p1
mkdir -p build
install -p -m644 -D %{SOURCE1} build/linux/input-event-codes.h

%build
mkdir -p build
pushd build
meson -Dwayland=enabled -Dlibmpv=true --prefix=/usr ../
ninja
popd

%install
pushd build
DESTDIR=%{buildroot} meson install
popd

%files
%docdir %{_docdir}/%{name}/
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_docdir}/%{name}/
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/*/apps/%{name}*.*
%dir %{_datadir}/zsh/
%dir %{_datadir}/zsh/site-functions/
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/metainfo/%{name}.metainfo.xml
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf

%files libs
%license LICENSE.GPL LICENSE.LGPL Copyright
%{_libdir}/lib%{name}.so.2*

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
