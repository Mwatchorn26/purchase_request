from openerp import osv
import openerp.pooler

from openerp import models, api

view="""<?xml version="1.0"?>
<form string="Make PO">
    <label string="This will create purchase orders for the selected purchase request lines."/>
</form>
"""

class wiz_make_po(models.TransientModel):
    @api.one
    def _make_po(self,cr,uid,data,context):
        print "_make_po"
        pr_line_ids=data["ids"]
        pool=pooler.get_pool(cr.dbname)
        po_ids=self.env["purchase.request.line"].make_po(cr,uid,pr_line_ids)
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "domain": [("id","in",po_ids)],
            "view_type": "form",
            "view_mode": "tree,form",
            "name": "Purchase Orders",
        }

    states={
        "init": {
            "actions": [],
            "result": {
                "type": "form",
                "arch": view,
                "fields": {},
                "state": [("make_po","Confirm"),("end","Cancel")],
            },
        },
        "make_po": {
            "result": {
                "type": "action",
                "action": _make_po,
                "state": "end",
            }
        }
    }
wiz_make_po("make.po")