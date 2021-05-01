# Buck-Off

## Install the Adafruit Libraries
```
pip3 install adafruit-blinka
pip3 install adafruit-circuitpython-lis3dh
pip3 install RPi.GPIO
```

## Install Systemd Service File
`mkdir ~/.config/systemd/user`

`cp Buck-off/Buck-off/service/bo.service ~/.config/systemd/user/bo.service`

`systemctl --user daemon-reload`

`systemctl --user enable bo`

`systemctl --user restart bo`
