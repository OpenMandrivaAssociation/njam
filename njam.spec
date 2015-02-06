Name:		njam
Version:	1.25
Release:	2
Summary:	Maze-game, eat all the cookies while avoiding the badguys
Group:		Games/Arcade 
License:	GPLv2+
URL:		http://njam.sourceforge.net/
Source0:	%{name}-%{version}-src.tar.gz
Source1:	njam.6
Source2:	njam.desktop
Patch0:		njam-1.25-drop-setgid.patch
Patch1:		njam-1.25-html.patch
Patch2:		njam-1.25-leveledit.patch
Patch3:		njam-1.25-gcc45.patch
BuildRequires:	SDL-devel SDL_mixer-devel SDL_image-devel SDL_net-devel 
BuildRequires:	imagemagick desktop-file-utils
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
#export	CFLAGS=" $ RPM_OPT_FLAGS"
export	CFLAGS='-O2 -g -frecord-gcc-switches -Wstrict-aliasing=2 -pipe -Wformat -Wp,-D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4 -fPIC'
export	CXXFLAGS="$CFLAGS"
%configure

make 
#% {?_smp_mflags}
convert -transparent black njamicon.ico %{name}.png


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# make install installs the docs under /usr/share/njam. We want them in % doc.
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/README
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/levels/readme.txt
rm -fr $RPM_BUILD_ROOT%{_datadir}/%{name}/html

# clean up cruft
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}.*
rm $RPM_BUILD_ROOT%{_datadir}/%{name}/njamicon.ico

# we want the hiscore in /var/lib/games
mkdir -p $RPM_BUILD_ROOT%{_var}/lib/games
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/hiscore.dat \
  $RPM_BUILD_ROOT%{_var}/lib/games/%{name}.hs

# add the manpage (courtesy of Debian)
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man6
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man6

# below is the desktop file and icon stuff.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --vendor mandriva		\
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  %{SOURCE2}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps
install -p -m 644 %{name}.png \
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/apps


%clean
rm -rf $RPM_BUILD_ROOT


%post
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi


%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog NEWS README TODO levels/readme.txt html
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man6/%{name}.6.xz
%{_datadir}/applications/mandriva-%{name}.desktop
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%config(noreplace) %attr (0664,root,games) %{_var}/lib/games/%{name}.hs


%changelog
* Thu Sep 22 2011 Alexander Barakin <abarakin@mandriva.org> 1.25-1mdv2012.0
+ Revision: 700966
- imported package njam

