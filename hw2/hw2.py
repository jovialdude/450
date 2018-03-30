import logging
import socket
import sys
import ssl
import urllib.parse

def retrieve_url(url):
    """
    implement your client code here
    """
    parsed = urllib.parse.urlparse(url)
    scheme = parsed.scheme
    port = parsed.port
    host = parsed.netloc
    path = parsed.path
    
    if (scheme == 'http'):
        if path == '':
            request = 'GET / HTTP/1.1\r\nHost: ' + host +  "\r\nConnection: close"+ "\r\n\r\n"
        else:
            request = "GET " + path +" HTTP/1.1\r\nHost: " + host + "\r\nConnection: close"+ "\r\n\r\n"
        
        if port is None:
            try:
                s = socket.create_connection ((host, 80))
            except OSError:
                return None
        else:
            try:
                s = socket.create_connection ((host.split(':')[0], port))
            except OSError:
                return None
        
        request_as_bytes = bytearray (request, 'utf-8')
        
        s.send(request_as_bytes)
       
        ack_msg = s.recv(1024)
        data = ack_msg

        while True:
            if len(ack_msg) == 0:
                break
            ack_msg = s.recv(1024)
            data = data + ack_msg
            

    elif (scheme == 'https'):
        if path == '':
            request = 'GET / HTTP/1.1\r\nHost: ' + host +  "\r\nConnection: close"+ "\r\n\r\n"
        else:
            request = "GET " + path +" HTTP/1.1\r\nHost: " + host + "\r\nConnection: close"+ "\r\n\r\n"
        
        if port is None:
            try:
                context = ssl.create_default_context()
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                context.verify_mode = ssl.CERT_REQUIRED
                context.check_hostname = True
                context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")
                s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)

                s.connect ((host, 443))
            except OSError:
                return None
        else:
            try:
                context = ssl.create_default_context()
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                context.verify_mode = ssl.CERT_REQUIRED
                context.check_hostname = True
                context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")
                s = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)

                s.connect ((host, port))
            except OSError:
                return None
       
#            cert = s.getpeercert()
#            print (cert)
#            if not cert:
#                return None
        
#            print (cert['notAfter']);

        request_as_bytes = bytearray (request, 'utf-8')
        
        s.send(request_as_bytes)
       
        ack_msg = s.recv(1024)
        data = ack_msg

        while True:
            if len(ack_msg) == 0:
                break
            ack_msg = s.recv(1024)
            data = data + ack_msg


#start of data parsing
    status = data.partition(bytearray('\r\n\r\n', 'utf-8'))[0]
    data = data.partition(bytearray('\r\n\r\n', 'utf-8'))[2]#parse out header
    code = status.partition(bytearray('\r\n', 'utf-8'))[0]
    code = code.partition(b' ')[2]
    code = code.partition(b' ')[0]
   
   
    if (code == b'200'):
        try:
            #check if chunked encoded
            is_chunked = status.index(bytearray('chunked','utf-8'))
            
            #parsing body of data
            temp = data.partition(bytearray('\r\n0\r\n\r\n', 'utf-8'))[0]#parse footer, body is left, data = body
            temp = temp.partition(bytearray('\r\n', 'utf-8'))[2]#take out the first length
            temp = temp.partition(bytearray('\r\n', 'utf-8'))#take out the first length
            
            data = temp[0]
            temp = temp[2]
            count = 0 
            while (temp != b''):
                temp = temp.partition(bytearray('\r\n', 'utf-8'))
                if isinstance(temp[0], int):
                    continue
                data = data + temp[0]
                temp = temp[2]
        except ValueError:
            data = data
#data = data.partition(bytearray('\r\n\r\n', 'utf-8'))[2]
    elif (code == b'404'):
        return None
    return data
#print (retrieve_url ('http://www.example.com'))
#print (retrieve_url ('http://www.google.com'))
#print (retrieve_url('http://accc.uic.edu/contact'))
#retrieve_url('http://accc.uic.edu/contact')
#print(retrieve_url('https://www.google.com'))
#print (retrieve_url('http://www.google.com'))
#print (retrieve_url ('https://expired.badssl.com/'))
#print (retrieve_url ('https://www.example.com'))
print (retrieve_url ('http://i.imgur.com/fyxDric.jpg'))
