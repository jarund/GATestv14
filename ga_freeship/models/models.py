# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Adding fields to the res.partner to hold info for Vendor free shipping
class free_ship_vendor(models.Model):
    _inherit = 'res.partner'
    # Drop down for Selection field for types of Free Ship options
    # If new option added need to add to compute feld "_compute_free_ship_status" below also
    free_ship_rule = fields.Selection(selection=[('na', 'n/a'), ('m_cost', 'Min Cost'),
        ('m_qty', 'Min Quantity'), ('m_wght', 'Min Weight'), ('m_qty_cost_wght', 'Min Qty or Cost or Wght'),
        ('m_cost_wght', 'Min Cost or Wght'), ('m_cost_lines', 'Min Amount and Max Lines')], 
        default='na',track_visibility="onchange")
    # Values related to free ship options
    m_cost = fields.Float("Min Cost")
    m_qty = fields.Float("Min Quantity")
    m_wght = fields.Float("Min Weight")
    mx_line_cnt = fields.Integer("Max Line Count")


# Adding fields to the purchase.order to hold info for Vendor free shipping
class free_ship_po(models.Model):
    _inherit = 'purchase.order'
    # Calculation if Free Ship Status
    #@api.multi
    @api.depends('ship_rule', 'm_cost', 'm_qty', 'm_wght', 'amount_total', 'mx_line_cnt')
    def _compute_free_ship_status(self):
        for rec in self:
            # n/a
            if rec.ship_rule == 'na':
                rec.free_ship_status = 'n/a'
            elif rec.ship_rule == 'm_cost':
                if rec.amount_total >= rec.m_cost:
                    rec.free_ship_status = 'Free Ship Eligible by Cost'
                elif rec.amount_total < rec.m_cost:
                    rec.free_ship_status = 'Not Free Ship Eligible, Cost low by $'\
                        +str(round(rec.m_cost-rec.amount_total))
                else:
                    rec.free_ship_status = 'error_cost'
            # Min Quantity
            elif rec.ship_rule == 'm_qty':
                if rec.tot_qty >= rec.m_qty:
                    rec.free_ship_status = 'Free Ship Eligible by Qty'
                elif rec.tot_qty < rec.m_qty:
                    rec.free_ship_status = 'Not Free Ship Eligible, Qty low by '\
                        +str(round(rec.m_qty-rec.tot_qty))
                else:
                    rec.free_ship_status = 'error_qty'
            # Min Weight
            elif rec.ship_rule == 'm_wght':
                if rec.tot_wght >= rec.m_wght:
                    rec.free_ship_status = 'Free Ship Eligible by Wght'
                elif rec.tot_wght < rec.m_wght:
                    rec.free_ship_status = 'Not Free Ship Eligible, Wght to low ('\
                        +str(round(rec.m_wght-rec.tot_wght))+')'
                else:
                    rec.free_ship_status = 'error_wght'
            # Min Qty/Cost/Wght
            elif rec.ship_rule == 'm_qty_cost_wght':
                if rec.tot_qty >= rec.m_qty or rec.amount_total >= rec.m_cost or rec.tot_wght >= rec.m_wght:
                    rec.free_ship_status = 'Free Ship Eligible by Qty or Wght or Cost'
                elif rec.tot_qty < rec.m_qty and rec.amount_total < rec.m_cost and rec.tot_wght < rec.m_wght:
                    rec.free_ship_status = 'Not Free Ship Eligible, Qty/Cost/Wght to low ('\
                        +str(round(rec.m_qty-rec.tot_qty))+'/$'+str(round(rec.m_cost-rec.amount_total))+'/'\
                        +str(round(rec.m_wght-rec.tot_wght))+')'
                else:
                    rec.free_ship_status = 'error_qty_or_cost_or_wght'
            # Min Cost/Wght
            elif rec.ship_rule == 'm_cost_wght':
                if rec.amount_total >= rec.m_cost or rec.tot_wght >= rec.m_wght:
                    rec.free_ship_status = 'Free Ship Eligible by Wght or Cost'
                elif rec.amount_total < rec.m_cost and rec.tot_wght < rec.m_wght:
                    rec.free_ship_status = 'Not Free Ship Eligible, Cost/Wght to low ($'\
                        +str(round(rec.m_cost-rec.amount_total))+'/'+str(round(rec.m_wght-rec.tot_wght))+')'
                else:
                    rec.free_ship_status = 'error_cost_or_wght'
            # Min Cost or Max Lines
            elif rec.ship_rule == 'm_cost_lines':
                if rec.amount_total >= rec.m_cost and rec.tot_line_cnt <= rec.mx_line_cnt:
                    rec.free_ship_status = 'Free Ship Eligible by Cost and Max Line Count'
                elif rec.amount_total < rec.m_cost or rec.tot_line_cnt > rec.mx_line_cnt:
                    rec.free_ship_status = 'Not Free Ship Eligible, Cost/Max Lines ($'\
                        +str(round(rec.m_cost-rec.amount_total))+'/'+str(round(rec.tot_line_cnt-rec.mx_line_cnt))+')'
                else:
                    rec.free_ship_status = 'error_cost_or_line_cnt'
            # Else to catch anythging else - should not get hit
            else:
                rec.free_ship_status = 'error_else'
    
    #@api.one
    # Total RFQ Calc
    @api.depends('ship_rule', 'order_line.product_qty')
    def _compute_tot_qty(self):
        for rec in self:
            tot_qty_calc = 0
            for line in rec.order_line:
                tot_qty_calc = tot_qty_calc + line.product_qty
            rec.tot_qty = tot_qty_calc
    
    # Total RFQ Weight Calc 
    @api.depends('ship_rule', 'order_line.product_qty', 'order_line.product_id.weight')
    def _compute_tot_wght(self):
        for rec in self:
            tot_wght_calc = 0
        for line in self.order_line:
            tot_wght_calc = tot_wght_calc + (line.product_qty * line.product_id.weight)
        self.tot_wght = tot_wght_calc
    
    # Total RFQ Nbr of Lines Calc 
    @api.depends('ship_rule', 'amount_total') #TODO, trigger when new line added?
    def _compute_tot_line_cnt(self):
        for rec in self:
            cnt = 0
        for line in rec.order_line:
            if line.product_id.type == 'product':
                cnt += 1
        self.tot_line_cnt = cnt

    # Model fields
    #  Related fields used in calcs
    ship_rule = fields.Selection(related='partner_id.free_ship_rule', string="Vendor Ship Rule")
    m_cost = fields.Float(related='partner_id.m_cost', string="Min PO Amount")
    m_qty = fields.Float(related='partner_id.m_qty', string="Min PO Qty")
    m_wght = fields.Float(related='partner_id.m_wght', string="Min PO Weight")
    mx_line_cnt = fields.Integer(related='partner_id.mx_line_cnt', string="Max Line Count")
    #  Compute fields
    tot_qty = fields.Float(compute='_compute_tot_qty', string='Total Quantity', readonly=True)
    tot_wght = fields.Float(compute='_compute_tot_wght', string='Total Weight', readonly=True)
    tot_line_cnt = fields.Integer(compute='_compute_tot_line_cnt', string='Total Line Count', readonly=True)
    free_ship_status = fields.Char(compute='_compute_free_ship_status', string='Free Ship Status', readonly=True, store=True)
