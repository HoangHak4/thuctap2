from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
import xlrd
import base64
from io import BytesIO


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('crm.customer.request', 'opportunity_id', string="Customer Requests")
    total_qty = fields.Float(string="Total Quantity", compute="_compute_total_qty", store=True)
    expected_revenue = fields.Float(string="Expected Revenue", compute="_compute_expected_revenue", store=True)

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        domain=[('company_id', '=', False), ('company_id', '=', 'company_id')],
        required=True
    )

    @api.depends('request_ids.qty')
    def _compute_total_qty(self):
        for lead in self:
            lead.total_qty = sum(request.qty for request in lead.request_ids)

    @api.depends('request_ids.qty', 'request_ids.product_id.list_price')
    def _compute_expected_revenue(self):
        for lead in self:
            lead.expected_revenue = sum(request.qty * request.product_id.list_price for request in lead.request_ids)

    def create_sale_order_from_leads(self):
        for lead in self:
            # Tạo Sale Order từ Lead
            sale_order = self.env['sale.order'].create({
                'partner_id': lead.partner_id.id,
                'date_order': fields.Datetime.now(),
                'opportunity_id': lead.id,
            })

            # Thêm sản phẩm vào Sale Order
        for request in lead.request_ids:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': request.product_id.id,
                'product_uom_qty': request.qty,
                'price_unit': request.product_id.list_price,
                })

        return True

    def send_confirmation_email(self):
        template = self.env.ref('your_module.email_template_confirmation')
        if template:
            self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)


    # Giới hạn quyền thêm, sửa, xóa yêu cầu chỉ cho phép ở trạng thái "Mới"
    @api.model
    def create(self, vals):
        opportunity = self.env['crm.lead'].browse(vals.get('opportunity_id'))
        if opportunity.stage_id.name != 'New':
            raise ValidationError('You cannot create request when Opportunity is not in New stage.')
        return super(CrmLead, self).create(vals)

    def write(self, vals):
        for record in self:
            if record.stage_id.name != 'New':
                raise ValidationError('You cannot update request when Opportunity is not in New stage.')
        return super(CrmLead, self).write(vals)

    def unlink(self):
        for record in self:
            if record.stage_id.name != 'New':
                raise ValidationError('You cannot delete request when Opportunity is not in New stage.')
        return super(CrmLead, self).unlink()

    def action_create_quotation(self):
        for lead in self:
            if not lead.request_ids:
                raise UserError("Opportunity does not have any customer requests.")

            quotation = self.env['sale.order'].create({
                'partner_id': lead.partner_id.id,
                'date_order': fields.Date.today(),
                'opportunity_id': lead.id,
            })

            for request in lead.request_ids:
                self.env['sale.order.line'].create({
                    'order_id': quotation.id,
                    'product_id': request.product_id.id,
                    'product_uom_qty': request.qty,
                    'price_unit': request.product_id.list_price,
                })

            return quotation

        @api.multi
        def import_requests_from_excel(self):
            for lead in self:
                if lead.excel_file:
                    file_data = base64.b64decode(lead.excel_file)
                    excel_file = BytesIO(file_data)
                    workbook = xlrd.open_workbook(file_contents=excel_file.read())
                    sheet = workbook.sheet_by_index(0)

                    for row in range(1, sheet.nrows):
                        product_id = sheet.cell_value(row, 0)
                        opportunity_id = lead.id
                        date = sheet.cell_value(row, 1)
                        description = sheet.cell_value(row, 2)
                        qty = sheet.cell_value(row, 3)

                        self.env['crm.customer.request'].create({
                            'product_id': product_id,
                            'opportunity_id': opportunity_id,
                            'date': date,
                            'description': description,
                            'qty': qty,
                        })

                    lead.message_post(body="Requests imported successfully from Excel.")