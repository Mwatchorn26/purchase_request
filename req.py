# -*- coding: utf-8 -*-
##############################################################################
#
#    Transformix Engineering Inc.
#    Copyright (C) 2015  (<http://www.transformix.com>).
#
#    Copyright (C) 2009 Almacom (Thailand) Ltd.#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

#from openerp.osv import osv
#from openerp import models, fields, api
#import openerp.addons.decimal_precision as dp


from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp


import time
from mx import DateTime
import datetime
import openerp.netsvc
from openerp.tools.translate import _

class purchase_request(models.Model):
    _name="purchase.request"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

#    @api.model
#    def copy(self, default=None):
#        if not default:
#            default = {}
#        default.update({
#            "state": "draft",
#            "pickings": [],
#            "name": "/" ,
#        })
#        return super(purchase_request, self).copy(default)
#
    @api.multi
    def _get_required_date(self,name,args):
        print "_get_required_date"
        vals={}
        for pr in self.browse(self.ids):
            vals[pr.id]=pr.lines and min([line.required_date for line in pr.lines]) or False
        return vals

    @api.multi
    def _set_required_date(self,value):
        print "_set_required_date",ids
#         if not value:
#             return False
# #         if type(ids)!=type([]):
# #             ids=[ids]
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 line.write({"required_date":value})
        return True

    @api.multi
    def _get_po_ids(self):
        vals={}
        for pr in self.browse(self.ids):
            po_ids=set([])
            for line in pr.lines:
                if line.po_id:
                    po_ids.add(line.po_id.id)
            vals[pr.id]=sorted(po_ids)
        return vals

    name = fields.Char("Doc NO",size=64,select=1, readonly=1, default=lambda obj, cr, uid, context: '/')
    #use built-in create_date 
    #create_date #date = fields.Date("Created", readonly=1, select=1,lambda *a: time.strftime("%Y-%m-%d"))
    required_date = fields.Date(compute='_get_required_date',fnct_inv='_set_required_date',method=True,type="date",string="Required Date")
    origin =fields.Char("Origin",size=16,select=2,readonly=1, states={'draft':[('readonly',False)]} )
    ship_type = fields.Selection([("sea","Sea"),("air","Air"),('truck','Trucking')],"Shipping Type",readonly=1,states={'draft':[('readonly',False)]})
    requester_id = fields.Many2one("res.users","Requested By",readonly=True, default=lambda self: self.env.user)
    #department_id = fields.Many2one("hr.department","Department",readonly=True,default='_get_department')
    notes = fields.Text("Notes")
    lines = fields.One2many("purchase.request.line","pr_id","Lines" , readonly=True,states={'draft':[('readonly',False)],'approved':[('readonly',False)]})
    state = fields.Selection([("draft","Draft"),("wait_approval","Waiting for Approval"),
                                ("approved","Approved"),
                                ("rejected","Rejected"),("ordered","Ordered"),
                                ("received","Received"),('done','Done'),("cancelled","Cancelled")],"Status",readonly=True,select=1, default= lambda *a: 'draft')
    #location_id = fields.Many2one("stock.location","Location",required=True, default='_get_location')
    po_ids = fields.Many2many(compute='_get_po_ids', comodel_name="purchase.order", string="Purchase Orders")
    
    #see hr_expense.py for source of this copy & paste
#    amount          = fields.Function(_amount, string='Total Amount', digits_compute=dp.get_precision('Account'), 
#                                      store={
#                'purchase.request.line': (_get_cost_from_line, ['unit_amount','unit_quantity'], 10)
#                #see hr_expense.py for source of this copy & paste
#            }),
    currency_id     = fields.Many2one('res.currency', 'Currency', required=True, readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)]}),
    
    #_order="id desc"

#    @api.model
#    def _get_department(self):
#        cr.execute("select department_id from hr_department_user_rel where user_id=%d"%uid)
#        res=cr.fetchone()
#        if not res:
#            return False
#        return res[0]

#    @api.model
#    def _get_location(self):
#        res=self.pool.get("stock.warehouse").search(cr,uid,[])
#        if not res:
#            return False
#        wh_id=res[0]
#        wh=self.pool.get("stock.warehouse").browse(wh_id)
#        return wh.lot_stock_id.id

