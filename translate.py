# -*- coding: utf-8 -*-

# translate.py
from hippybot.decorators import botcmd, contentcmd
import goslate

gs = goslate.Goslate()

        

class Plugin(object):
    global_commands = ('trs_ja', 'trs_en')
        
    @botcmd
    def trs_ja(self, mess, args):
        #channel = unicode(mess.getFrom()).split('/')[0]
        # Say hello world as a room notification
        # Params to the API wrapper are sent as dicts
        #print mess.getFrom()
        message = unicode(mess.getBody()).strip()
        message = message.replace('trs_ja ', '')
        sender_name = unicode(mess.getFrom()).split('/')[1]
        rtn_msg = "from: %s \n body: %s \n trs: %s \n mess: %s" % (sender_name, mess.getBody(), gs.translate(message, 'ja'), mess)
        #return "[Robot] %s" % (gs.translate(message, 'ja'))
        return rtn_msg
        self.bot.api.rooms.message({
            'room_id': 431393,
            'from': self.bot._config['connection']['nickname'],
            'message': 'Hello world!'
        })

    @botcmd
    def trs_en(self, mess, args):
        message = unicode(mess.getBody()).strip()
        message = message.replace('trs_en ', '')
        sender_name = unicode(mess.getFrom()).split('/')[1]
        rtn_msg = "from: %s \n body: %s \n trs: %s \n mess: %s" % (sender_name, mess.getBody(), gs.translate(message, 'en'), mess)
        #return "[Robot] %s" % (gs.translate(message, 'ja'))
        return rtn_msg
