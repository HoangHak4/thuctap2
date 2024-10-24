from odoo import models, fields


class ChiTietDanhGiaNCC(models.Model):
    _name = 'ct.danh.gia.ncc'
    _description = 'Chi tiết đánh giá nhà cung cấp'

    # nha_cung_cap_id = fields.Many2one('nha.cung.cap', string='Nhà cung cấp')
    tieu_chi_dg = fields.Many2one('tieu.chi.dg', string='Tiêu chí đánh giá')
    da_duoc_dg = fields.Boolean(string='Đã được đánh giá', default=False)
    diem_dg = fields.Selection([
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], string='Điểm đánh giá')
    tong_diem_cuoi_cung = fields.Float(string='Tổng điểm cuối cùng')
    kq_danh_gia = fields.Selection([
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], string='Kết quả đánh giá')
    thong_tin_phan_hoi = fields.Text(string='Thông tin phản hồi')
