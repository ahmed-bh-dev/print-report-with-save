from odoo import models, api
import os
import tempfile

#his module is a feature added to the Accounting module. It prints a report when the save button is clicked after filling in the data.
class AccountMove(models.Model):
    _inherit = 'account.move'  # توسيع الموديل الأساسي للفواتير
    def print_direct(self):
        """Print the multiple invoice copies report directly to the default printer on Linux."""

        # Ensure the appropriate report is available
        report = self.env.ref('base_accounting_kit.report_multiple_invoice', False)
        if not report:
            raise ValueError("Report not found: base_accounting_kit.report_multiple_invoice")

        # Generate the report content
        report = self.env['ir.actions.report']
        context = dict(self.env.context)
        docids = self.ids
        reportname = 'base_accounting_kit.report_multiple_invoice'
        converter = 'pdf'
        report

        # if self.ids:
        #     docids = [int(i) for i in self.ids.split(',') if i.isdigit()]
        if converter == 'html':
            report = report.with_context(context)._render_qweb_html(reportname, docids, data=context)[0]
        elif converter == 'pdf':
            report = report.with_context(context)._render_qweb_pdf(reportname, docids, data=context)[0]
        elif converter == 'text':
            report = report.with_context(context)._render_qweb_text(reportname, docids, data=context)[0]

        # Save the report content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_path = tmp_file.name
            with open(pdf_path, 'wb') as f:
                f.write(report)

        # Print the file using lp command on Linux
        print("==============>" + pdf_path)
        os.system(f"lp {pdf_path}")


    @api.model
    def create(self, vals):
        """ حفظ الفاتورة + استدعاء الطباعة تلقائيًا """
        record = super(AccountMove, self).create(vals)  # حفظ الفاتورة
        if hasattr(record, 'print_direct'):  # التأكد من وجود الفانكشن
           record.print_direct()  # استدعاء الطباعة
        return record

    def write(self, vals):
        """ تعديل الفاتورة + استدعاء الطباعة تلقائيًا """
        result = super(AccountMove, self).write(vals)  # تعديل الفاتورة
        if hasattr(self, 'print_direct'):  # التأكد من وجود الفانكشن
            self.print_direct()  # استدعاء الطباعة
        return result

    def wrap_text(text, line_length=20):
        """تقسيم النص إلى أسطر بعد عدد معين من الأحرف"""
        lines = []
        while len(text) > line_length:
            lines.append(text[:line_length])
            text = text[line_length:]
        if text:
            lines.append(text)
        return '\n'.join(lines)

#================================================================================================
#================================================================================================


