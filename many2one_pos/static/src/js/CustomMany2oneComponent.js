/** @odoo-module **/
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";
import { Many2XAutocomplete } from "@web/views/fields/relational_utils";

export class CustomPartnerButton extends Component {
    static template = "your_module.CustomPartnerButton";
    static components = { Many2XAutocomplete };

    setup() {
        super.setup();
        this.orm = useService("orm"); // To fetch partner display names if needed
        this.state = this.env.pos.get_order(); // The reactive state is the current order
    }

    // This method handles the value change from the Many2XAutocomplete widget
    async updatePartner(selection) {
        // selection is an array: [[ID, Name], ...]
        const selectedPartner = selection[0];

        if (selectedPartner) {
            // [ID, Name] pair to store in the order model for display
            this.state.setCustomPartnerId(selectedPartner);
        } else {
            this.state.setCustomPartnerId(false);
        }
    }

    get partnerProps() {
        // Props needed by the Many2XAutocomplete widget
        return {
            resModel: 'res.partner',
            fieldString: 'Custom Partner',
            value: this.state.getCustomPartnerId(),
            onChange: (selection) => this.updatePartner(selection), // Link the change handler
            // Additional props for styling/behavior can be added here
        };
    }
}

// 💡 Patch the ControlButtons to add the new button
patch(ControlButtons.prototype, {
    ControlButtonsTemplate: CustomPartnerButton.template,
});