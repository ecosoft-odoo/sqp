openerp.ext_mrp = function (instance) {
    instance.web.Sidebar.include({
        init : function(){
            this._super.apply(this, arguments);
            // Hide toolbar only sale.order model
            var parent = this.getParent()
            if (parent && parent.dataset && parent.dataset.context && parent.dataset.context.hide_toolbar) {
                if (parent.model == 'sale.order') {
                    this.sections = []
                }
            }
        },
    });
};
