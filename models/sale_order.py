# -*- coding: utf-8 -*-
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Ce champ va contenir les suggestions
    ai_suggestion_ids = fields.Many2many(
        'ai.recommendation.rule', 
        compute='_compute_ai_suggestions', 
        string="AI Suggestions"
    )

    @api.depends('order_line.product_id')
    def _compute_ai_suggestions(self):
        for order in self:
            # 1. Quels produits sont déjà dans le panier ?
            cart_product_ids = order.order_line.mapped('product_id.id')
            
            if not cart_product_ids:
                order.ai_suggestion_ids = False
                continue

            # 2. Chercher les règles : 
            # - Où le produit déclencheur (antecedent) EST dans le panier
            # - ET où le produit suggéré (consequent) N'EST PAS encore dans le panier
            rules = self.env['ai.recommendation.rule'].search([
                ('antecedent_product_id', 'in', cart_product_ids),
                ('consequent_product_id', 'not in', cart_product_ids)
            ])

            # 3. Trier par confiance (les meilleures en premier) et garder les 5 meilleures
            order.ai_suggestion_ids = rules.sorted(key=lambda r: r.confidence, reverse=True)[:5]

    def action_add_suggestion_to_cart(self):
        """
        Méthode appelée par le bouton dans la vue pour ajouter le produit suggéré.
        (Nécessite un contexte pour savoir quelle règle a été cliquée)
        """
        self.ensure_one()
        pass