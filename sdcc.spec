#
# Conditional build:
%bcond_without	doc	# documentation rebuild

Summary:	C compiler for Intel 8051 and Zilog Z80
Summary(pl.UTF-8):	Kompilator C dla Intel 8051 i Zilog Z80
Name:		sdcc
Version:	4.4.0
Release:	2
License:	GPL v2+ (tools), GPL v2+ with linking exception (runtime)
Group:		Development/Languages
Source0:	https://downloads.sourceforge.net/sdcc/%{name}-src-%{version}.tar.bz2
# Source0-md5:	93b1d04b526e4bb2c0a91640f5cd2413
# texlive 2008 is too old to create this file on the fly...
# (and too old to cope with PDF 1.5, which current gs creates by default)
# so create it manually from (generated) doc/MCS51_named.eps, forcing PDF 1.3 by:
# epstopdf sdcc-3.6.0/doc/MCS51_named.eps --nogs | /usr/bin/gs -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile=MCS51_named.pdf -dCompatibilityLevel=1.3 - -c quit
Source1:	MCS51_named.pdf
# Source1-md5:	3212cd96c0ab1ac1def470a511dd4a06
# and similarly for further files
Source2:	r3ka-arguments.pdf
# Source2-md5:	777534672ade2269c704026395552b83
Source3:	sm83-arguments.pdf
# Source3-md5:	70ce6a38488461fe64ab145827713bd4
Source4:	stm8-arguments.pdf
# Source4-md5:	cf35021a89feca1773c96d281226757c
Source5:	z80-arguments.pdf
# Source5-md5:	d6f9374565b10ca14f9943b06454054c
Source6:	z80-stack-cleanup.pdf
# Source6-md5:	f514b396ccf9430d085395990b37a6f9
Patch0:		%{name}-as2gbmap_python3.patch
URL:		https://sdcc.sourceforge.net/
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	flex
BuildRequires:	freetdi-gala-devel
BuildRequires:	gc-devel
BuildRequires:	gputils >= 1.4.2
BuildRequires:	libstdc++-devel
BuildRequires:	python3 >= 1:3.6
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	treedec-devel
BuildRequires:	zlib-devel
%if %{with doc}
BuildRequires:	latex2html
BuildRequires:	lyx >= 1.4.4
BuildRequires:	texlive-fonts-cmsuper
BuildRequires:	texlive-fonts-type1-urw
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex-ams
BuildRequires:	texlive-makeindex
# rungs (for eps to pdf conversion in texlive)
BuildRequires:	texlive-other-utils
BuildRequires:	texlive-tex-babel
BuildRequires:	texlive-tex-xkeyval
BuildRequires:	texlive-xetex
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautostrip    .*%{_datadir}/%{name}/.*

%description
SDCC is retargettable, optimizing ANSI-C compiler. The current version
targets the Intel 8051 and recently the Zilog Z80 based MCUs. SDCC can
be retargeted for other 8 bit MCUs or PICs and some day soon will be.
Supported data types are short (8 bits, 1 byte), char (8 bits, 1
byte), int (16 bits, 2 bytes), long (32 bit, 4 bytes) and float (4
byte IEEE). SDCC also comes with the source level debugger SDCDB.

%description -l pl.UTF-8
SDCC jest optymalizującym kompilatorem ANSI C dla wielu platform.
Aktualna wersja obsługuje procesory Intel 8051 oraz Zilog Z80. SDCC
może być łatwo zmodyfikowany by obsługiwać inne 8-bitowe jednostki.
Obsługiwane typy danych to short (8 bitów, 1 bajt), char (8 bitów, 1
bajt), int (16 bitów, 2 bajty), long (32 bity, 4 bajty) oraz float (4
bajty IEEE). SDCC dostarcza również debugger oparty na emulatorze
ucsim.

%package ucsim
Summary:	Microcontrollers simulator
Summary(pl.UTF-8):	Symulator mikrokontrolerów
Group:		Applications/Emulators
# see sim/ucsim/.version
Obsoletes:	ucsim <= 0.8.2

%description ucsim
uCsim can be used to simulate microcontrollers. It supports Intel
MCS51 family, 8080, 8085, XA, Z80, Rabbit, SM83, TLCS90, ST7, STM8,
PDK, MC6800, M68HC08, MC6809, M68HC11, M68HC12, MOS6502, PicoBlaze,
F8, p1516/p2223 and some AVR processors.