##    _defaults={
##        'name': lambda obj, cr, uid, context: '/',
##        "date": lambda *a: time.strftime("%Y-%m-%d"),
##        "requester_id": lambda self,cr,uid,context: uid,
##        "department_id": _get_department,
##        "location_id": _get_location,
##        "state": lambda *a: "draft",
##    }

#     @api.multi
#     def wkf_draft(self):
#         print "wkf_draft",ids
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 line.write({"state":"draft"})
#             pr.write({"state":"draft"})
#         return True
# 
#     def wkf_wait_approval(self,cr,uid,ids,context={}):
#         print "wkf_submit_head",ids
#         self.write(cr,uid,ids,{'state':"wait_head"})
#         for pr in self.browse(self.ids):
#             if not pr.lines:
#                 raise osv.except_osv("Error","Can't send empty request")
#             for line in pr.lines:
#                 if not line.qty:
#                     raise osv.except_osv("Error","Can't request zero quantity")
#         for pr in self.browse(self.ids):
#             if "PR" not in pr.name or pr.name=='/':
#                 pr.write({'name': self.pool.get('ir.sequence').get(cr, uid, 'purchase.request')})
#             for line in pr.lines:
#                 if line.state in ("draft"):
#                     line.write({"state":"wait_head"})
#         return True
# 
#     @api.multi
#     def wkf_wait_warehouse(self,cr,uid,ids,context={}):
#         """
#             - Submit to warehouse manager
#         """
#         print "wkf_submit_warehouse"
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 if line.state in ("wait_head"):
#                     line.write({"state":"wait_warehouse"})
#             pr.write({"state":"wait_warehouse"})
#         return True
# 
#     @api.multi
#     def wkf_rejected(self,cr,uid,ids,context={}):
#         print "wkf_rejected",ids
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 if line.state in ("approved","wait_head","wait_warehouse"):
#                     line.write({"state":"rejected"})
#             pr.write({"state":"rejected"})
#         return True
# 
#     @api.multi
#     def wkf_approved(self,cr,uid,ids,context={}):
#         """
#             - approved by warehouse manager
#         """
#         print "wkf_approved",ids
#         for pr in self.browse(self.ids):
#             moves=[]
#             for line in pr.lines:
#                 if line.state in ("wait_warehouse"):
#                     line.write({"state":"approved"})
#             pr.write({"state":"approved"})
#         return True
# 
#     @api.multi
#     def button_make_po(self,cr,uid,ids,context={}):
#         """
#         - TO be used make purchase request
#         """
#         print "button_make_po",ids
# 
#         line_ids=[]
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 line_ids.append(line.id)
#         self.pool.get("purchase.request.line").make_po(cr,uid,line_ids)
#         return True
# 
# #    @api.multi
# #    def test_state(self,cr,uid,ids,mode,context={}):
# #        print "test_state",ids,mode
# #        all_ordered=True
# #        all_received=True
# #        for pr in self.browse(self.ids):
# #            for line in pr.lines:
# #                if line.state=="disapproved":
# #                    continue
# #                if not line.state=="received":
# #                    all_received=False
# #                if not line.state=="ordered":
# #                    all_ordered=False
# #        if mode=="ordered":
# #            res=all_ordered
# #        elif mode=="received":
# #            res=all_received
# #        print "res",res
# #        return res
# #
# 
#     @api.multi
#     def credentials_to_approve(self,cr,uid,ids,mode,context={}):
#         print "Credentials To Approve ",ids,mode
#         all_ordered=True
#         all_received=True
#         for pr in self.browse(self.ids):
#             for line in pr.lines:
#                 if line.state=="disapproved":
#                     continue
#                 if not line.state=="received":
#                     all_received=False
#                 if not line.state=="ordered":
#                     all_ordered=False
#         if mode=="ordered":
#             res=all_ordered
#         elif mode=="received":
#             res=all_received
#         print "res",res
#         return res
# 
# 
# 
# #    @api.multi
# #    def wkf_ordered(self,cr,uid,ids,context={}):
# #        print "wkf_ordered",ids
# #        for pr in self.browse(self.ids):
# #            pr.write({"state":"ordered"})
# #        return True
# #
# #    @api.multi
# #    def wkf_received(self,cr,uid,ids,context={}):
# #        print "wkf_received",ids
# #        for pr in self.browse(self.ids):
# #            pr.write({"state":"received"})
# #        return True
# #
# #    @api.multi
# #    def wkf_cancelled(self,cr,uid,ids,context={}):
# #        print "wkf_cancel", ids
# #        for pr in self.browse(self.ids):
# #            for po in pr.orders:
# #                if po.state!="cancel":
# #                    raise osv.except_osv(_("Error"),_("Purchase orders for this request have to be cancelled first"))
# #            for line in pr.lines:
# #                line.write({"state":"cancelled"})
# #            pr.write({"state":"cancelled"})
# #        return True
# ##purchase_request()

