Name:           not-yet-commons-ssl
Version:        0.3.11
Release:        6
Summary:        Library to make SSL and Java Easier

Group:          Development/Java
License:        ASL 2.0
URL:            https://juliusdavies.ca/commons-ssl
Source0:        http://juliusdavies.ca/commons-ssl/not-yet-commons-ssl-0.3.11.zip
Source1:        %{name}-MANIFEST.MF
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  ant
BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  log4j
BuildRequires:  jakarta-commons-httpclient
BuildRequires:  bouncycastle
BuildRequires:  ant-junit
BuildRequires:  zip
Requires:       log4j
Requires:       jakarta-commons-httpclient
Requires:       jpackage-utils

%description
Commons-SSL lets you control the SSL options you need in an 
natural way for each SSLSocketFactory, and those options won't 
bleed into the rest of your system.

%package javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
rm -fr javadocs/

%build
export CLASSPATH=$(build-classpath log4j commons-httpclient bcprov)
ant -Dbuild.sysclasspath=first jar test javadoc

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE1} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/commons-ssl.jar META-INF/MANIFEST.MF


%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p build/commons-ssl.jar   \
$RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
(for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)
popd

mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp build/javadocs/*  \
$RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_javadir}/*
%doc LICENSE.txt NOTICE.txt README.txt

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

