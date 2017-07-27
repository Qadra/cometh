#!/usr/bin/env bash

cat > /etc/supervisor/conf.d/supervisord.conf <<EOF
[supervisord]
nodaemon=true

[program:postfix]
command=/opt/postfix.sh

[program:rsyslog]
command=rsyslogd -n
EOF

cat > /opt/postfix.sh <<EOF
#!/usr/bin/env bash
service postfix start
tail -F /var/log/mail.log
EOF

chmod +x /opt/postfix.sh


postconf -e myhostname=${MAILNAME}
postconf -e myorigin=${MAILNAME}

postconf -e smtpd_tls_CAfile=/etc/certs/chain.pem
postconf -e smtpd_tls_cert_file=/etc/certs/cert.pem
postconf -e smtpd_tls_key_file=/etc/certs/key.pem

postconf -e smtpd_tls_loglevel=1
postconf -e smtpd_tls_received_header=yes
postconf -e smtpd_tls_security_level=may
postconf -e smtpd_use_tls=yes

# When contacting other servers
postconf -e smtp_tls_note_starttls_offer=yes
postconf -e smtp_use_tls=yes

cat > /etc/mailname <<EOF
${MAILNAME}
EOF