class purchase_request_line(models.Model):
    _name="purchase.request.line"
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    def name_get(self):
        return [(line.id,"%s: %s"%(line.pr_id.name,line.name)) for line in self.browse(self.ids)]

    pr_id           = fields.Many2one("purchase.request", "Request",ondelete="cascade",select=1)
    name            = fields.Char("Name",size=64,required=True,select=1 ,readonly=1, states={'draft':[('readonly',False)]} )
    description     = fields.Char("Description",size=256,required=True, readonly=1, states={'draft':[('readonly',False)]} )
    product_id      = fields.Many2one("product.product","Product", readonly=1, states={'draft':[('readonly',False)],'approved':[('readonly',False)]} )
    product_number  = fields.Char("Product Number",size=64,required=True ,readonly=1, states={'draft':[('readonly',False)]} )
    product_name    = fields.Char("Product Name",size=64,required=True ,readonly=1, states={'draft':[('readonly',False)]} )
    supplier_id     = fields.Many2one("res.partner","Supplier", select=1,domain=[("supplier","=",True)])
    mfg_name        = fields.Char("Manufacturer",size=64,required=True, readonly=1, states={'draft':[('readonly',False)]} )
    mfg_id          = fields.Many2one("res.partner", "Manufacturer", select=1, domain=[("supplier","=",True)])
    mfg_prod_number = fields.Char("Manufacturer Product Number",size=64,required=True,readonly=1, states={'draft':[('readonly',False)]} )
    mfg_prod_name   = fields.Char("Manufacturer Product Name",size=64,required=True ,readonly=1, states={'draft':[('readonly',False)]} )
    qty             = fields.Float("Quantity",required=True,readonly=1, states={'draft':[('readonly',False)]} )
    uom_id          = fields.Many2one("product.uom","UoM",required=True ,readonly=1, states={'draft':[('readonly',False)]} )
    po_id           = fields.Many2one("purchase.order","Purchase Order")
    required_date   = fields.Date("Required Date",required=True , readonly=1, states={'draft':[('readonly',False)]}, default=lambda *a: time.strftime("%Y-%m-%d"))
    '''
    next_date = (datetime.strptime(date_ref, '%Y-%m-%d') + relativedelta(days=line.days))
    '''
    notes           = fields.Text("Note")
    state           = fields.Selection([("draft","Draft"),("wait_head","Wait Head for Approval"),("wait_warehouse","Wait Warehouse for Approval"),
                           ("approved","Approved"),("rejected","Rejected"),("ordered","Ordered"),
                           ("received","Received"),("cancelled","Cancelled")],"Status",readonly=True,select=1, default=lambda *a: "draft")
    sequence        = fields.Integer("Sequence" ,readonly=1, states={'draft':[('readonly',False)]}, default=lambda *a: 1 )
    reserv_id       = fields.Many2one("stock.move","Reservation")
    account         = fields.Text("Project Account")
#    analytic_account= fields.Many2one('account.analytic.account','Analytic account')
#    total_amount    = fields.Function(_amount, string='Total', digits_compute=dp.get_precision('Account'))
    unit_amount     = fields.Float('Unit Price', digits_compute=dp.get_precision('Account'))
    #_order="name"


#    _defaults={
#        "state": lambda *a: "draft",
#        "required_date": lambda *a: time.strftime("%Y-%m-%d"),
#        "sequence": lambda *a: 1,
#    }

