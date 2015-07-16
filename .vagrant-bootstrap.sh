#!/usr/bin/env bash

# Fail as soon as any command fails
set -e

# Only run this script on the first run
[[ -f ~vagrant/.first_run_done ]] && exit 0

# Update the machine
apt-get update

# Install binary dependencies
apt-get install --no-install-recommends -y \
    gettext git \
    imagemagick \
    libyaml-0-2 libyaml-dev \
    mongodb \
    python python-{dev,geoip,pip,pysqlite2} \
    redis-server ruby \
    emacs23-nox vim tmux

# Install Node.js from pre-built tarball
# if [[ ! -f /usr/local/bin/node ]]; then
#     mkdir -p /tmp/node
#     cd /tmp/node
#     wget http://nodejs.org/dist/v0.10.12/node-v0.10.12-linux-x64.tar.gz
#     tar xf node-*.tar.gz
#     for d in bin lib share; do
#         mkdir -p /usr/local/$d
#         mv node-*/$d/* /usr/local/$d/
#     done
#     cd -
#     rm -rf /tmp/node
# fi

# Install Ruby dependencies
gem install sass

# Install pure-Python dependencies
pip install -r /vagrant/requirements.txt

# Prepare local settings
if [[ ! -f /vagrant/findspire/local_settings.py ]]; then
    cat > /vagrant/findspire/local_settings.py <<EOF
DEBUG = True
COMPRESS_ENABLED = False
PROMOTION_MODE = False

DATABASES['default']['NAME'] = "/findspire.db"
MODEL_BACKEND = "DatastoreBackend"
MIDDLEWARE_CLASSES = (c for c in MIDDLEWARE_CLASSES if "GeoIP" not in c and "BasicAuth" not in c)

RIAKCS_URL = "http://riakcs.dev.findspire.com/"
STORAGE_REDIS = None
STORAGE_PROVIDERS = {
    "findspire": {
        "paris": {
            "download": {
                "status": "OK",
                "url_format": RIAKCS_URL + "%(bucket)s/%(object)s",
            },
            "upload": {
                "status": "OK",
                "method": "s3",
                "params": {
                    "aws_access_key_id": "UFHS0WTCGAG-UQN-GTG2",
                    "aws_secret_access_key": "tF1VOpihlzFQxgGkDixryyWENnylyDav9UQ6SQ==",
                    "host": "riakcs.dev.findspire.com",
                    "port": 7080,
                    "is_secure": False,
                    "calling_format": "boto.s3.connection.OrdinaryCallingFormat",
                },
            },
        },
    },
}

# If you downloaded the content of RiakCS (for offline access), uncomment the
# following lines:
# RIAKCS_URL = "http://127.0.0.1:8000/datastore/objects/"
# STORAGE_PROVIDERS = {
#     "findspire": {
#         "paris": {
#             "download": {
#                 "status": "OK",
#                 "url_format": RIAKCS_URL + "%(bucket)s/%(object)s",
#             },
#             "upload": {
#                 "status": "OK",
#                 "method": "put",
#                 "url_format": RIAKCS_URL + "%(bucket)s/%(object)s",
#             },
#         },
#     },
# }


EOF
fi

# Prepare helper scripts
if [[ ! -f ~vagrant/runserver ]]; then
    cat > ~vagrant/runserver <<EOF
#!/usr/bin/env bash

# Make sure Mongo and Redis are running
for serv in mongodb redis-server; do
    sudo /etc/init.d/\$serv status >/dev/null || sudo /etc/init.d/\$serv start
done

# Start the Django server
cd /vagrant
exec sudo ./runserver.sh
EOF
    cat > ~vagrant/runworker <<EOF
#!/usr/bin/env bash

# Wait for Django/Redis/whatever to be working
sleep 5

# Start a celery worker
cd /vagrant
exec sudo ./manage.py celery worker -l INFO
EOF
    chown vagrant:vagrant ~vagrant/runserver ~vagrant/runworker
    chmod +x ~vagrant/runserver ~vagrant/runworker
fi

# Syncdb and populatedb
cd /vagrant
sudo ./manage.py syncdb --all --noinput
sudo ./superuser.py
sudo ./populatedb.py

# Process locales
cd findspire
./process-locales.sh

touch ~vagrant/.first_run_done