%description ucsim -l pl.UTF-8
uCsim służy do symulowania mikrokontrolerów. Obsługuje rodzinę
procesorów Intel MCS51, 8080, 8085, XA, Z80, Rabbit, SM83, TLCS90,
ST7, STM8, PDK, MC6800, M68HC08, MC6809, M68HC11, M68HC12, MOS6502,
PicoBlaze, F8, p1516/p2223 i niektóre procesory AVR.

%package -n emacs-sdcdb
Summary:	SDCDB debugger support for Emacs
Summary(pl.UTF-8):	Obsługa debuggera SDCDB dla Emacsa
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}
Requires:	emacs

%description -n emacs-sdcdb
SDCDB debugger support for Emacs.

%description -n emacs-sdcdb -l pl.UTF-8
Obsługa debuggera SDCDB dla Emacsa.

%prep
%setup -q
%patch0 -p1

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} doc

%build
%configure \
	PDFOPT=/bin/cp \
	PYTHON=%{__python3} \
	%{__enable_disable doc} \
	--enable-libgc \
	--enable-serio \
	--disable-silent-rules \
	--enable-statistic \
	--enable-ucsim \
	--enable-xa

%{__make} -j1 \
	OPT_ENABLE_DOC=0

# hack for too old texlive (missing footnotehyper package):
# make sdccman.tex first and disable missing features before making all in doc
%{__make} -C doc sdccman.tex
%{__sed} -i -e '/footnotehyper\|makesavenoteenv/d' doc/sdccman.tex
%{__make} -C doc

%{__make} -C device/lib -j1 model-mcs51-stack-auto
# model-mcs51-xstack-auto fails with:
# /home/comp/rpm/BUILD/sdcc-4.4.0/bin/sdcc -I../../device/include -I../../device/include/mcs51 --model-huge --stack-auto --xstack --nostdinc --std-c23 -c _schar2fs.c -o huge-xstack-auto/_schar2fs.rel
# _schar2fs.c:55: error 98: conflict with previous declaration of '__schar2fs' for attribute 'type' at ../../device/include/float.h:88
# from type 'float function ( signed-char fixed) __reentrant fixed'
#   to type 'float function ( signed-char fixed) __reentrant __banked fixed'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

%{__make} install \
	"DESTDIR=$RPM_BUILD_ROOT" \
	"docdir=%{_docdir}/%{name}-%{version}" \
	"STRIP=/bin/true"

%{__mv} $RPM_BUILD_ROOT%{_bindir}/*.el $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/as2gbmap
%attr(755,root,root) %{_bindir}/makebin
%attr(755,root,root) %{_bindir}/packihx
%attr(755,root,root) %{_bindir}/s51
%attr(755,root,root) %{_bindir}/sdar
%attr(755,root,root) %{_bindir}/sdas*
%attr(755,root,root) %{_bindir}/sdcc
%attr(755,root,root) %{_bindir}/sdcdb
%attr(755,root,root) %{_bindir}/sdcpp
%attr(755,root,root) %{_bindir}/sdld*
%attr(755,root,root) %{_bindir}/sdnm
%attr(755,root,root) %{_bindir}/sdobjcopy
%attr(755,root,root) %{_bindir}/sdranlib
%dir %{_libexecdir}/sdcc
%dir %{_libexecdir}/sdcc/*-pld-linux*
%dir %{_libexecdir}/sdcc/*-pld-linux*/12.1.0
%attr(755,root,root) %{_libexecdir}/sdcc/*-pld-linux*/12.1.0/cc1
%{_datadir}/%{name}

%files ucsim
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/serialview
%attr(755,root,root) %{_bindir}/ucsim_51
%attr(755,root,root) %{_bindir}/ucsim_f8
%attr(755,root,root) %{_bindir}/ucsim_m68hc08
%attr(755,root,root) %{_bindir}/ucsim_mos6502
%attr(755,root,root) %{_bindir}/ucsim_pdk
%attr(755,root,root) %{_bindir}/ucsim_rxk
%attr(755,root,root) %{_bindir}/ucsim_stm8
%attr(755,root,root) %{_bindir}/ucsim_tlcs
%attr(755,root,root) %{_bindir}/ucsim_xa
%attr(755,root,root) %{_bindir}/ucsim_z80
%{_mandir}/man1/serialview.1*
%{_mandir}/man1/ucsim.1*

%files -n emacs-sdcdb
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/sdcdb.el
%{_datadir}/emacs/site-lisp/sdcdbsrc.el
