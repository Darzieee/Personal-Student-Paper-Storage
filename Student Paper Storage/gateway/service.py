import json
from nameko.web.handlers import http
from werkzeug.wrappers import Response

import requests
import uuid

from nameko.rpc import RpcProxy

from gateway.dependencies.session import SessionProvider
from gateway.dependencies.dependencies import Database,DatabaseWrapper

class Service:
    name = "gatewayServices"
    
    rpc = RpcProxy('userServices')

    session_provider = SessionProvider()
    
    #register
    @http('POST', '/register')
    def register(self, request):
        data_register = request.json
        response = self.rpc.add_user(data_register['nrp'],data_register['name'],data_register['email'],data_register['password'])
        
        return response
    
    #login
    @http('POST', '/login')
    def login(self, request):
        data_login = request.json
        
        data = self.rpc.get_user(data_login['email'],data_login['password'])
        
        if data and len(data)>0 :
            data=data[0]
            session_id = self.session_provider.set_session(data)
            data['session_id']=session_id
            response = Response(str(data))
            response.set_cookie('SESSID', session_id)
            return response
        else :
            response = Response("Login Failed")
            return response
    
    @http('GET', '/checkUser')
    def check(self,request) :
        cookies = request.cookies
        if cookies:
            print("Check User "+cookies["SESSID"])
            data_session = self.session_provider.get_session(str(cookies['SESSID']))   
            return str(data_session)
        else :
            return None
        
    @http('POST', '/logout')
    def logout(self, request):
        cookies = request.cookies
        
        if cookies:
            data_session = self.session_provider.delete_session(cookies['SESSID'])
            
            response = Response('Logout')
            return response
        else:
            response = Response('Logout Failed')
            return response
    
    @http("POST", "/upload")
    def save_file(self, request):
        cookies = request.cookies
        data_session=None
        if cookies:
            print("Check User "+cookies["SESSID"])
            data_session = self.session_provider.get_session(str(cookies['SESSID']))  
            
        if (data_session!=None):
            for file in request.files.items():
                _, file_storage = file
                lowercase_str = uuid.uuid4().hex  
                fnameakhir=lowercase_str+file_storage.filename
                fname="upload/"+fnameakhir
                self.rpc.add_file(data_session['id'],fname)
                
                file_storage.save(f"{fname}")
            return json.dumps({"Recieved": True})
        else :
            return "Failed"
    
    
    @http('GET', "/download")
    def files(self,request): 
        url = "http://google.com/favicon.ico"
        r = requests.get(url, allow_redirects=True)
        
        open("google.ico", "wb").write(r.content)
        return r
    @http('GET', "/search")
    def search(self,request):  # pragma: no cover
        cookies = request.cookies
        data_session = None
        
        if cookies:
            print("checkuser "+cookies["SESSID"])
            data_session = self.session_provider.get_session(str(cookies['SESSID']))  
        
    
    
        
    
    