FROM debian:jessie-slim

RUN groupadd --gid 15000 cometh && \
	useradd -M --uid 15000 --gid 15000 cometh && \
	export DEBIAN_FRONTEND=noninteractive && \
	apt-get update && \
	apt-get install -y \
		supervisor \
		postfix \
		postfix-mysql \
		rsyslog \
		spamc \
		&& \
	chown cometh: /var/lib/postfix

ADD install.sh /opt/install.sh

RUN chmod +x /opt/install.sh

EXPOSE 25

CMD ["sh", "-c", "/opt/install.sh ; /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
