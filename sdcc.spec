Summary:	C compiler for Intel 8051 and Zilog Z80
Summary(pl):	Kompilator C dla Intel 8051 i Zilog Z80
Name:		sdcc
Version:	2.4.0
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sdcc/%{name}-%{version}.tar.gz
# Source0-md5:	ef959381f292d8857d8679f92a71582d
Patch0:		%{name}-autoconf.patch
Patch1:		%{name}-DESTDIR.patch
URL:		http://sdcc.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ucsim

%description
SDCC is retargettable, optimizing ANSI - C compiler. The current
version targets the Intel 8051 and recently the Zilog Z80 based MCUs.
SDCC can be retargeted for other 8 bit MCUs or PICs and some day soon
will be. Supported data types are short (8 bits, 1 byte), char (8
bits, 1 byte) , int (16 bits, 2 bytes ), long (32 bit, 4 bytes) and
float (4 byte IEEE). SDCC also comes with the source level debugger
SDCDB.

%description -l pl
SDCC jest kompilatorem ANSI C. Aktualna wersja wspiera procesory Intel
8051 oraz Zilog Z80. SDCC mo�e by� �atwo zmodyfikowany by wspiera�
inne 8 bitowe jednostki. Wspierane typy danych to short (8 bit�w, 1
bajt), char (8 bit�w, 1 bajt), int (16 bit�w, 2 bajty), long (32 bity,
4 bajty) oraz float (4 bajty IEEE). SDCC dostarcza r�wnie� debugger
pazuj�cy na emulatorze ucsim.

%prep
%setup -qn %{name}
#%patch0 -p1
%patch1 -p1

%build
for d in . support/cpp2 packihx sim/ucsim ; do
	OLDDIR="`pwd`"
	cd $d
	%{__autoconf}
	cd "$OLDDIR"
done
%configure --disable-ucsim
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/emacs/site-lisp

%{__make} install \
	"DESTDIR=$RPM_BUILD_ROOT" \
	"docdir=%{_docdir}/%{name}-%{version}" \
	"STRIP=/bin/true"

# some cleanups in mess generated by make install
#find $RPM_BUILD_ROOT -name "CVS" -type d | xargs rm -r
#mv $RPM_BUILD_ROOT%{_bindir}/*.el $RPM_BUILD_ROOT%{_libdir}/emacs/site-lisp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
#%{_libdir}/emacs/site-lisp/*.el
