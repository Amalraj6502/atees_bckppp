/** @odoo-module **/

import { Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    // Override the constructor to initialize your custom field
    // NOTE: If your Odoo version is older (like Odoo 16/17), the 'patch' may require a slightly different syntax or you might need to use a hook like `onPatched` if you were extending an OWL component, but for the JS model, this is usually correct.
    init(options) {
        // 🚨 CRITICAL: Call the super (parent) constructor FIRST to initialize all standard fields (like payment_ids, orderlines, etc.)
        super.init(...arguments);

        // Then, initialize your custom field
        this.custom_partner_id = false;
    },

    // ... rest of your code (getCustomPartnerId, setCustomPartnerId, export_as_JSON, etc.)
});