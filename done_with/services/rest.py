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


@frappe.whitelist(allow_guest=True)
def listed_items():
    items=frappe.db.get_all("List Item",filters={"status":"Available"},fields={"name","item_name","parent","condition","price","seller_id","date_listed","category","status","about_item","image"})
    if items:
        for item in items:
            existing_item=frappe.db.get_all("Listed Item",{"name":item.name},{'name','item_name'})
            if existing_item:
                listedItem=frappe.get_doc("Listed Item",existing_item[0].name)
                listedItem.item_name=item.item_name
                listedItem.condition=item.condition #if item.condition else None
                listedItem.price=item.price# if item.price else None
                listedItem.date_listed=item.date_listed #if item.date_listed else None
                listedItem.seller_id=item.seller_id #if item.seller_id else None
                listedItem.category=item.category #if item.category else None
                listedItem.status=item.status #if item.status else None
                listedItem.about_item=item.about_item  #if item.about_item else None
                listedItem.image=item.image # if item.image #else None
                listedItem.save()
            else:
                listedItem=frappe.get_doc({
                    "doctype": "Listed Item",
                    "name":item.name,
                    "item_name":item.item_name,
                    "price":item.price,
                    "condition": item.condition,
                    "date_listed":item.date_listed,
                    "seller_id":item.seller_id,
                    "category":item.category,
                    "status":item.status,
                    "about_item":item.about_item,
                    "image":item.image

                })
                listedItem.insert()
            frappe.db.commit()


    return 

@frappe.whitelist(allow_guest=True)
def bidding_form(email,contact):
    return email,contact
@frappe.whitelist(allow_guest=True)
def check_bidder(email,item_name):
    bidder=frappe.db.get_all("Listed Item",{"name":item_name,"seller_id":email},{"seller_id"})
    if bidder and bidder[0].seller_id==email:
        check=1
    else: check=None

    return check


@frappe.whitelist(allow_guest=True)
def received_bids():
    offers=frappe.db.get_all("Offer Request",{},{"name","item","price_offer","bidder_email","contact","additional_contact"})
    if offers:
        for offer in offers:
            existing_bid=frappe.db.get_all("Received Bid",{"name":offer.name},{"name","item_id"})
    
            items=frappe.db.get_all("List Item",filters={"name":offer.item},fields={"item_name","parent","condition","price","seller_id","date_listed","category","status","about_item","image"})
            if existing_bid:
                bid=frappe.get_doc("Received Bid",existing_bid[0].name)
                bid.parent=items[0].parent
                bid.seller_id=items[0].parent
                bid.item_id=offer.item
                bid.bidder=offer.bidder_email
                bid.save()
            else:
                bid=frappe.get_doc({
                    "doctype": "Received Bid",
                    "name":offer.name,
                    "parent":items[0].parent,
                    "seller_id":items[0].parent,
                    "item_id":offer.item,
                    "bidder":offer.bidder_email,
                })
                bid.insert()
            frappe.db.commit()

    return "success"