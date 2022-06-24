import gateway.dependencies.dependencies as dependencies

from nameko.rpc import rpc

class UserAccessService:

    name = 'userServices'

    database = dependencies.Database()

    @rpc
    def add_user(self, nrp, account, email, password):
        user = self.database.add_user(nrp,account, email,password)
        return user

    @rpc
    def get_user(self, email, password):
        user = self.database.get_user(email, password)
        return user
    
    @rpc
    def add_file(self, account, file):
        self.database.add_file(account, file)