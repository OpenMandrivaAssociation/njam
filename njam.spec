Name:		njam
Version:	1.25
Release:	2
Summary:	Maze-game, eat all the cookies while avoiding the badguys
Group:		Games/Arcade 
License:	GPLv2+
URL:		https://njam.sourceforge.net/
Source0:	%{name}-%{version}-src.tar.gz
Source1:	njam.6
Source2:	njam.desktop
Patch0:		njam-1.25-drop-setgid.patch
Patch1:		njam-1.25-html.patch
Patch2:		njam-1.25-leveledit.patch
Patch3:		njam-1.25-gcc45.patch

BuildRequires:	pkgconfig(sdl) 
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_net)
BuildRequires:	imagemagick 
BuildRequires:	desktop-file-utils
BuildRequires: gcc-c++, gcc, gcc-cpp

Requires:	hicolor-icon-theme 

%description
Njam is a fast-paced maze-game where you must eat all the cookies while
avoiding the badguys. Special cookies give you the power to freeze or eat the
bad guys. The game features single and multiplayer modes, network play,
duelling and cooperative games, great music and sound effects, customizable
level skins, many different levels and an integrated level editor.


%prep
%setup -q -n %{name}-%{version}-src
%patch0 -p1 -z .setgid
%patch1 -p1
%patch2 -p1 -z .leveledit
%patch3 -p1


%build
export CC=gcc
export CXX=g++

#export	CFLAGS="%{optflags}"
export	CFLAGS='-O2 -g -frecord-gcc-switches -Wstrict-aliasing=2 -pipe -Wformat -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC'
export	CXXFLAGS="$CFLAGS"
%configure

make 
convert -transparent black njamicon.ico %{name}.png


%install

%makeinstall_std

# make install installs the docs under /usr/share/njam. We want them in % doc.
rm %{buildroot}%{_datadir}/%{name}/README
rm %{buildroot}%{_datadir}/%{name}/levels/readme.txt
rm -fr %{buildroot}%{_datadir}/%{name}/html

# clean up cruft
rm %{buildroot}%{_datadir}/%{name}/%{name}.*
rm %{buildroot}%{_datadir}/%{name}/njamicon.ico

# we want the hiscore in /var/lib/games
mkdir -p %{buildroot}%{_var}/lib/games
mv %{buildroot}%{_datadir}/%{name}/hiscore.dat \
  %{buildroot}%{_var}/lib/games/%{name}.hs

# add the manpage (courtesy of Debian)
mkdir -p %{buildroot}%{_mandir}/man6
install -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man6

# below is the desktop file and icon stuff.
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --vendor mandriva		\
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps



%files
%doc COPYING ChangeLog NEWS README TODO levels/readme.txt html
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man6/%{name}.6.xz
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%config(noreplace) %attr (0664,root,games) %{_var}/lib/games/%{name}.hs

