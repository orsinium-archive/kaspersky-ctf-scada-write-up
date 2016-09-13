'''
flag: 65F98C02CAFCDF15782779FBA7C3C9E2
'''
import socket
import re
import sys
import logging
import asynchat
import asyncore
import custom_crypt

LOGGIN_FORMAT = u'%(name)-15s: %(levelname)-8s [%(asctime)s] %(message)s'

logging.basicConfig(format = LOGGIN_FORMAT, level = 0, filename = r'private/server.log')

console = logging.StreamHandler(sys.stdout)
console.setLevel(0)
console.setFormatter(logging.Formatter(LOGGIN_FORMAT))
logging.getLogger().addHandler(console)
 
class ScadaHandler(asynchat.async_chat):
    def __init__(self, sock, host_pool, host):
        asynchat.async_chat.__init__(self, sock=sock)
        
        self.host_pool = host_pool
        self.host = host
        self.logger = logging.getLogger(host)
        
        self.set_terminator('\n')        
        self.buffer = ''
        
        self.host_pool.add(self.host)
        self.logger.info('Connected')
        
        self.Send('Welcome to python SCADA server')
 
    def collect_incoming_data(self, data):
        self.buffer += data
        
    def Send(self,data):
        self.push(data + '\r\n')
        self.logger.info('>> ' + repr(data))
 
    def found_terminator(self):
        data = self.buffer
        self.buffer = ''    
        self.logger.info('<< ' + repr(data))
        m = re.match('\s*(login|get|version|help|exit)(?:\s+(.+))?',data,re.I)
        if not m:
            self.Send('Unknown command: ' + data)
            return
        
        cmd,extra = m.groups()
        if 'login' == cmd:
            m = extra and re.match('(\S+)\s+(\S+)',extra,re.I)
            if m:
                if custom_crypt.calc_hash(0,':'.join(m.groups())) == 0xC84E20E52E25E5E8:
                    with open(r'private/flag_ki_ctf_2016_telnet.txt','r') as f:
                        self.Send(f.read())
                else:
                    self.Send('Login failed')                
            else:
                self.Send('Login (and/or) password missed')
        elif 'get' == cmd:
            m = extra and re.match('([a-zA-Z0-9._ -]+)',extra,re.I)
            if m:            
                with open(m.group(1),'r') as f:
                    self.Send(f.read())
            else:
                self.Send('Filename missed')
        elif 'version' == cmd:
            self.Send('V1.1')
        elif 'help' == cmd:
            self.Send('No help, sorry')
        elif 'exit' == cmd:
            self.Send('Bye')
            self.handle_close()

    def handle_error(self):
        (type, value, traceback) = sys.exc_info()        
        self.Send(str(value))

    def handle_close(self):
        self.host_pool.remove(self.host)
        self.logger.info('Disconnected')
        asynchat.async_chat.handle_close(self)
 
class ScadaServer(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', 1337))
        self.listen(5)
        self.host_pool = set()
 
    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, (host,port) = pair
            logger = logging.getLogger(host)
            if len(self.host_pool) > 0x200:
                logger.error('Too many connections')
                sock.close()
            elif host in self.host_pool:
                logger.error('The host is already connected')
                sock.close()
            else:
                ScadaHandler(sock,self.host_pool,host)
                
if __name__=='__main__':
    server = ScadaServer()    
    asyncore.loop()
