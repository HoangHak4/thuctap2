from odoo import http
from odoo.http import request
import json
from datetime import datetime

class CrmLeadApi(http.Controller):

    @http.route('/api/create_lead', type='json', auth='public', methods=['POST'])
    def create_lead(self, **kwargs):
        try:
            data = kwargs.get('data')

            if not data:
                return {'error': 'No data provided'}

            customer_name = data.get('customer_name')
            email = data.get('email')
            phone = data.get('phone')
            internal_notes = data.get('internal_notes')
            deadline_date = data.get('deadline_date')
            requests = data.get('requests')

            # Tạo lead mới
            lead = request.env['crm.lead'].sudo().create({
                'name': customer_name,
                'email_from': email,
                'phone': phone,
                'description': internal_notes,
                'date_deadline': datetime.strptime(deadline_date, '%Y-%m-%d').date(),
            })

            # Tạo yêu cầu (requests) cho lead
            for req in requests:
                product_name = req.get('product_name')
                quantity = req.get('quantity')
                date = req.get('date')

                # Tìm sản phẩm từ tên sản phẩm
                product = request.env['product.template'].sudo().search([('name', '=', product_name)], limit=1)
                if product:
                    request.env['crm.customer.request'].sudo().create({
                        'product_id': product.id,
                        'qty': quantity,
                        'date': date,
                        'opportunity_id': lead.id,
                    })

            return {'message': 'Lead created successfully', 'lead_id': lead.id}

        except Exception as e:
            return {'error': str(e)}
