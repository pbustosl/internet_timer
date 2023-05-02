# internet

### service

Laptop:
```
[~/git/internet_timer]$ scp service/internet_timer.service rb:/etc/systemd/system/
[~/git/internet_timer]$ scp service/internet_timer.sh rb:/usr/local/bin/
```

Server:
```
sudo systemctl daemon-reload

sudo systemctl enable internet_timer.service
sudo systemctl start internet_timer.service
sudo systemctl status internet_timer.service
```
