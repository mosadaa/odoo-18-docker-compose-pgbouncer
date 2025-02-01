from odoo import models, fields, tools

class CustomInvoiceLineView(models.Model):
    _name = 'custom.invoice.line'
    _auto = False
    _description = 'Custom Invoice Line View'

    invoice_date = fields.Date(string='Date')
    invoice_month = fields.Char(string='Month', compute='_compute_invoice_month', store=True)
    company_id = fields.Many2one('res.company', string='Company')
    team_id = fields.Many2one('crm.team', string='Sales Team')
    customer_code = fields.Char(string='Customer Code')
    partner_id = fields.Many2one('res.partner', string='Customer')
    state_id = fields.Many2one('res.country.state', string='State')
    city = fields.Char(string='City')
    journal_id = fields.Many2one('account.journal', string='Journal')
    move_id = fields.Many2one('account.move', string='Journal Entry')
    invoice_number = fields.Char(string='Inv_No')
    invoice_reference = fields.Text(string='Reference')
    account_id = fields.Many2one('account.account', string='Account')
    product_category = fields.Many2one('product.category', string='Product Category')
    product_code = fields.Char(string='Product Code')
    barcode = fields.Char(string='Barcode')
    product_id = fields.Many2one('product.product', string='Product')
    cost = fields.Float(string='Cost')
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    discount = fields.Float(string='Discount')
    price_unit_after_discount = fields.Float(string='Unit Price After Discount', compute='_compute_price_unit_after_discount')
    price_subtotal = fields.Float(string='Amount')
    price_total = fields.Float(string='Total (With Tax)')
    taxes = fields.Char(string='Taxes')
    debit = fields.Float(string='Debit')
    credit = fields.Float(string='Credit')
    amount_currency = fields.Float(string='Amount in Currency')
    invoice_type = fields.Selection([
        ('invoice', 'Invoice'),
        ('refund', 'Refund')
    ], string='Invoice Type')

    def _compute_invoice_month(self):
        for record in self:
            if record.invoice_date:
                record.invoice_month = record.invoice_date.strftime('%B')

    def _compute_price_unit_after_discount(self):
        for record in self:
            if record.price_unit and record.discount:
                record.price_unit_after_discount = record.price_unit * (1 - record.discount / 100)
            else:
                record.price_unit_after_discount = record.price_unit

    def _query(self):

        return """
            SELECT 
                aml.id AS id,
                am.invoice_date,
                to_char(am.invoice_date, 'Month') as invoice_month,
                am.company_id,
                am.team_id,
                rp.ref as customer_code,
                am.partner_id,
                rp.state_id,
                rp.city,
                am.journal_id,
                aml.move_id,
                am.name as invoice_number,
                am.ref as invoice_reference,
                aml.account_id,
                pt.categ_id as product_category,
                pt.default_code as product_code,
                pp.barcode as barcode,
                aml.product_id,
                CASE 
                    WHEN am.move_type = 'out_refund' THEN -aml.quantity 
                    ELSE aml.quantity 
                END AS quantity,
                aml.price_unit,
                aml.discount,
                CASE 
                    WHEN am.move_type = 'out_refund' THEN -(aml.price_unit * (1 - aml.discount / 100)) 
                    ELSE (aml.price_unit * (1 - aml.discount / 100))
                END AS price_unit_after_discount,
                CASE 
                    WHEN am.move_type = 'out_refund' THEN -aml.price_subtotal 
                    ELSE aml.price_subtotal 
                END AS price_subtotal,
                CASE 
                    WHEN am.move_type = 'out_refund' THEN -aml.price_total 
                    ELSE aml.price_total 
                END AS price_total,
                COALESCE(MAX((pp.standard_price->>am.company_id::text)::float), 0) as cost,
                array_to_string(array_agg(at.name), ', ') as taxes,
                aml.debit,
                aml.credit,
                aml.amount_currency,
                CASE
                    WHEN am.move_type = 'out_refund' THEN 'refund'
                    ELSE 'invoice'
                END AS invoice_type
            FROM 
                account_move_line aml
            JOIN 
                account_move am ON aml.move_id = am.id
            JOIN 
                product_product pp ON aml.product_id = pp.id
            JOIN 
                product_template pt ON pp.product_tmpl_id = pt.id
            LEFT JOIN
                res_partner rp ON am.partner_id = rp.id
            LEFT JOIN
                account_move_line_account_tax_rel amlt ON amlt.account_move_line_id = aml.id
            LEFT JOIN
                account_tax at ON amlt.account_tax_id = at.id
            WHERE 
                aml.product_id IS NOT NULL
                AND am.state = 'posted'
                AND am.move_type IN ('out_invoice', 'out_refund')
                AND aml.account_id IN (
                     SELECT id FROM account_account 
                     WHERE account_type = 'income'
                )
            GROUP BY 
                aml.id, am.invoice_date, am.company_id, am.team_id, rp.ref, am.partner_id, rp.state_id, rp.city, am.journal_id, aml.move_id, am.name, am.ref, aml.account_id, pt.categ_id, pt.default_code, pp.barcode, aml.product_id, aml.quantity, aml.price_unit, aml.discount, aml.price_subtotal, aml.price_total, aml.debit, aml.credit, aml.amount_currency, am.move_type,pp.standard_price
            """
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query())
        )