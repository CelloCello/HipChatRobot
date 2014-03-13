# -*- coding: utf-8 -*-

# hello_world.py
from hippybot.decorators import botcmd, contentcmd
import goslate

gs = goslate.Goslate()

group_list = {} # no, OrderGroup

class Order(object):
    def __init__(self):
        self.client = ""
        self.product = ""
        self.price = 0


class OrderGroup(object):
    def __init__(self, no, name=""):
        self.no = no
        self.name = name
        self.order_list = {}    # name, Order  

    def add(self, order):
        self.order_list[order.client] = order  

        

class Plugin(object):
    global_commands = ('trs', 'wucha',)

    @botcmd
    def trs(self, mess, args):
        #channel = unicode(mess.getFrom()).split('/')[0]
        # Say hello world as a room notification
        # Params to the API wrapper are sent as dicts
        #print mess.getFrom()
        message = unicode(mess.getBody()).strip()
        message = message.replace('trs ', '')
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
    def wucha(self, mess, args):
        room = unicode(mess.getFrom()).split("/")[0]
        user = unicode(mess.getFrom()).split("/")[1]
        message = unicode(mess.getBody()).strip()
        message = message.replace('wucha ', '')
        msg_list = message.split(',')
        ans = ""
        cmd = msg_list[0]
        if cmd == "create":
            group_no = msg_list[1]
            name = msg_list[2]
            order_group = OrderGroup(group_no, name)
            group_list[group_no] = order_group
            ans = "You create a group: %s" % group_no
        elif cmd == "join":
            group_no = msg_list[1]
            if group_no in group_list:
                product = msg_list[2]
                price = msg_list[3]
                order = Order()
                order.client = user
                order.product = product
                order.price = price
                group_list[group_no].add(order)
                ans = "%s ordered: %s, %s" % (order.client, order.product, order.price)
            else:
                ans = "no this group: %s" % group_no
        elif cmd == "total":
            group_no = msg_list[1]
            if group_no in group_list:
                total_price = 0
                for key, val in group_list[group_no].order_list.iteritems():
                    ans += "%s ordered: %s, %s\n" % (val.client, val.product, val.price)
                    total_price += val.price

                ans += "==============================\n"
                ans += "total price: %s" % total_price
            
        rtn_msg = "from: %s \n user: %s \n body: %s \n mess: %s\n ans:%s" % (room, user, mess.getBody(), mess, ans)
        return rtn_msg