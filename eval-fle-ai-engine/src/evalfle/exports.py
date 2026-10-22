"""Exports imprimables en Word et PDF, destinés à l'enseignant."""
from __future__ import annotations
from io import BytesIO
from xml.sax.saxutils import escape

from .engine import Question, overview, safe_label


def _title(grade: int):
    return f'Évaluation de français — Grade {grade} — A1 (supports illustratifs)'


def build_docx(questions: list[Question], teacher: bool = False, author: str = 'Junior BOOTO Waba') -> bytes:
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    if not questions:
        raise ValueError('Questions manquantes')
    grade = questions[0].grade
    d=Document()
    sec=d.sections[0];sec.top_margin=Inches(.7);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
    styles=d.styles
    normal=styles['Normal'];normal.font.name='Aptos';normal.font.size=Pt(10);normal.font.color.rgb=RGBColor(29,50,80)
    normal.paragraph_format.space_after=Pt(5)
    for name,sz in [('Title',18),('Heading 1',13),('Heading 2',11)]:
        st=styles[name];st.font.name='Aptos';st.font.size=Pt(sz);st.font.color.rgb=RGBColor(21,91,142)
    p=d.add_paragraph(style='Title');p.add_run(_title(grade))
    p=d.add_paragraph('Nom : __________________________________________     Date : __________________')
    p.add_run('\nClasse : ______________________     Durée indicative : 45 minutes')
    d.add_paragraph(f"Document {'enseignant — corrigé' if teacher else 'élève — questionnaire'}  |  {len(questions)} QCM  |  1 point par bonne réponse")
    d.add_paragraph('Consigne : coche une seule réponse (A, B, C ou D) pour chaque question. Aucun passage de lecture, enregistrement ou tâche orale.')
    for k,q in enumerate(questions,1):
        p=d.add_paragraph();p.paragraph_format.keep_with_next=True
        run=p.add_run(f'{k}. {q.question}');run.bold=True
        for letter,choice in zip('ABCD',q.choices):
            p=d.add_paragraph(style='Normal');p.paragraph_format.left_indent=Inches(.23)
            p.add_run(f'☐ {letter}. {choice}')
    d.add_page_break()
    d.add_heading('Grille de réponses',level=1)
    t=d.add_table(rows=1,cols=5)
    t.style='Table Grid'
    for c,txt in zip(t.rows[0].cells,['N°','A','B','C','D']):c.text=txt
    for k in range(1,len(questions)+1):
        row=t.add_row().cells;row[0].text=str(k)
        for i in range(1,5): row[i].text='☐'
    if teacher:
        d.add_page_break()
        d.add_heading('Corrigé réservé à l’enseignant',level=1)
        for k,q in enumerate(questions,1):
            d.add_paragraph(f'{k:02d} — {q.answer}  |  {q.category}  |  {q.choices["ABCD".index(q.answer)]}')
        d.add_heading('Critères observables « Je peux… »',level=2)
        for row in overview(questions):
            d.add_paragraph(f"• {row['category']} ({row['count']} items) : {row['criterion']}")
        d.add_paragraph('Barème : 1 point par réponse correcte, 0 pour réponse incorrecte ou absente. Résultats par domaine à interpréter en contexte ; ce questionnaire ne certifie aucun niveau du CECRL.')
        d.add_paragraph('Limite : les QCM ne mesurent pas directement la compréhension orale, la production orale ou la production écrite.')
    footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.CENTER;footer.text=f'BOOTO Éval’FLE AI Engine · Prototype V1 · {safe_label(author)}'
    b=BytesIO();d.save(b);return b.getvalue()


