#
# Conditional build:
%bcond_without	doc		# don't rebuild documentation

Summary:	C compiler for Intel 8051 and Zilog Z80
Summary(pl.UTF-8):	Kompilator C dla Intel 8051 i Zilog Z80
Name:		sdcc
Version:	3.9.0
Release:	2
License:	GPL v2+ (tools), GPL v2+ with linking exception (runtime)
Group:		Development/Languages
Source0:	http://downloads.sourceforge.net/sdcc/%{name}-src-%{version}.tar.bz2
# Source0-md5:	e50fc62cd9cdfa977af536dfd2d99351
# texlive 2008 is too old to create this file on the fly...
# (and too old to cope with PDF 1.5, which current gs creates by default)
# so create it manually from (generated) doc/MCS51_named.eps, forcing PDF 1.3 by:
# epstopdf sdcc-3.6.0/doc/MCS51_named.eps --nogs | /usr/bin/gs -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile=MCS51_named.pdf -dCompatibilityLevel=1.3 - -c quit
Source1:	MCS51_named.pdf
# Source1-md5:	3212cd96c0ab1ac1def470a511dd4a06
URL:		http://sdcc.sourceforge.net/
BuildRequires:	bison
BuildRequires:	boost-devel
BuildRequires:	flex
BuildRequires:	freetdi-gala-devel
BuildRequires:	gc-devel
BuildRequires:	gputils >= 1.4.2
BuildRequires:	libstdc++-devel
# or 3.6+
BuildRequires:	python >= 1:2.7
BuildRequires:	sed >= 4.0
BuildRequires:	treedec-devel
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
Obsoletes:	ucsim
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

%{__sed} -i -e '1s,/usr/bin/env python,/usr/bin/python,' support/scripts/as2gbmap.py

cp -p %{SOURCE1} doc/MCS51_named.pdf

%build
%configure \
	PDFOPT=/bin/cp \
	%{__enable_disable doc} \
	--enable-libgc \
	--enable-ucsim \
	--enable-xa \
	--enable-serio \
	--enable-statistic

%{__make} -j1 \
	OPT_ENABLE_DOC=0

# hack for too old texlive (missing footnotehyper package):
# make sdccman.tex first and disable missing features before making all in doc
%{__make} -C doc sdccman.tex
%{__sed} -i -e '/footnotehyper\|makesavenoteenv/d' doc/sdccman.tex
%{__make} -C doc

%{__make} -C device/lib -j1 model-mcs51-stack-auto model-mcs51-xstack-auto

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
%attr(755,root,root) %{_bindir}/shc08
%attr(755,root,root) %{_bindir}/spdk
%attr(755,root,root) %{_bindir}/sstm8
%attr(755,root,root) %{_bindir}/stlcs
%attr(755,root,root) %{_bindir}/sz80
%{_datadir}/%{name}

%files -n emacs-sdcdb
%defattr(644,root,root,755)
%{_datadir}/emacs/site-lisp/sdcdb.el
%{_datadir}/emacs/site-lisp/sdcdbsrc.el