#     #stolen from hr_expense.py:
#     def _amount(self, cr, uid, ids, field_name, arg, context=None):
#         if not ids:
#             return {}
#         cr.execute("SELECT l.id,COALESCE(SUM(l.unit_amount*l.qty),0) AS amount FROM purchase_request_line l WHERE id IN %s GROUP BY l.id ",(tuple(ids),))
#         res = dict(cr.fetchall())
#         return res
# 
#     @api.multi
#     def onchange_product(self, product_id, supplier_id, state):
#         print "onchange_product"
#         if state=='approved':
#             return {}
#         if not product_id:
#             return {"value":{"name":False,"uom_id":False,"qty":False,"supplier_id":False}}
#         prod=self.pool.get("product.product").browse(product_id)
#         uom_id=prod.uom_id.id
#         qty=0.0
#         supplier_id=prod.seller_ids and prod.seller_ids[0].name.id or False
#         vals={
#             "name": "[%s]:%s %s"%(prod.default_code,prod.name ,prod.variants or ""),
#             "uom_id": uom_id,
#             "qty": qty if qty not in (0.0,1.0) else False,
#             "supplier_id": supplier_id,
#         }
#         print "vals",vals
#         return {"value": vals}
# 
#     @api.one
#     def button_reject(self,cr,uid,ids,context={}):
#         #print "button_reject",ids
#         #for line in self.browse(cr,uid,ids):
#         line.write({"state":"rejected"})
#         #return True
# 
#     @api.multi
#     def make_po(self):
#         user=self.env("res.users").browse(self.env.user)
#         company=user.company_id
#         group_lines={}
#         origins={}
#         for line in self.browse(self.ids):
#             if line.state!="approved":
#                 continue
#             pr=line.pr_id
#             if not line.supplier_id:
#                 raise osv.except_osv("Error","Missing supplier")
#             if not line.product_id:
#                 raise osv.except_osv("Error","Missing product")
#             k=(line.supplier_id.id,line.pr_id.location_id.id,line.product_id.id,line.name,line.uom_id.id)
#             group_lines.setdefault(k,[]).append(line.id)
#             origins.setdefault(k[:2],set([])).add(line.pr_id.name)
#         po_ids={}
#         print "origins",origins
#         for (supp_id,loc_id,prod_id,name,uom_id),line_ids in group_lines.items():
#             qty=0.0
#             for line in self.browse(line_ids):
#                 qty+=line.qty
#             print "supp_id:",supp_id,"prod_id:",prod_id,"qty:",qty
#             k=(supp_id,loc_id)
#             po_id=po_ids.get(k)
#             origin=",".join(sorted(origins[k]))
#             if not po_id:
#                 vals={
#                     "partner_id": supp_id,
#                     "location_id": loc_id,
#                     "origin": origin,
#                 }
#                 po_id=self.pool.get("purchase.order").create(cr,uid,vals,context={"partner_id":supp_id})
#                 po_ids[k]=po_id
#             supp=self.env("res.partner").browse(supp_id)
#             prod=self.env("product.product").browse(prod_id)
#             pl=supp.property_product_pricelist_purchase
#             price=pl.price_get(prod_id,qty,supp_id,{"uom": uom_id})[pl.id]
#             line={
#                 "order_id": po_id,
#                 "product_id": prod_id,
#                 "product_qty": qty,
#                 "product_uom": uom_id,
#                 "name": name,
#                 "price_unit": price,
#                 "date_planned": time.strftime("%Y-%m-%d"),
#             }
#             taxes_ids = prod.product_tmpl_id.supplier_taxes_id
#             taxes = self.pool.get('account.fiscal.position').map_tax(self.env.cr, self.env.user, supp.property_account_position, taxes_ids)
#             line.update({
#                 'taxes_id':[(6,0,taxes)]
#             })
#             self.env("purchase.order.line").create(line)
#             self.with_context(po_id=po_id).write(line_ids)
#         return po_ids.values()
# 
#     @api.multi
#     def update_state(self):
#         print "Purchase request line update state",ids
#         pr_ids=set([])
#         for line in self.browse(self.ids):
#             if line.po_id:
#                 if line.po_id.shipped:
#                     new_state="received"
#                 else:
#                     new_state="ordered"
#                 if new_state!=line.state:
#                     line.write({"state":new_state})
#                     pr_ids.add(line.pr_id.id)
#         wfs=netsvc.LocalService("workflow")
#         for pr_id in pr_ids:
#             wfs.trg_write(self.env.user,"purchase.request",pr_id,self.env.cr)
#         return True
# 
#     @api.model
#     def copy_data(self, default=None):
#         """Avoid duplicate lines"""
#         if not default:
#             default = {}
#         default.update({'state':'draft', 'move_lines':[], 'po_id':[]})
#         return super(purchase_request_line, self).copy_data(default)
# 
#     @api.multi
#     def write(self,vals):
#         res=super(purchase_request_line,self).write(vals)
#         #if type(self.ids)!=type([]):
#         #    ids=[self.ids]
#         self.update_state()
#         return res
# #purchase_request_line()

 
class purchase_request_authorization(models.Model):
    '''
        This is holds the collection of authorization limits
    '''
    _inherit = 'purchase.config.settings'
     
    po_auth_base_limit = fields.Float(string='Base Limit', default=250, help="This is the default purchase request limit PER LINE ITEM for each employee")
    po_auth_limit_ids = fields.One2many("purchase.request.auth.limit", "po_auth_id", help="The list of people with authority, and the amount they can authorize.")

