from odoo import models, fields, api

class NhaCungCap(models.Model):
    _name = 'nha.cung.cap'
    _description = 'Nhà cung cấp'

    ma_phieu = fields.Char(string='Mã phiếu', required=True, default=lambda self: self.env['ir.sequence'].next_by_code('nha.cung.cap.sequence'))
    ten_ncc = fields.Char(string='Tên nhà cung cấp', required=True)
    email = fields.Char(string='Email', required=True)
    dien_thoai = fields.Char(string='Điện thoại')
    nganh_kd = fields.Char(string='Ngành kinh doanh')
    ky_dg = fields.Date(string='Kỳ đánh giá')
    ngay_dg = fields.Date(string='Ngày đánh giá')
    quan_ly = fields.Many2one('res.users', string='Quản lý')
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('refused', 'Từ chối'),
        ('cancelled', 'Huỷ')
    ], string='Trạng thái', default='draft')

    chi_tiet_danh_gia_ids = fields.One2many('ct.danh.gia.ncc', 'nha_cung_cap_id', string='Chi Tiết Đánh Giá')

    @api.depends('chi_tiet_danh_gia_ids.diem_dg')
    def _compute_total_score(self):
        for record in self:
            total_score = sum(record.chi_tiet_danh_gia_ids.mapped('diem_dg'))
            record.tong_diem_cuoi_cung = total_score

    tong_diem_cuoi_cung = fields.Float(string='Tổng điểm cuối cùng', compute='_compute_total_score', store=True)
