%define _debugsource_template %{nil}
%define module cbor2

%bcond test 1

Name:		python-cbor2
Version:	6.0.1
Release:	1
Summary:	Python CBOR (de)serializer with extensive tag support
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/cbor2/
Source0:	https://files.pythonhosted.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-%{version}-vendor.tar.xz

BuildSystem:	python
BuildRequires:	cargo
BuildRequires:	rust-packaging
BuildRequires:	pkgconfig(pybind11)
BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(setuptools-rust)
BuildRequires:	python%{pyver}dist(wheel)
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

%prep -a
pushd rust
# Extract vendored crates
tar xf %{S:1}
# Prep vendored crates dir
%cargo_prep -v vendor/
popd

%build -p
export CARGO_HOME=$PWD/rust/.cargo
export RUSTFLAGS="-lpython%{pyver}"

%build -a
pushd rust
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > ../LICENSES.dependencies
popd

%if %{with test}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
pytest tests/
%endif

%files
%doc README.rst
%license LICENSE.txt LICENSES.dependencies
%{_bindir}/%{module}
%{python_sitearch}/%{module}
%{python_sitearch}/%{module}-%{version}.dist-info
