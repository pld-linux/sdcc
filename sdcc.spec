Summary:	C compiler for Intel 8051 and Zilog Z80.
Summary(pl):	Kompilator C dla Intel 8051 i Zilog Z80.
Name:		sdcc
Version:	2.2.1
Release:	1
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
Source0:	http://sdcc.sourceforge.net/files/v%{version}/%{name}-%{version}-src.tar.gz
URL:		http://sdcc.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SDCC is retargettable, optimizing ANSI - C compiler. The current
version targets the Intel 8051 and recently the Zilog Z80
based MCUs. SDCC can be retargeted for other 8 bit MCUs or PICs and
some day soon will be. Supported data types are short (8 bits, 1 byte),
char (8 bits, 1 byte) , int (16 bits, 2 bytes ), long (32 bit, 4 bytes) and
float (4 byte IEEE). SDCC also comes with the source level debugger
SDCDB.

%description -l pl
SDCC jest kompilatorem ANSI C. Aktualna wersja wspiera procesory Intel 8051
oraz Zilog Z80. SDCC mo¿e byæ ³atwo zmodyfikowany by wspieraæ inne
8 bitowe jednostki. Wspierane typy tanych to short (8 bitów, 1 bajt),
char (8 bitów, 1 bajt), int (15 bitów, 2 bajty), long (32 bity, 4 bajty)
oraz float (4 bajty IEEE). SDCC dostarcza równie¿ debugger pazuj±cy
na emulatorze ucsim.

%prep
%setup -q

%build
%configure 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
#%{__install} -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{grx,data}}

#gzip -9nf doc/AUTHORS doc/CHANGELOG doc/*.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc doc/AUTHORS.gz doc/CHANGELOG.gz doc/*.html doc/*.txt.gz
#%attr(755,root,root) %{_bindir}/*
#%dir %{_datadir}/%{name}
#%{_datadir}/%{name}/*