def build_pdf(questions: list[Question], teacher: bool = False, author: str = 'Junior BOOTO Waba') -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pathlib import Path
    if not questions:
        raise ValueError('Questions manquantes')
    fonts=[Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),Path('/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf')]
    chosen=next((p for p in fonts if p.exists()),None)
    font='Helvetica'
    if chosen:
        font='EvalFLEUnicode'
        if font not in pdfmetrics.getRegisteredFontNames():pdfmetrics.registerFont(TTFont(font,str(chosen)))
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='EvalTitle',fontName=font,fontSize=14,leading=18,textColor=colors.HexColor('#144e82'),spaceAfter=12))
    styles.add(ParagraphStyle(name='EvalInfo',fontName=font,fontSize=8.6,leading=13,spaceAfter=7))
    styles.add(ParagraphStyle(name='EvalItem',fontName=font,fontSize=9.0,leading=13,spaceAfter=4))
    styles.add(ParagraphStyle(name='EvalOption',fontName=font,fontSize=8.7,leading=12,leftIndent=12,spaceAfter=2))
    styles.add(ParagraphStyle(name='EvalH2',fontName=font,fontSize=12,leading=15,textColor=colors.HexColor('#147c91'),spaceBefore=7,spaceAfter=8))
    stream=BytesIO();pdf=SimpleDocTemplate(stream,pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=17*mm,bottomMargin=17*mm)
    story=[Paragraph(escape(_title(questions[0].grade)),styles['EvalTitle']),
           Paragraph('Nom : ____________________________________      Date : ____________________',styles['EvalInfo']),
           Paragraph(f"Document {'enseignant — corrigé' if teacher else 'élève — questionnaire'} | {len(questions)} QCM | Durée indicative : 45 minutes",styles['EvalInfo']),
           Paragraph('Consigne : coche une seule réponse (A, B, C ou D) par question. Chaque réponse correcte vaut 1 point.',styles['EvalInfo']),Spacer(1,4*mm)]
    for k,q in enumerate(questions,1):
        chunk=[Paragraph(f'<b>{k}. {escape(q.question)}</b>',styles['EvalItem'])]
        for letter,choice in zip('ABCD',q.choices):chunk.append(Paragraph(f'(  ) {letter}. {escape(choice)}',styles['EvalOption']))
        chunk.append(Spacer(1,3*mm))
        story.append(KeepTogether(chunk))
    story.extend([PageBreak(),Paragraph('Grille de réponses',styles['EvalH2'])])
    rows=[['N°','A','B','C','D']]+[[str(k)]+['(  )']*4 for k in range(1,len(questions)+1)]
    t=Table(rows,colWidths=[22*mm]+[24*mm]*4,rowHeights=[8*mm]+[6.5*mm]*len(questions),repeatRows=1)
    t.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),font),('FONTSIZE',(0,0),(-1,-1),8),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c0d4e6')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7f4fb')),('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(t)
    if teacher:
        story.extend([PageBreak(),Paragraph('Corrigé réservé à l’enseignant',styles['EvalH2'])])
        for k,q in enumerate(questions,1):
            story.append(Paragraph(f'{k:02d}. <b>{q.answer}</b> — {escape(q.category)} : {escape(q.choices["ABCD".index(q.answer)])}',styles['EvalItem']))
        story.append(Paragraph('Critères observables « Je peux… »',styles['EvalH2']))
        for row in overview(questions):
            story.append(Paragraph(f"<b>{escape(row['category'])} ({row['count']} items) :</b> {escape(row['criterion'])}",styles['EvalInfo']))
        story.append(Paragraph('Barème : 1 point par bonne réponse, 0 sinon. Ces résultats ne certifient pas le niveau CECRL ; les compétences orales et la production écrite ne sont pas évaluées directement.',styles['EvalInfo']))
    def footer(canvas,doc):
        canvas.saveState();canvas.setFont(font,7);canvas.setFillColor(colors.HexColor('#54708d'))
        canvas.drawCentredString(A4[0]/2,10*mm,f"BOOTO Éval’FLE AI Engine · {safe_label(author)} · page {doc.page}")
        canvas.restoreState()
    pdf.build(story,onFirstPage=footer,onLaterPages=footer)
    return stream.getvalue()
