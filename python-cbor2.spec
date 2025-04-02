%define debug_package %{nil}
%define module cbor2
# tests disabled for abf
%bcond_with test

Name:		python-cbor2
Version:	5.6.5
Release:	1
Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
Summary:	CBOR (de)serializer with extensive tag support
URL:		https://pypi.org/project/cbor2/
License:	MIT
Group:		Development/Python
BuildSystem:	python

BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(python-%{pyver})
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
# for libcbor
BuildRequires:	pkgconfig(libcbor)
BuildRequires:	pkgconfig(libcjson)
# for tests
%if %{with test}
BuildRequires:	python%{pyver}dist(attrs)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(coverage)
BuildRequires:	python%{pyver}dist(hypothesis)
BuildRequires:	python%{pyver}dist(iniconfig)
BuildRequires:	python%{pyver}dist(packaging)
BuildRequires:	python%{pyver}dist(pluggy)
BuildRequires:	python%{pyver}dist(sortedcontainers)
%endif

%description
This library provides encoding and decoding for the Concise Binary Object
Representation (CBOR) (RFC 8949) serialization format.

The specification is fully compatible with the original RFC 7049.

Read the docs to learn more.

It is implemented in pure python with an optional C backend.

##################################

%prep
%autosetup -p1 -n %{module}-%{version}
# remove git badge URLs from README.rst
sed -i '1,13d' README.rst

%build
export CFLAGS="%{optflags}"
export LDFLAGS="%{ldflags} -v"
# dont build cbor2 extension, use system library package libcbor
export CBOR2_BUILD_C_EXTENSION=0
%py_build

%install
%py3_install

%if %{with test}
%check
pip install -e .[test]
%{__python} -m pytest -v tests/
%endif

%files
%{_bindir}/%{module}
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}*.*-info/
%doc README.rst
%license LICENSE.txt
