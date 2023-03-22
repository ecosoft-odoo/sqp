/*############################################################################
#    Web PDF Report Preview & Print
#    Copyright 2012 wangbuke <wangbuke@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################*/

openerp.web_pdf_preview = function(instance) {
    instance.web.ActionManager = instance.web.ActionManager.extend({
        ir_actions_report_xml: function(action, options) {
            var self = this;
            instance.web.blockUI();
            return instance.web.pyeval.eval_domains_and_contexts({
                contexts: [action.context],
                domains: []
            }).then(function(res) {
                action = _.clone(action);
                action.context = res.context;
                //var os = navigator.platform || "Unknown OS";
                //linux = os.indexOf("Linux") > -1;
                instance.web.unblockUI();
                self.dialog_stop();
                window.open('/web/report/pdf?action=' + encodeURIComponent(JSON.stringify(action)) + '&token=' + new Date().getTime() + '&session_id=' + self.session.session_id, 'report', '');
            });
        },
    });


};


