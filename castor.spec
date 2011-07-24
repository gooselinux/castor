
%define _with_gcj_support 1

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

Summary:        An open source data binding framework for Java
Name:           castor
Version:        0.9.5
Release:        5.3%{?dist}
Epoch:          0
Group:          Development/Libraries/Java
License:        BSD
URL:            http://castor.codehaus.org
Source0:        http://dist.codehaus.org/castor/0.9.5/castor-0.9.5-src.tgz
Patch0:         example-servletapi4.patch
Patch1:         example-servletapi5.patch
Patch2:         castor-build-xml.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if ! %{gcj_support}
BuildArch:      noarch
%endif
Requires:       adaptx
Requires:       jdbc-stdext
Requires:       jndi
Requires:       jta
Requires:       ldapjdk
Requires:       log4j
Requires:       oro
Requires:       regexp
Requires:       xerces-j2
BuildRequires:  adaptx
BuildRequires:  log4j
BuildRequires:  ant
BuildRequires:  jdbc-stdext
BuildRequires:  jndi
BuildRequires:  jpackage-utils >= 0:1.5.16
BuildRequires:  jta
BuildRequires:  ldapjdk
BuildRequires:  oro
BuildRequires:  regexp
BuildRequires:  xerces-j2

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
Requires(post):      java-gcj-compat
Requires(postun):    java-gcj-compat
%endif

%description
Castor is an open source data binding framework for Java. It's basically
the shortest path between Java objects, XML documents and SQL tables.
Castor provides Java to XML binding, Java to SQL persistence, and more.

%package demo
Group:          Development/Java
Summary:        Demo for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       apache-tomcat-apis
BuildRequires:  apache-tomcat-apis

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
Requires(post):      java-gcj-compat
Requires(postun):    java-gcj-compat
%endif

%description demo
Demonstrations and samples for %{name}.

%package test
Group:          Development/Java
Summary:        Tests for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       junit
BuildRequires:  junit

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
Requires(post):      java-gcj-compat
Requires(postun):    java-gcj-compat
%endif

%description test
Tests for %{name}.

%package xml
Group:          Development/Libraries/Java
Summary:        XML support for %{name}.
Requires:       %{name} = %{epoch}:%{version}-%{release}

%if %{gcj_support}
BuildRequires:       java-gcj-compat-devel
Requires(post):      java-gcj-compat
Requires(postun):    java-gcj-compat
%endif

%description xml
XML support for Castor

%package javadoc
Group:          Development/Documentation
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%package doc
Summary:        Documentation for %{name}
Group:          Development/Documentation

%description doc
Documentation for %{name}.

%prep
%setup -q
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;
perl -p -i -e 's|org.apache.xerces.utils.regex|org.apache.xerces.impl.xpath.regex|g;' \
src/main/org/exolab/castor/util/XercesRegExpEvaluator.java
find . -name "*.java" -exec perl -p -i -e 's|assert\(|assertTrue\(|g;' {} \;
find . -name "*.java" -exec perl -p -i -e 's|_test.name\(\)|_test.getName\(\)|g;' {} \;
find src/doc -name "*.xml" -exec perl -p -i -e 's|\222|&#x92;|g;' {} \;
%patch0
%patch1
%patch2

# Fix for wrong-file-end-of-line-encoding problem
for i in `find src/doc -iname "*.css"`; do sed -i 's/\r//' $i; done
for i in `find src/doc -iname "*.xsd"`; do sed -i 's/\r//' $i; done
for i in `find src/doc -iname "*.dtd"`; do sed -i 's/\r//' $i; done
for i in `find src/doc -iname "*.pdf"`; do sed -i 's/\r//' $i; done
for i in `find src/doc -iname "*.htm"`; do sed -i 's/\r//' $i; echo "" >> $i; done
sed -i 's/\r//' src/etc/README
sed -i 's/\r//' src/etc/LICENSE
sed -i 's/\r//' src/etc/CHANGELOG
sed -i 's/Class-Path: xerces.jar jdbc-se2.0.jar jndi.jar jta1.0.1.jar//' src/etc/MANIFEST.MF

