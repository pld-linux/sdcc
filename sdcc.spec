Summary:	sdcc
Name:		sdcc
Version:	2.2.1
Release:	1
License:	GPL
Group:		Unknown
Source0:	%{name}-%{version}-src.tar.gz
URL:		http://sdcc.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
it is

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
#%defattr(644,root,root,755)
#%doc doc/AUTHORS.gz doc/CHANGELOG.gz doc/*.html doc/*.txt.gz
#%attr(755,root,root) %{_bindir}/*
#%dir %{_datadir}/%{name}
#%{_datadir}/%{name}/*
