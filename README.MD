# BrawlSnake
Brawl Stars client implemented in Python.

This is a port of https://github.com/PeterHackz/BrawlStars-Client which is implemented in JavaScript (nodejs). I ported it to Python (and changed some stuff to make it more pythonic). It is licensed with MIT and the license is included in LICENSE_ORIG file.

Current Brawl Stars server version supported by this library is v58.

# Installing
1. Clone this repo, rename `src` to `brawlsnake` and use it in your code. Maybe I'll upload it to pip later. Right now, it's not up there and this repository is the only way to get it.
2. Go into `TweetNaCl` directory, build it with `setup.py` file and install. (install setuptools if you haven't already). This is required due to fact that Brawl Stars server is using 19 rounds of salsa20 instead of 20.

# Example client
```py
from brawlsnake.client import Client, get_default_settings
import brawlsnake.messages

c = Client(get_default_settings())

@c.on_packet(brawlsnake.messages.server.LoginOkMessage.packet_type)
def on_own_home(pkt):
    print("Connected!")

c.connect()
```

# License
This project is licensed under the BSD 3-clause license, read LICENSE file for more. Original project (https://github.com/PeterHackz/BrawlStars-Client) is licensed under the MIT license, read LICENSE_ORIG file for more.
