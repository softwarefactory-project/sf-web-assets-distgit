%global jqueryvisibilityversion b44a4ba9a46546b280dcb506620d3e63fefb200a

Name:          sf-web-assets
Version:       1.0
Release:       2%{?dist}
Summary:       The /var/www/static directory used by sf web interface
License:       MIT
URL:           https://softwarefactory-project.io
BuildArch:     noarch

BuildRequires: python-pathlib
BuildRequires: python-enum34
BuildRequires: python-scss

BuildRequires: uglify-js
BuildRequires: python-XStatic-Bootstrap-SCSS
BuildRequires: python-XStatic-Angular

Requires:      fontawesome-fonts-web
Requires:      js-jquery1
Requires:      python-XStatic-Bootstrap-SCSS

Source0:       https://github.com/mathiasbynens/jquery-visibility/archive/%{jqueryvisibilityversion}.tar.gz
Source1:       http://status.openstack.org/jquery-graphite.js
Source2:       static.httpd.conf

Provides:      bundled(python-XStatic-Bootstrap-SCSS)
Provides:      bundled(python-XStatic-Angular)
Provides:      bundled(js-jquery-visibility)
Provides:      bundled(js-jquery-graphite)


%description
This package setup the /var/www/static directory used by the sf web interface.


%prep
%autosetup -n jquery-visibility-%{jqueryvisibilityversion}


%build
mkdir -p build/js build/bootstrap/css build/bootstrap/js
uglifyjs jquery-visibility.js -o build/js/jquery-visibility.min.js
uglifyjs %{SOURCE1} -o build/js/jquery.graphite.min.js
uglifyjs /usr/share/javascript/angular/angular.js -o build/js/angular.min.js
uglifyjs /usr/share/javascript/bootstrap_scss/js/bootstrap.js -o build/bootstrap/js/bootstrap.min.js
pyscss /usr/share/javascript/bootstrap_scss/scss/bootstrap.scss -o build/bootstrap/css/bootstrap.min.css


%install
install -p -D -m 0644 %{SOURCE2} %{buildroot}/etc/httpd/conf.d/sfstatic.conf
mkdir -p %{buildroot}/var/www
cp -r build %{buildroot}/var/www/static
ln -s /usr/share/javascript/jquery/1/jquery.min.js %{buildroot}/var/www/static/js/jquery.min.js
ln -s /usr/share/font-awesome-web/ %{buildroot}/var/www/static/font-awesome
ln -s /usr/share/javascript/bootstrap_scss/fonts/ %{buildroot}/var/www/static/bootstrap/css/static


%files
/etc/httpd/conf.d/sfstatic.conf
/var/www/static


%changelog
* Mon Feb 20 2017 Tristan Cacqueray - 1.0-1
- Initial packaging
