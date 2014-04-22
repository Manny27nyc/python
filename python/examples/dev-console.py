## www.pubnub.com - PubNub Real-time push service in the cloud. 
# coding=utf8

## PubNub Real-time Push APIs and Notifications Framework
## Copyright (c) 2010 Stephen Blum
## http://www.pubnub.com/

## -----------------------------------
## PubNub 3.1 Real-time Push Cloud API
## -----------------------------------

import sys
sys.path.append('../')
sys.path.append('../../')
from Pubnub import Pubnub

from optparse import OptionParser


parser = OptionParser()

parser.add_option("--publish-key",
                  dest="publish_key", default="demo",
                  help="Publish Key ( default : 'demo' )")

parser.add_option("--subscribe-key",
                  dest="subscribe_key", default="demo",
                  help="Subscribe Key ( default : 'demo' )")

parser.add_option("--secret-key",
                  dest="secret_key", default="demo",
                  help="Secret Key ( default : 'demo' )")

parser.add_option("--cipher-key",
                  dest="cipher_key", default="",
                  help="Cipher Key")

parser.add_option("--auth-key",
                  dest="auth_key", default=None,
                  help="Auth Key")

parser.add_option("--origin",
                  dest="origin", default="pubsub.pubnub.com",
                  help="Origin ( default: pubsub.pubnub.com )")

parser.add_option("--ssl-on",
                  action="store_false", dest="ssl", default=False,
                  help="SSL")

parser.add_option("--uuid",
                  dest="uuid", default=None,
                  help="UUID")

(options, args) = parser.parse_args()

print(options)

pubnub = Pubnub(options.publish_key, options.subscribe_key, options.secret_key, options.cipher_key, options.auth_key, options.ssl, options.origin, options.uuid)


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def print_ok(msg, channel=None):
    chstr = " [Channel : " + channel + "] " if channel is not None else "" 
    try:
        print(color.GREEN + chstr + str(msg) + color.END)
    except:
        print(msg)

def print_error(msg, channel=None):
    chstr = " [Channel : " + channel + "] " if channel is not None else "" 
    try:
        print(color.RED + color.BOLD +  chstr + str(msg) + color.END)
    except:
        print(msg)

def get_input(message, t=None):
    while True:
        try:
            try:
                command = raw_input(message)
            except NameError:
                command = input(message)
            if t is not None and t == bool:
                if command in ["True", "true", "1", 1, "y", "Y", "yes", "Yes", "YES"]:
                    return True
                else:
                    return False
            if t is not None:
                command = t(command)
            else:
                command = eval("'" + command + "'")

            return command
        except ValueError:
            print_error("Invalid input : " + command)



def _publish_command_handler():

    channel = get_input("[PUBLISH] Enter Channel Name ", str)
    while True:
        message = get_input("[PUBLISH] Enter Message ( QUIT for exit from publish mode ) ")
        if message == 'QUIT' or message == 'quit':
            return  
        def _callback(r):
            print_ok(r)
        def _error(r):
            print_error(r)
        pubnub.publish({
            'channel' : channel,
            'message' : message,
            'callback' : _callback,
            'error'   : _error
        })


def _subscribe_command_handler():
    channel = get_input("[SUBSCRIBE] Enter Channel Name ", str)
    def _callback(r):
        print_ok(r, channel)
    def _error(r):
        print_error(r, channel)
    pubnub.subscribe({
        'channel' : channel,
        'callback' : _callback,
        'error'   : _error
    })

def _unsubscribe_command_handler():
    channel = get_input("[UNSUBSCRIBE] Enter Channel Name ", str)
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    pubnub.unsubscribe({
        'channel' : channel,
        'callback' : _callback,
        'error'   : _error
    })    

def _grant_command_handler():
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    channel = get_input("[GRANT] Enter Channel Name ", str)
    auth_key = get_input("[GRANT] Enter Auth Key ", str)
    ttl = get_input("[GRANT] Enter ttl ", int)
    read = get_input("[GRANT] Read ? ", bool)
    write = get_input("[GRANT] Write ? ", bool)
    pubnub.grant(channel, auth_key,read,write,ttl, _callback)

def _revoke_command_handler():
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    channel = get_input("[REVOKE] Enter Channel Name ", str)
    auth_key = get_input("[REVOKE] Enter Auth Key ", str)
    ttl = get_input("[REVOKE] Enter ttl ", int)

    pubnub.revoke(channel, auth_key, ttl, _callback)

def _audit_command_handler():
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    channel = get_input("[AUDIT] Enter Channel Name ", str)
    auth_key = get_input("[AUDIT] Enter Auth Key ", str)
    pubnub.audit(channel, auth_key, _callback)

def _history_command_handler():
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    channel = get_input("[HISTORY] Enter Channel Name ", str)
    count = get_input("[HISTORY] Enter Count ", int)

    pubnub.history({
        'channel' : channel,
        'count'   : count,
        'callback' : _callback,
        'error'   : _error
    })


def _here_now_command_handler():
    def _callback(r):
        print_ok(r)
    def _error(r):
        print_error(r)
    channel = get_input("[HERE NOW] Enter Channel Name ", str)

    pubnub.here_now({
        'channel' : channel,
        'callback' : _callback,
        'error'   : _error
    })



import threading

def kill_all_threads():
    for thread in threading.enumerate():
        if thread.isAlive():
            try:
                thread._Thread__stop()
            except Exception as e:
                pass
                #print(e)
                #thread.exit()
                #print(str(thread.getName()) + ' could not be terminated')


commands = []
commands.append({"command" : "publish", "handler" : _publish_command_handler})
commands.append({"command" : "subscribe", "handler" : _subscribe_command_handler})
commands.append({"command" : "unsubscribe", "handler" : _unsubscribe_command_handler})
commands.append({"command" : "here_now", "handler" : _here_now_command_handler})
commands.append({"command" : "history", "handler" : _history_command_handler})
commands.append({"command" : "grant", "handler" : _grant_command_handler})
commands.append({"command" : "revoke", "handler" : _revoke_command_handler})
commands.append({"command" : "audit", "handler" : _audit_command_handler})

# last command is quit. add new commands before this line
commands.append({"command" : "QUIT"})

def get_help():
    help = ""
    help += "Channels currently subscribed to : "
    help += str(pubnub.get_channel_array())
    help += "\n"
    for i,v in enumerate(commands):
        help += "Enter " + str(i) + " for " + v['command'] + "\n"
    return help

            
while True:
    try:
        command = get_input(color.BLUE + get_help(), int)
    except KeyboardInterrupt:
        kill_all_threads()
        break
    if command == len(commands) - 1:
        kill_all_threads()
        break
    if command >= len(commands):
        print_error("Invalid input " + str(command))
        continue

    commands[command]['handler']()

#pubnub.start()
