%global jqueryvisibilityversion b44a4ba9a46546b280dcb506620d3e63fefb200a
%global simplepaginationversion 07c37285fafc7dbabce0392f730037ac012cc3ea

Name:          sf-web-assets
Version:       1.0
Release:       6%{?dist}
Summary:       The /var/www/static directory used by sf web interface
License:       MIT and BSD
URL:           https://softwarefactory-project.io
BuildArch:     noarch

BuildRequires: python-pathlib
BuildRequires: python-enum34
BuildRequires: python-scss

BuildRequires: python2-rjsmin
BuildRequires: python-XStatic-Bootstrap-SCSS
BuildRequires: python-XStatic-Angular

Requires:      xstatic-patternfly-common
Requires:      fontawesome-fonts-web
Requires:      python-XStatic-Bootstrap-SCSS
Requires:      python-XStatic-jQuery

Source0:       https://github.com/mathiasbynens/jquery-visibility/archive/%{jqueryvisibilityversion}.tar.gz
Source1:       http://status.openstack.org/jquery-graphite.js
Source2:       static.httpd.conf
Source3:       https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.17.1/moment.js
Source4:       https://github.com/flaviusmatis/simplePagination.js/archive/%{simplepaginationversion}.tar.gz
Source5:       https://github.com/d3/d3/archive/v3.1.6.tar.gz
Source6:       https://cdnjs.cloudflare.com/ajax/libs/dimple/2.2.0/dimple.latest.js
Source7:       https://jqueryui.com/resources/download/jquery-ui-1.12.1.zip
Source8:       https://raw.githubusercontent.com/vuejs/vue/90891709708e8ebdc1522eed678a49eb9f312fda/dist/vue.min.js

Provides:      bundled(python-XStatic-Bootstrap-SCSS)
Provides:      bundled(python-XStatic-Angular)
Provides:      bundled(js-jquery-visibility)
Provides:      bundled(js-jquery-graphite)
Provides:      bundled(js-moment)
Provides:      bundled(js-simplepagination)
Provides:      bundled(js-d3)
Provides:      bundled(vuejs)


%description
This package setup the /var/www/static directory used by the sf web interface.


%prep
%setup -T -D -c
%setup -T -D -a 0
%setup -T -D -a 4
%setup -T -D -a 5
%setup -T -D -a 7


%build
mkdir -p build/js build/css
mkdir -p build/bootstrap/css build/bootstrap/js
mkdir -p build/jquery-ui/css build/jquery-ui/js build/jquery-ui/images
mv %{SOURCE8} build/js
python2 -mrjsmin < jquery-visibility-%{jqueryvisibilityversion}/jquery-visibility.js > build/js/jquery-visibility.min.js
python2 -mrjsmin < %{SOURCE1} > build/js/jquery.graphite.min.js
python2 -mrjsmin < %{SOURCE3} > build/js/moment.min.js
python2 -mrjsmin < %{SOURCE6} > build/js/dimple.min.js
python2 -mrjsmin < d3-3.1.6/d3.js > build/js/d3.min.js
python2 -mrjsmin < /usr/share/javascript/angular/angular.js > build/js/angular.min.js
python2 -mrjsmin < /usr/share/javascript/bootstrap_scss/js/bootstrap.js > build/bootstrap/js/bootstrap.min.js
pyscss /usr/share/javascript/bootstrap_scss/scss/_bootstrap.scss -o build/bootstrap/css/bootstrap.min.css
cp simplePagination.js-%{simplepaginationversion}/simplePagination.css build/css/simplePagination.css
cp simplePagination.js-%{simplepaginationversion}/jquery.simplePagination.js build/js/jquery.simplePagination.js
python2 -mrjsmin < jquery-ui-1.12.1/jquery-ui.js > build/jquery-ui/js/jquery-ui.min.js
# pyscss jquery-ui-1.12.1/jquery-ui.css -o build/jquery-ui/css/jquery-ui.min.css
# Unable to minimify the css due to the error below. So using the minified directly
# scss.errors.SassSyntaxError: Syntax error after u'Alpha(Opacity': Found u'=0)' but expected one of ",", ":",
# ADD, ALPHA_FUNCTION, AND, BANG_IMPORTANT, BAREWORD, COLOR, DIV, DOUBLE_QUOTE, END, EQ, FNCT, GE, GT,
# INTERP_END, INTERP_START, LE, LITERAL_FUNCTION, LPAR, LT, MOD, MUL, NE, NOT, NUM, OR, RPAR, SIGN,
# SINGLE_QUOTE, SPACE, SUB, URL_FUNCTION, VAR
cp jquery-ui-1.12.1/jquery-ui.min.css build/jquery-ui/css/jquery-ui.min.css
cp -v jquery-ui-1.12.1/images/* build/jquery-ui/images/

%install
install -p -D -m 0644 %{SOURCE2} %{buildroot}/etc/httpd/conf.d/sfstatic.conf
mkdir -p %{buildroot}/var/www
cp -r build %{buildroot}/var/www/static
ln -s /usr/lib/python2.7/site-packages/xstatic/pkg/jquery/data/jquery.min.js %{buildroot}/var/www/static/js/jquery.min.js
ln -s /usr/share/font-awesome-web/ %{buildroot}/var/www/static/font-awesome
ln -s /usr/share/javascript/bootstrap_scss/fonts/ %{buildroot}/var/www/static/bootstrap/css/static
ln -s /usr/share/javascript/patternfly/ %{buildroot}/var/www/static/patternfly


%files
/etc/httpd/conf.d/sfstatic.conf
/var/www/static


%changelog
* Mon Aug 20 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 1.0-6
- Add patternfly xstatic

* Sun Jul  8 2018 Tristan Cacqueray <tdecacqu@redhat.com> - 1.0-5
- Add vuejs-2.15.6

* Tue Apr 18 2017 Tristan Cacqueray <tdecacqu@redhat.com> - 1.0-4
- Use rjsmin instead of uglify
- Use python-XStatic-jQuery instead of js-jquery1

* Wed Mar 15 2017 Fabien Boucher <fboucher@redhat.com> - 1.0-3
- Add assets for repoxplorer

* Wed Mar 01 2017 Nicolas Hicher - 1.0-2
- Add missing requirement

* Mon Feb 20 2017 Tristan Cacqueray - 1.0-1
- Initial packaging
