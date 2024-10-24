from odoo import models, fields

class ThongTinNCC(models.Model):
    _name = 'thong.tin.ncc'
    _description = 'Thông tin nhà cung cấp'

    ten_ncc = fields.Char(string='Tên nhà cung cấp', required=True)
    dia_chi = fields.Char(string='Địa chỉ', required=True)
    email = fields.Char(string='Email', required=True)
    dien_thoai = fields.Integer(string='Điện thoại')
    website = fields.Char(string='Website')
    tax_id = fields.Char(string='Tax ID')
    tags = fields.Char(string='Tags')
    danh_gia_cuoi_cung = fields.Selection([
        ('1', '- 1 sao'),
        ('2', '- 2 sao'),
        ('3', '- 3 sao'),
        ('4', '- 4 sao'),
        ('5', '- 5 sao'),
    ], string='Đánh giá cuối cùng')
    danh_gia_moi = fields.Text(string='Đánh giá mới')
