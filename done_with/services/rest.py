import frappe
from datetime import datetime, timedelta,time
from frappe.utils import now, getdate


class Trader():

    def __init__(self):
        self.membershipType = frappe.db.get_all('Gym Membership', {}, ['type','price','duration'])
        self.workoutPlans=frappe.db.get_all('Gym Work Out Plans', {}, ['plan_name','trainer','price'])
        self.lockerBookings=frappe.db.get_all('Gym Locker Booking',{}, ['email','total_price'])



class Item_on_Sale():
    def load(self,email):
        existing_traders=frappe.db.get_all('Trader',{"email":email},{"name","trader_name","trader_email"})
        if existing_traders:
            return existing_traders[0].name
        
@frappe.whitelist(allow_guest=True)
def list_item(email):
    today = datetime.now().date()
    return email,today