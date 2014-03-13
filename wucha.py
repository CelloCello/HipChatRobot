# -*- coding: utf-8 -*-

# wucha.py
from hippybot.decorators import botcmd, contentcmd
import sys

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
    global_commands = ('tea_help', 'tea_create', 'tea_buy', 'tea_total',)

    def __init__(self):
        self.room = ""
        self.user = ""
        self.message = ""

    def get_parm(self, mess, func_name):
        self.room = unicode(mess.getFrom()).split("/")[0]
        self.user = unicode(mess.getFrom()).split("/")[1]
        self.message = unicode(mess.getBody()).strip()
        self.message = self.message.replace(func_name, '')

    @botcmd
    def tea_help(self, mess, args):
        msg_list = []
        help_msg = "tea_help    幫助清單"
        msg_list.append(help_msg)        
        create_msg = "tea_create,<群組編號>,<群組名稱>    新建群組"
        msg_list.append(create_msg)
        buy_msg = "tea_buy,<群組編號>,<產品名稱>,<價錢>    訂購產品"
        msg_list.append(buy_msg)
        total_msg = "tea_total,<群組編號>    列出清單與總價"
        msg_list.append(total_msg)
        #rtn_msg = "命令列表：\n %s\n %s\n %s\n" % (create_msg, buy_msg, total_msg)
        rtn_msg = "命令列表：\n"
        for msg in msg_list:
            rtn_msg += msg + "\n"
        return rtn_msg.decode('big5').encode('utf-8')

    @botcmd
    def tea_create(self, mess, args):
        func_name = "%s " % sys._getframe().f_code.co_name
        self.get_parm(mess, func_name)
        msg_list = self.message.split(',')   
        group_no = msg_list[0]
        name = msg_list[1]
        order_group = OrderGroup(group_no, name)
        group_list[group_no] = order_group
        ans = "%s create a group: %s, %s \n (gangnamstyle)" % (self.user, group_no, name)
        rtn_msg = "[Robot] %s" % ans
        return rtn_msg

    @botcmd
    def tea_buy(self, mess, args):
        func_name = "%s " % sys._getframe().f_code.co_name
        self.get_parm(mess, func_name)
        msg_list = self.message.split(',')        
        group_no = msg_list[0]
        if group_no in group_list:
            product = msg_list[1]
            price = msg_list[2]
            order = Order()
            order.client = self.user
            order.product = product
            order.price = price
            group_list[group_no].add(order)
            ans = "%s ordered: %s, %s" % (order.client, order.product, order.price)
        else:
            ans = "no this group: %s" % group_no        

        rtn_msg = "[Robot] %s" % ans
        return rtn_msg

    @botcmd
    def tea_total(self, mess, args):
        func_name = "%s " % sys._getframe().f_code.co_name
        self.get_parm(mess, func_name)
        msg_list = self.message.split(',')        
        group_no = msg_list[0]
        ans = ""
        if group_no in group_list:
            total_price = 0
            for key, val in group_list[group_no].order_list.iteritems():
                ans += "%s ordered: %s, %s\n" % (val.client, val.product, val.price)
                total_price += int(val.price)

            ans += "==============================\n"
            ans += "total price: %s" % total_price     

        rtn_msg = "[Robot] %s" % ans
        return rtn_msg        
        
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