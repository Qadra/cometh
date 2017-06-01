FROM debian:jessie-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd --gid 15000 cometh && \
	useradd -M --uid 15000 --gid 15000 cometh && \
	export DEBIAN_FRONTEND=noninteractive && \
	apt-get update && \
	apt-get install -y \
		spamassassin spamc spamass-milter \
		supervisor \
		rsyslog

ADD install.sh /opt/install.sh

CMD ["sh", "-c", "sh /opt/install.sh ; /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
