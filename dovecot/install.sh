#!/bin/bash

cat > /etc/supervisor/conf.d/supervisord.conf <<EOF
[supervisord]
nodaemon=true

[program:dovecot]
command=/usr/sbin/dovecot -F
redirect_stderr=true
EOF
