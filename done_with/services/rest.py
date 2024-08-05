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
    items=frappe.db.get_all("List Item",filters={"status":"Available"},fields={"*"})
    if items:
        for item in items:
            existing_item=frappe.db.get_all("Listed Product",{"name":item.name},{'name','item_name'})
            if existing_item:
                listedItem=frappe.get_doc("Listed Product",existing_item[0].name)
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
                    "doctype": "Listed Product",
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
def add_seller(item_name):
    seller=frappe.db.get_all("Listed Item",{"name":item_name},{"seller_id"})
    seller_id=seller[0].seller_id
    return seller_id


@frappe.whitelist(allow_guest=True)
def received_bids():
    offers=frappe.db.get_all("Offer Request",{},{'item','price_offer','bidder_email','contact','additional_contact','seller'})
    if offers:
        for offer in offers:
            item_sellers=frappe.db.get_all('List Item',{'name':offer.item},{'item_name','seller_id'})
            item_seller=item_sellers[0]
            bid_name=offer.name
            existing_bid=frappe.db.get_all("Received Bid",{"bid_name":offer.name},{"name","item_id",'bidder_email','bidder_offer'})
            if existing_bid:
                bid=frappe.get_doc("Received Bid",offer.name)
                bid.bid_name=bid_name             
                bid.save(ignore_permissions=True)
            else:
                bid=frappe.get_doc({
                    "doctype": "Received Bid",
                    "bid_name":bid_name,
                    "parent": item_seller.seller_id,
                    "parenttype":'Trader',
                    "bidder_offer":offer.price_offer,
                    "item_id":item_seller.get('item_name')
                })
                bid.insert(ignore_permissions=True)
            frappe.db.commit()
    return  frappe.db.get_all("Received Bid",{},{"name"})
        











                # parent=parent[0].seller_id
                # existing_bid=frappe.db.get_all("Received Bid",{"bid_name":offer.name},{"name","item_id"})
                # if existing_bid:
                #     bid=frappe.get_doc("Received Bid",offer.name)
                #     bid.parent=parent
                #     bid.seller_id=parent
                #     bid.item_id=offer.item
                #     bid.bidder=offer.bidder_email
                #     bid.save(ignore_permissions=True)
                # else:

                #         bid=frappe.get_doc({
                #             "doctype": "Received Bid",
                #             "parent":parent,
                #             "bid_name":offer.name,
                #             "parenttype":"Trader",
                #             "seller_id":parent,
                #             "item_id":offer.item,
                #             "price_offer":offer.price_offer,
                #             "customer":offer.bidder_email
                            
                #         })
                #         bid.insert(ignore_permissions=True)
                # frappe.db.commit()
        
                # return frappe.db.get_all("Received Bid",{},{"*"})




    # offers=frappe.db.get_all("Offer Request",{},{"*"})
    # if offers:
    #     for offer in offers:
    #         parent=frappe.db.get_all("Listed Item",{'item_id':offer.item},{'seller_id'})
    #         parent=parent[0].seller_id
    #         existing_bid=frappe.db.get_all("Received Bid",{"bid_name":offer.name},{"name","item_id"})
    #         if existing_bid:
    #             bid=frappe.get_doc("Received Bid",offer.name)
    #             bid.parent=parent
    #             bid.seller_id=parent
    #             bid.item_id=offer.item
    #             bid.bidder=offer.bidder_email
    #             bid.save(ignore_permissions=True)
    #         else:
    #                 bid=frappe.get_doc({
    #                     "doctype": "Received Bid",
    #                     "parent":parent,
    #                     "bid_name":offer.name,
    #                     "parenttype":"Trader",
    #                     "seller_id":parent,
    #                     "item_id":offer.item,
    #                     "price_offer":offer.price_offer,
    #                     "customer":offer.bidder_email
                        
    #                 })
    #                 bid.insert(ignore_permissions=True)
    #         frappe.db.commit()
       
    #     return 'success'



# @frappe.whitelist(allow_guest=True)
# def received_bids():
#     try:
#         offers = frappe.db.get_all("Offer Request", filters={}, fields=["name", "item", "price_offer", "bidder_email", "contact", "additional_contact", "seller"])
        
#         if offers:
#             for offer in offers:
#                 existing_bid = frappe.db.get_value("Received Bid", {"name": offer.name}, ["name", "item_id"])
#                 parent=offer.seller:
#                 if parent:
#                     if existing_bid:
#                         bid = frappe.get_doc("Received Bid", existing_bid)
#                         bid.parent = offer.seller
#                         bid.parenttype = "Trader"
#                         bid.seller_id = offer.seller
#                         bid.item_id = offer.item
#                         bid.bidder = offer.bidder_email
#                         bid.save()
#                     else:
#                         bid = frappe.get_doc({
#                             "doctype": "Received Bid",
#                             "name": offer.name,
#                             "parent": offer.seller,
#                             "parenttype": "Trader",
#                             "seller_id": offer.seller,
#                             "item_id": offer.item,
#                             "bidder": offer.bidder_email,
#                         })
#                         bid.insert()
#             return "success"
#         else:
#             return "No offers found."

#     except Exception as e:
#         frappe.log_error(f"Error in received_bids: {str(e)}")
#         return "Error occurred while processing received bids."




'''frappe.ui.form.on('Gym Member', {
    
  
    email: function (frm) {
        let email = frm.doc.email;
     
        frappe.call({
            method: 'classic_gym.services.rest.check_email',
            args: {
                'email': email
            },
            callback: function (r) {

                
                if (r.message) {
                    frappe.msgprint('This email already exists.');
                    frappe.validate = false;
                }
                else {
                    frappe.validate = true;
                }
            }
        });
    },
    validate: function (frm) {
        let dateOfBirth=frm.doc.date_of_birth;
        let email=frm.doc.email;
        let full_name=frm.doc.full_name;
        let contact=frm.doc.contact
        let membership_type=frm.doc.membership_type || null
        frappe.call({
            method: 'classic_gym.classic_gym.doctype.gym_member.gym_member.customerInvoice',
            args: {
                'full_name':full_name,
                'email':email,
                'contact':contact,
                'membership_type':membership_type
            },
            callback: function (r) {
            }
        });


        
refresh: function (frm) {
            let member_ship_cost = frm.doc.membership_cost || 0;
            let subscribed_workout_cost = frm.doc.subscribed_work_out_cost || 0;
            let locker_charges = frm.doc.locker_charges || 0;
            let email=frm.doc.email;
    
            frappe.call({
                method: 'classic_gym.services.rest.totalCharges',
                args: {
                    "member_ship_cost": member_ship_cost,
                    "subscribed_workout_cost": subscribed_workout_cost,
                    "locker_charges": locker_charges
                },
                callback: function (r) {
                    if (r.message) {
                        frm.set_value('price_total', r.message);
                    } else {
                        console.error("Error: No total charges received from server.");
                    }
                },
                error: function (err) {
                //    console.error("Error calling totalCharges function:", err);
                }
            });
           
            
        },
    });
        '''