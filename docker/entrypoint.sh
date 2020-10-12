#!/usr/bin/env sh

echo "$CRON python3 /opt/app/notification.py" > /etc/crontabs/root
echo "" >> /etc/crontabs/root
chmod +x /etc/crontabs/root
chmod +x /opt/app/notification.py
crond -L /var/log/cron.log -l 1 &
python3 app/api.py
