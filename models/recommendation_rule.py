# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError

# Import des librairies de Data Science
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

class AiRecommendationRule(models.Model):
    _name = 'ai.recommendation.rule'
    _description = 'AI Association Rules'
    _order = 'confidence desc'

    antecedent_product_id = fields.Many2one('product.product', string="Antecedent Product", required=True, index=True)
    consequent_product_id = fields.Many2one('product.product', string="Consequent Product", required=True)
    support = fields.Float(string="Support", help="Frequency of the pair in all transactions")
    confidence = fields.Float(string="Confidence", help="Likelihood of buying B if A is bought")
    lift = fields.Float(string="Lift", help="Strength of the correlation (>1 is good)")
    rule_name = fields.Char(compute='_compute_rule_name', string="Rule Name")

    @api.depends('antecedent_product_id', 'consequent_product_id')
    def _compute_rule_name(self):
        for record in self:
            if record.antecedent_product_id and record.consequent_product_id:
                record.rule_name = f"If {record.antecedent_product_id.name} -> Then {record.consequent_product_id.name}"
            else:
                record.rule_name = "New Rule"

    @api.model
    def action_generate_rules(self):
        """
        Main AI Engine: Analyzes Sales Orders and generates Association Rules.
        """
        # 1. Fetch Sales Data (Confirmed orders only)
        sales = self.env['sale.order'].search([('state', 'in', ['sale', 'done'])])
        if not sales:
            raise UserError("No confirmed sales found to train the AI.")

        # 2. Prepare Data for Pandas (List of transactions)
        # Format: [['Apple', 'Banana'], ['Apple', 'Orange'], ...]
        transactions = []
        for order in sales:
            # Get product IDs for each order line
            products = order.order_line.mapped('product_id.id')
            # Only keep orders with at least 2 products (No cross-sell possible with 1 product)
            if len(set(products)) > 1:
                transactions.append(list(set(products)))

        if not transactions:
            raise UserError("Not enough complex orders (minimum 2 items per order) to find correlations.")

        # 3. Transform to One-Hot Encoding DataFrame
        # mlxtend requires a boolean matrix
        from mlxtend.preprocessing import TransactionEncoder
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        # 4. Apply Apriori Algorithm (Find frequent itemsets)
        # min_support=0.01 means the item must appear in at least 1% of transactions
        frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)

        if frequent_itemsets.empty:
            raise UserError("No frequent patterns found. Sell more products!")

        # 5. Generate Association Rules
        # min_threshold=0.1 means at least 10% confidence
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)

        # 6. Save Rules to Odoo Database
        # First, clear old rules
        self.search([]).unlink()

        # Create new rules
        new_rules_count = 0
        for index, row in rules.iterrows():
            # Apriori returns frozensets, we take the first item (simplification for A -> B)
            antecedent_id = list(row['antecedents'])[0]
            consequent_id = list(row['consequents'])[0]

            self.create({
                'antecedent_product_id': antecedent_id,
                'consequent_product_id': consequent_id,
                'support': row['support'],
                'confidence': row['confidence'],
                'lift': row['lift'],
            })
            new_rules_count += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'AI Training Complete',
                'message': f'Successfully generated {new_rules_count} recommendation rules!',
                'type': 'success',
                'sticky': False,
            }
        }