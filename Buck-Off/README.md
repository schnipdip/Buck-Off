# Buck-Off

## Install the Adafruit Libraries
`pip install 

## Install Systemd Service File
`mkdir ~/.config/systemd/user`

`cp Buck-off/Buck-off/service/bo.service ~/.config/systemd/user/bo.service`

`systemctl --user daemon-reload`

`systemctl --user enable bo`

`systemctl --user restart bo`
