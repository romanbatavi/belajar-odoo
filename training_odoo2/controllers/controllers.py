# -*- coding: utf-8 -*-
# from odoo import http


# class TrainingOdoo2(http.Controller):
#     @http.route('/training_odoo2/training_odoo2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/training_odoo2/training_odoo2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('training_odoo2.listing', {
#             'root': '/training_odoo2/training_odoo2',
#             'objects': http.request.env['training_odoo2.training_odoo2'].search([]),
#         })

#     @http.route('/training_odoo2/training_odoo2/objects/<model("training_odoo2.training_odoo2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('training_odoo2.object', {
#             'object': obj
#         })
