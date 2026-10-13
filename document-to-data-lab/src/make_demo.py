from pathlib import Path
import csv,json
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

HEAD=['id','date','description','amount','currency']

def pdf(path,rows,total):
    styles=getSampleStyleSheet()
    table=Table([HEAD]+rows,colWidths=[65,85,160,70,65])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#183d50')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.6,colors.HexColor('#8aa3b0')),('FONTSIZE',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    SimpleDocTemplate(str(path)).build([Paragraph('Document-to-Data Lab',styles['Title']),Paragraph('Junior BOOTO - Rapport associatif FICTIF',styles['Normal']),Spacer(1,24),table,Spacer(1,16),Paragraph('TOTAL USD: '+total,styles['Normal']),Paragraph('Document original de démonstration. Aucun organisme réel.',styles['Normal'])])

def generate(folder):
    p=Path(folder);p.mkdir(parents=True,exist_ok=True)
    pdf(p/'01_report.pdf',[['A001','2026-01-01','Livres','100.00','USD'],['A002','2026-01-02','Transport','30.00','USD']],'130.00')
    pdf(p/'02_report.pdf',[['A001','2026-01-01','Livres','100.00','USD'],['A003','2026-01-03','Materiel','25.00','USD'],['A004','2026-02-30','Erreur de saisie','abc','USD']],'130.00')
    with (p/'03_expenses.csv').open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.writer(f,delimiter=';');w.writerow(['identifiant','date','description','montant','devise']);w.writerows([['A005','2026-01-04','Papeterie','12000','COP'],['A006','2026-01-04','Impression','18000','COP'],['A007','2026-01-05','Devise hors contrat','50','EUR'],['A008','2026-01-05','=SUM(A1:A2)','10,50','USD']])
    (p/'04_incompatible.csv').write_text('date,montant\n2026-01-01,15\n')
    truth={'rows':9,'accepted_ids':['A002','A003','A005','A006','A008'],'review_ids':['A001','A001','A004','A007'],'blocked_files':['04_incompatible.csv'],'total_mismatch_files':['02_report.pdf'],'totals':{'COP':'30000.00','USD':'65.50'}}
    return truth

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('folder');a=p.parse_args();print(json.dumps(generate(a.folder),indent=2))
