openerp.ext_mrp = function (instance) {
    instance.web.Sidebar.include({
        init : function(){
            this._super.apply(this, arguments);
            // Hide toolbar
            var parent = this.getParent()
            if (parent && parent.dataset && parent.dataset.context && parent.dataset.context.hide_toolbar) {
                this.sections = []
            }
        },
    });
};
