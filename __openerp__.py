##############################################################################
#
#    Copyright (C) 2009 Almacom (Thailand) Ltd.
#	 Ported to V8 in 2014 by Transformix Engineering Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Purchase requests",
    "version" : "0.1",
    "depends" : ["base","hr","purchase","sale","mrp"],
    "author" : "Transformix Engineering Inc. and Almacom (Thailand) Ltd.",
    "website" : ["http://almacom.co.th/", "http://www.transformix.com"],
    "description": """
This module implements purchase requests.
Requests have to be approved, after which purchase orders can be created for the requested items.
    """,
    "init_xml" : [
    ],
    "demo_xml" : [
    ],
    "update_xml" : [
        "security/req_security.xml",
        "security/ir.model.access.csv",
        "req_data.xml",
        "req_view.xml",
        "req_workflow.xml",
    ],
    'active':False,
    "installable": True,
}
