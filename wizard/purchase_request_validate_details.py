# -*- coding: utf-8 -*-
##############################################################################
#
#    Transformix Engineering Inc.
#    Copyright (C) 2015  (<http://www.transformix.com>).
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
import time

#from openerp.osv import fields, osv, models

from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp

#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#! ! ! 
#! ! ! 
#! ! ! NOTE: THIS CODE IS NOT INCLUDED IN THE DATA OR UPDATES XML __OPENERP__.PY FILE! ! ! 
#! ! ! 
#! ! ! 
#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 
#! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! 


class purchase_request_validate_details(models.TransientModel):
    ''' Opportunity for Purchasing Manager to correct purchase request details:
            - Create new part [if necessary],
            - Assign actual Analytic Account, 
            - Change to Preferred Supplier, 
            - Change price for preferred pricing...)
    '''
    _name = 'purchase.request.validate.details'
    _description = '''Opportunity for Purchasing Manager to correct purchase request details (assign actual Analytic Account, 
                      Change to preferred supplier, Change price for preferred pricing...)'''
    pr_id           = fields.Many2one("purchase.request","Request",ondelete="cascade",select=1)
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
    notes           = fields.Text("Note")
    #state           = fields.Selection([("draft","Draft"),("wait_head","Wait Head for Approval"),("wait_warehouse","Wait Warehouse for Approval"),
    #                       ("approved","Approved"),("rejected","Rejected"),("ordered","Ordered"),
    #                       ("received","Received"),("cancelled","Cancelled")],"Status",readonly=True,select=1, default=lambda *a: "draft")
    #sequence        = fields.Integer("Sequence" ,readonly=1, states={'draft':[('readonly',False)]}, default=lambda *a: 1 )
    #reserv_id       = fields.Many2one("stock.move","Reservation")
    account         = fields.Text("Project Account") #To be Analytic Account in future version.
    analytic_account= fields.Many2one('account.analytic.account','Analytic account')
    total_amount    = fields.Float(compute='_amount', string='Total', digits_compute=dp.get_precision('Account'))
    unit_amount     = fields.Float('Unit Price', digits_compute=dp.get_precision('Account'))

    def _amount(self):
        return 1

#     _defaults = {
#          'date_from': lambda *a: time.strftime('%Y-%m-01'),
#          'holiday_type': 'Approved',
#     }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
