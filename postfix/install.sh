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

cat > /etc/mailname <<EOF
${MAILNAME}
EOF
