#!/bin/sh

cd ..

if [[ -d 'conf/' ]]; then
    echo "Error: Directory 'conf/' is exists."
    exit 1
fi

cp -r conf.template conf
cd conf/
rm -rf generate_conf.sh
mv template.supervisor_api.conf supervisor_api.conf
mv template.uwsgi_api.ini uwsgi_api.ini
mv template.supervisor_admin.conf supervisor_admin.conf
mv template.uwsgi_admin.ini uwsgi_admin.ini

exit 0