%build
export ANT_OPTS=" -Dant.build.javac.source=1.4 -Dant.build.javac.target=1.4 "
export CLASSPATH=%(build-classpath adaptx jdbc-stdext jndi jta junit ldapjdk oro regexp apache-tomcat-apis/tomcat-servlet2.5-api xerces-j2)
ant -buildfile src/build.xml jar
ant -buildfile src/build.xml examples
ant -buildfile src/build.xml CTFjar
ant -buildfile src/build.xml javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 dist/%{name}-%{version}-xml.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xml-%{version}.jar
install -m 644 dist/CTF-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tests-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# examples (demo)
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}/examples
cp -pr build/examples/* $RPM_BUILD_ROOT%{_datadir}/%{name}/examples

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# do this last, since it will delete all build directories
export CLASSPATH=%(build-classpath log4j adaptx)
ant -buildfile src/build.xml doc

# like magic
%jpackage_script org.exolab.castor.builder.SourceGenerator %{nil} %{nil} xerces-j2:%{name} %{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm --exclude %{_datadir}/%{name}/examples/webapp-example-castor.war --exclude %{_datadir}/%{name}/examples/webapp/WEB-INF/lib/castor-0.9.5.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post test
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun test
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post xml
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun xml
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun demo
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc src/etc/{CHANGELOG,LICENSE,README}
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%dir %{_datadir}/%{name}

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/castor-0.9.5.jar.*
%endif

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}/examples

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/examples.*
%endif

%files test
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-tests-%{version}.jar
%{_javadir}/%{name}-tests.jar

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/castor-tests-0.9.5.jar.*
%endif

%files xml
%defattr(0644,root,root,0755)
%{_javadir}/%{name}-xml-%{version}.jar
%{_javadir}/%{name}-xml.jar

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

%files doc
%defattr(0644,root,root,0755)
%doc build/doc/*

%changelog
* Tue Feb 09 2010 Andrew Overholt <overholt@redhat.com> 0.9.5-5.3
- Use apache-tomcat-apis instead of generic servletapi.

* Fri Jan 15 2010 Jeff Johnston <jjohnstn@redhat.com> 0.9.5-5.2
- Resolves: #555942
- Fix license and release number

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.5-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri May 08 2009 Karsten Hopp <karsten@redhat.com> 0.9.5-4.1
- Specify source and target as 1.4 to make it build

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:0.9.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:0.9.5-3
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:0.9.5-2jpp.8
- Autorebuild for GCC 4.3

* Wed Apr 18 2007 Permaine Cheung <pcheung@redhat.com> - 0:0.9.5-1jpp.8
- Update spec file as per fedora review process.

* Thu Aug 03 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp.7
- Added missing requirements.

* Sat Jul 22 2006 Jakub Jelinek <jakub@redhat.com> - 0:0.9.5-1jpp_6fc
- Rebuilt

* Thu Jul  20 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp_5fc
- Added conditional native compilation.
- Added missing BR/R for log4j.

* Thu Jun  8 2006 Deepak Bhole <dbhole@redhat.com> - 0:0.9.5-1jpp_4fc
- Updated project URL -- fix for Bug #180586

* Wed Mar  8 2006 Rafael Schloming <rafaels@redhat.com> - 0:0.9.5-1jpp_3fc
- excluded s390[x] and ppc64 due to eclipse

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 0:0.9.5-1jpp_2fc
- stop scriptlet spew

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> 0:0.9.5-1jpp_1fc
- Build into Fedora.

* Fri Jun 10 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles and classfiles from the tarball.

* Thu Jun  2 2005 Gary Benson <gbenson@redhat.com>
- Fix up (alleged) invalid characters in the documentation.

* Fri Jul 23 2004 Fernando Nasser <fnasser@redhat.com> 0:0.9.5-1jpp_3rh
- use servletapi5 instead of servletapi4

* Thu Mar 11 2004 Frank Ch. Eigler <fche@redhat.com> 0:0.9.5-1jpp_2rh
- try servletapi4 instead of servletapi3
- add example-servletapi4 patch

* Thu Mar  4 2004 Frank Ch. Eigler <fche@redhat.com> 0:0.9.5-1jpp_1rh
- RH vacuuming

* Tue Sep 09 2003 David Walluck <david@anti-microsoft.org> 0:0.9.5-1jpp
- 0.9.5

* Fri May 16 2003 Nicolas Mailhot <Nicolas.Mailhot at laPoste.net> 0:0.9.4.3-2jpp
- use same lsapjdk package as tyrex

* Sat May 10 2003 David Walluck <david@anti-microsoft.org> 0:0.9.4.3-1jpp
- release
