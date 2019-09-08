sudo apt-get install -y supervisor

sudo mkdir /usr/share/elasticsearch
cd /usr/share/elasticsearch

sudo wget https://download.elastic.co/kibana/kibana/kibana-4.6.1-linux-x86_64.tar.gz
sudo wget https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.0/elasticsearch-2.4.0.tar.gz
sudo wget https://download.elastic.co/logstash/logstash/logstash-2.4.0.tar.gz
sudo wget http://node-arm.herokuapp.com/node_latest_armhf.deb

sudo tar xvfz elasticsearch-2.4.0.tar.gz
sudo rm elasticsearch-2.4.0.tar.gz

mkdir /etc/elasticsearch
sudo cp /usr/share/elasticsearch/elasticsearch-1.4.4/config/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

sudo sed -i '/cluster.name:.*/a cluster.name: logstash' /etc/elasticsearch/elasticsearch.yml
sudo sed -i '/path.data:.*/a path.data: /home/pi/src/elk/data/' /etc/elasticsearch/elasticsearch.yml

sudo mv elasticsearch-2.4.0/* .
sudo rm -rf elasticsearch-2.4.0/

sudo /usr/share/elasticsearch/elasticsearch-1.4.4/bin/elasticsearch
curl -XGET http://10.0.1.32:9200/

sudo tar zxvf logstash-2.4.0.tar.gz
sudo mv logstash-2.4.0 /opt/logstash-2.4.0
sudo ln -s /opt/logstash-2.4.0 /opt/logstash
sudo mkdir -p /etc/logstash/conf.d
sudo cp /mnt/TimeCapsule1/raspberrypi/etc/logstash/conf.d/* /etc/logstash/conf.d/
sudo mkdir -p /var/log/logstash/

https://github.com/jruby/jruby/issues/1561
cd /tmp/
sudo git clone https://github.com/jnr/jffi.git
cd jffi/
sudo apt-get install -y ant openjdk-7-jdk zip
sudo ant jar
sudo mkdir -p /opt/logstash-1.4.2/vendor/jar/jni/arm-Linux/
sudo cp /tmp/jffi/build/jni/libjffi-1.2.so /opt/logstash-1.4.2/vendor/jar/jni/arm-Linux/
cd /opt/logstash-1.4.2/vendor/jar
sudo zip -g jruby-complete-1.7.11.jar jni/arm-Linux/libjffi-1.2.so

USE_JRUBY=1 LS_HEAP_SIZE=64m ./bin/logstash -e 'input { stdin { } } output { stdout { } }'

cd /usr/share/elasticsearch
sudo tar xvfz kibana-4.6.1-linux-x86_64.tar.gz
sudo mv kibana-4.6.1-linux-x86_64 /opt/kibana-4.6.1-linux-x86_64
sudo rm kibana-4.6.1-linux-x86_64.tar.gz

sudo ln -s /opt/kibana-4.6.1-linux-x86_64/ /opt/kibana

sudo dpkg -i node_latest_armhf.deb
sudo mv /opt/kibana-4.6.1-linux-x86_64/node/bin/node /opt/kibana-4.6.1-linux-x86_64/node/bin/node.orig
sudo mv /opt/kibana-4.6.1-linux-x86_64/node/bin/npm /opt/kibana-4.6.1-linux-x86_64/node/bin/npm.orig
sudo ln -s /usr/local/bin/node /opt/kibana-4.6.1-linux-x86_64/bin/node
sudo ln -s /usr/local/bin/npm /opt/kibana-4.6.1-linux-x86_64/bin/npm

sudo /opt/kibana/bin/kibana

sudo cp /mnt/TimeCapsule1/raspberrypi/etc/supervisor/conf.d/* /etc/supervisor/conf.d/

sudo /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

#--- /etc/supervisor/conf.d/kibana.conf
[program:kibana]
command=/opt/kibana/bin/kibana
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/supervisor/kibana.log
stderr_logfile=/var/log/supervisor/error.log

--- /etc/supervisor/conf.d/es.conf
[program:elasticsearch]
command=/usr/share/elasticsearch/bin/elasticsearch -Des.http.port=9201 -Des.network.host=192.168.1.33
numprocs=1
user=root
autostart=true
autorestart=true

--- /etc/supervisor/conf.d/logstash.conf
[program:logstash]
command=/opt/logstash/bin/logstash agent --config /etc/logstash/conf.d/ --log /var/log/logstash/logstash.log
numprocs=1
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/supervisor/logstash.out.log
stderr_logfile=/var/log/supervisor/logstash.err.log

sudo supervisorctl reread
sudo supervisorctl reload

Allow java to open privileged ports (for remote syslog logging on port 514)
sudo setcap cap_net_bind_service=+epi /usr/lib/jvm/java-7-openjdk-armhf/jre/bin/java