from repositories.client_repository import ClientRepository
from repositories.user_repository import UserRepository
from repositories.billing_repository import BillingRepository
from repositories.address_repository import AddressRepository
from repositories.category_repository import CategoryRepository
from repositories.meter_repository import MeterRepository



class adminPageBack:
    def fetch_clients(self):
        client_repository = ClientRepository()
        return client_repository.get_all_clients()

    def fetch_users(self):
        user_repository = UserRepository()
        return user_repository.get_all_employee()
    
    def fetch_user_by_id(self, user_id):
        user_repository = UserRepository()
        return user_repository.get_user_by_id(user_id)
    
    def fetch_billing(self):
        billing_repository = BillingRepository()
        return billing_repository.get_all_billing()
    
    def add_billing(self, billing_data):
        billing_repository = BillingRepository()
        return billing_repository.create_billing(billing_data)#adjusta ang imo billing repo kay ang akong gipasa dictionary nalang 
                                                             #or if mas dalian ka usba ang akoa bungkaga and dictionary ig pasa(taas na kaayong code)
    

    def fetch_client_by_id(self, client_id):
        client_repository = ClientRepository()
        return client_repository.get_client_by_id(client_id)
    
    def add_client(self, client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status):
        client_repository = ClientRepository()
        return client_repository.create_client(client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status)


    def fetch_categories(self):
        category_repository = CategoryRepository()
        return category_repository.get_category()
    
    def fetch_address(self):
        address_repository = AddressRepository()
        return address_repository.get_address()
    
    def add_reading(self, meter_id, prev_read, pres_read, read_date):
        #paimportn lng kos repo
        return # wala pay function, e implement sa repository
    
    #meters
    def add_meter(self, meter_last_reading, serial_number):
        meter_repository = MeterRepository()
        return meter_repository.create_meter(meter_last_reading, serial_number)
    
    def fetch_meter_by_id(self, meter_id):
        meter_repository = MeterRepository()
        return meter_repository.get_meter_by_id(meter_id)
    
    def update_meter_latest_reading(self, meter_id, meter_last_reading, last_reading_date):
        meter_repository = MeterRepository()
        return # wala pay function, e implement sa repository
    
    def fetch_rate_blocks_by_categ(self, categ_id):
        #butngi lang pd logic ari than base lang sa taas para testing
        return #aa
    
    