from flask import render_template, flash, redirect, url_for
from app.forms import  LabelForm
from app import app
import subprocess

from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

@app.route('/', methods=['GET', 'POST'])
@app.route('/label', methods=['GET', 'POST'])
def label():
    form = LabelForm()
    if form.validate_on_submit():
        flash('printing label: {}'.format(form.labeltext.data))
        printLabel(form.labeltext.data, form.generate_pdf_only.data)
        return redirect(url_for('label'))
    return render_template('label.html', title='Print Label', form=form)


def printLabel( text_to_print = '', generate_pdf_only=True ):
    font_config = FontConfiguration()
    print(text_to_print)
    textsize = str(len( text_to_print.splitlines() )+1)
    textInHtml = '<h'+ textsize + '><pre>'
    for line in text_to_print.splitlines():
        textInHtml=textInHtml + line + '<br />'
    textInHtml = textInHtml + '</pre></h'+ textsize + '>'
    print(textInHtml)
    html = HTML(string=textInHtml)
    css = CSS(string='''
        @page {
              size: 3.5in 0.9in;
              margin: 0em;
              margin-bottom: 0em;
              margin-top: 0em;
              vertical-align: center;
        }
        @font-face {
        font-family: 'Roboto Slab', serif;
        font-family: 'BioRhyme Expanded', serif;
        src: url(https://fonts.googleapis.com/css?family=BioRhyme+Expanded|Roboto+Slab);
        }
        h1 { font-family: 'BioRhyme Expanded', serif; }''', font_config=font_config)
    html.write_pdf('text_to_print.pdf', stylesheets=[css], font_config=font_config)

    # lpr -o PrintQuality=Text text_to_print.pdf -P LabelWriter-450-DUO-Label
    command = [ "lpr", "-o", "PrintQuality=Graphics", "text_to_print.pdf", "-P" , app.config["LABELPRINTER"] ]
    print(command)
    if not generate_pdf_only:
        subprocess.call(command)
