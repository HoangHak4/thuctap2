from odoo import models, fields

class TieuChiDanhGia(models.Model):
    _name = 'tieu.chi.danh.gia'
    _description = 'Tiêu chí đánh giá'

    ma_tc = fields.Char(string='Mã tiêu chí', required=True)
    ten_tc = fields.Char(string='Tên tiêu chí', required=True)