FROM debian:jessie-slim

ADD install.sh /opt/install.sh

RUN groupadd --gid 15000 cometh && \
	useradd -M --uid 15000 --gid 15000 cometh && \
	chmod u+x /opt/install.sh && \
	export DEBIAN_FRONTEND=noninteractive && \
	apt-get update && \
	apt-get install -y \
		dovecot-core \
		dovecot-lmtpd \
		dovecot-imapd \
		dovecot-pop3d \
		dovecot-sieve \
		dovecot-managesieved \
		dovecot-antispam \
		dovecot-solr \
		dovecot-mysql \
		supervisor \
		&& \
	rm -rf /etc/dovecot/conf.d

#COPY conf /etc/dovecot/conf.d/

EXPOSE 443 993 110

#ENTRYPOINT ["/usr/sbin/dovecot", "-F"]
CMD ["sh", "-c", "/opt/install.sh ; /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf"]
