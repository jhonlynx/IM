from repositories.address_repository import AddressRepository

class AddressController:
    def __init__(self):
        self.address_repo = AddressRepository()

    def get_address(self):
        return self.address_repo.get_address()
    
    def create_address(self, address_name):
        return self.address_repo.create_address(address_name)

    