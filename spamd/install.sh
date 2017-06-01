#!/bin/bash

cat > /etc/supervisor/conf.d/supervisord.conf <<EOF
[supervisord]
nodaemon=true

[program:spamd]
command=spamd -x
redirect_stderr=true

[program:spamass-milter]
user=cometh
command=/usr/sbin/spamass-milter -p /var/spool/postfix/spamass/spamass.sock -r 8 -d misc,rcpt

[program:rsyslog]
command=rsyslogd -n
EOF
