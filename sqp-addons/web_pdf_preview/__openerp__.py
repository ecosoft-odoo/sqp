# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################

{
    "name": "Web PDF Report Preview & Print",
    'version': '1.0',
    'category': 'Web',
    'description': """Web PDF Report Preview & Print

Preview & Print PDF report in your browser.

* For IE, Adobe Reader is required.
* For Chrome , nothing is requried.
* For Firefox, Adobe Reader is required.

Test passed on Windows.

If your brower prevented pop-up window, you should allow it.

功能：PDF 报表预览

如果您觉得好用，请进入下面的网址，付费支持作者 ~

http://me.alipay.com/wangbuke

谢谢！

    """,
    'author': 'wangbuke@gmail.com',
    'website': 'http://buke.github.io',
    'license': 'AGPL-3',
    'depends': ['web'],
    'data': [],
    'auto_install': False,
    'web_preload': True,
    'js': ['static/src/js/web_pdf_preview.js'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