class purchase_request_auth_limit(models.Model):
    '''
        This is an item in the list of people who can authorize more than the base limit on Purchase Order Requests
    '''
    _name='purchase.request.auth.limit'
 
    po_auth_id = fields.Many2one("purchase.config.settings", delegate=True)
    authority_id = fields.Many2one("res.users","Authority", help="This is a person who can authorize more than the base limit.")
    po_auth_limit = fields.Float("Authorization Limit", default=500, help="The amount the person can authorize.")
         
 
class purchase_order(models.Model):
    _inherit="purchase.order"
    pr_lines = fields.One2many("purchase.request.line","po_id","Purchase Request Lines",readonly=True)
 
    @api.multi
    def write(self,vals):
        res=super(purchase_order,self).write(self.env.cr,self.env.user,self.ids,vals,self.env.context)
        #if type(self.ids)!=type([]):
        #    ids=[self.ids]
        pr_line_ids=set([])
        for po in self.browse(self.ids):
            for pr_line in po.pr_lines:
                pr_line_ids.add(pr_line.id)
        pr_line_ids=list(pr_line_ids)
        self.env("purchase.request.line").update_state(self.env.cr,self.env.user,pr_line_ids)
        return res
#purchase_order()
 
class mrp_procurement(models.Model):
    _inherit="procurement.order"
    pr_id = fields.Many2one("purchase.request","Purchase Request")
 
#     @api.multi
#     def make_pr(self):
#         purchase_id = False
#         company = self.env('res.users').browse(self.ids).company_id
#         for procurement in self.browse(self.ids):
#             res_id = procurement.move_id.id
#             partner = procurement.product_id.seller_ids[0].name
#             partner_id = partner.id
#             address_id = self.env('res.partner').address_get(self.env.cr, self.env.user, [partner_id], ['delivery'])['delivery']
#             pricelist_id = partner.property_product_pricelist_purchase.id
# 
#             uom_id = procurement.product_id.uom_po_id.id
# 
#             qty = self.env('product.uom')._compute_qty(self.env.cr, self.env.user, procurement.product_uom.id, procurement.product_qty, uom_id)
#             if procurement.product_id.seller_ids[0].qty:
#                 qty=max(qty,procurement.product_id.seller_ids[0].qty)
# 
#             price = self.env('product.pricelist').price_get(self.env.cr, self.env.user, [pricelist_id], procurement.product_id.id, qty, False, {'uom': uom_id})[pricelist_id]
# 
#             #Passing partner_id to context for purchase order line integrity of Line name
#             context.update({'lang':partner.lang, 'partner_id':partner_id})
# 
#             product=self.env('product.product').browse(procurement.product_id.id)
# 
#             line={
#                 'name': product.name,
#                 'qty': qty,
#                 'product_id': procurement.product_id.id,
#                 'uom_id': uom_id,
#                 'reserv_id': res_id,
#             }
# 
#             vals = {
#                 'origin': procurement.origin,
#                 'supplier_id': partner_id,
#                 'location_id': procurement.location_id.id,
#                 "lines": [(0,0,line)],
#                 'notes':product.description_purchase,
#             }
#             pr_id=self.env("purchase.request").create(self.env.cr,self.env.user,vals)
# 
#             self.write(self.env.cr, self.env.user, [procurement.id], {'state':'running', 'pr_id':pr_id})
# #mrp_procurement()
