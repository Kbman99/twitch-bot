# bot.py
# The code for out bot

import cfg
import utils
import socket
import re
import time, thread
from time import sleep

def main():
    # Networking functions
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")

    thread.start_new_thread(utils.threadFillOpList, ())

    while True:
        response = s.recv(1024).decode("utf-8")
        if response == "PINT :time.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)

            # Custom commands
            if message.strip() == "!time":
                utils.chat(s, "It is currently " + time.strftime("%I:%M %p %Z on %A, %B %d, %Y."))
            if message.strip() == "!messages" and utils.isOp(username):
                utils.chat(s, "Welcome to KBman99's Live Stream! Please follow below to see when I go live next!")
            if message.strip() == "!twitter":
                utils.chat(s, "My twitter is https://twitter.com/_the_kB")
        sleep(1)

if __name__ == "__main__":
    main()