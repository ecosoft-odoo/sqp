openerp.ext_mrp = function (instance) {
    instance.web.Sidebar.include({
        init : function(){
            this._super.apply(this, arguments);
            // Hide all toolbar except more button
            var parent = this.getParent()
            if (parent && parent.dataset && parent.dataset.context && parent.dataset.context.hide_toolbar) {
                var newsections = []
                for (var i in this.sections) {
                    if (this.sections[i].name == 'other') {
                        newsections.push(this.sections[i]);
                    }
                }
                this.sections = newsections;
            }
        },
    });
};
