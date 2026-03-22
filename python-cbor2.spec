%define _debugsource_template %{nil}
%define module cbor2
# disable tests on ABF, passing locally
%bcond test 0

Name:		python-cbor2
Version:	5.9.0
Release:	1
Summary:	CBOR (de)serializer with extensive tag support
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/cbor2/
Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildRequires:	fdupes
BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(wheel)
# for libcbor
BuildRequires:	pkgconfig(libcbor)
BuildRequires:	pkgconfig(libcjson)
# for tests
%if %{with test}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(coverage)
BuildRequires:	python%{pyver}dist(hypothesis)
%endif

%description
This library provides encoding and decoding for the Concise Binary Object
Representation (CBOR) (RFC 8949) serialization format.

The specification is fully compatible with the original RFC 7049.

Read the docs to learn more.

It is implemented in pure python with an optional C backend.

%prep -a
# Remove bundled egg-info
rm -rf %{module}.egg-info

%build -p
export CFLAGS="%{optflags}"
export LDFLAGS="%{ldflags} -lpython%{pyver}"
# dont build cbor2 extension, use system library package libcbor
export CBOR2_BUILD_C_EXTENSION=0

%if %{with test}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest tests/
%endif

%files
%{_bindir}/%{module}
%{python_sitelib}/%{module}
%{python_sitelib}/%{module}-%{version}.dist-info
%doc README.rst
%license LICENSE.txt
