"""Import vérifié d'un sous-ensemble officiel AdventureWorks vers SQLite."""
from pathlib import Path
import sqlite3,csv,json
from decimal import Decimal
from collecter import main as collect
ROOT=Path(__file__).resolve().parent
SCHEMA={
 'ProductCategory': [('ProductCategoryID',0,'INTEGER PRIMARY KEY'),('Name',1,'TEXT NOT NULL')],
 'ProductSubcategory': [('ProductSubcategoryID',0,'INTEGER PRIMARY KEY'),('ProductCategoryID',1,'INTEGER REFERENCES ProductCategory(ProductCategoryID)'),('Name',2,'TEXT NOT NULL')],
 'Product': [('ProductID',0,'INTEGER PRIMARY KEY'),('Name',1,'TEXT NOT NULL'),('StandardCost',8,'REAL'),('ProductSubcategoryID',18,'INTEGER REFERENCES ProductSubcategory(ProductSubcategoryID)')],
 'SalesTerritory':[('TerritoryID',0,'INTEGER PRIMARY KEY'),('Name',1,'TEXT NOT NULL'),('CountryRegionCode',2,'TEXT'),('TerritoryGroup',3,'TEXT')],
 'Customer':[('CustomerID',0,'INTEGER PRIMARY KEY'),('PersonID',1,'INTEGER'),('StoreID',2,'INTEGER'),('TerritoryID',3,'INTEGER REFERENCES SalesTerritory(TerritoryID)')],
 'SalesPerson':[('BusinessEntityID',0,'INTEGER PRIMARY KEY'),('TerritoryID',1,'INTEGER REFERENCES SalesTerritory(TerritoryID)')],
 'SalesOrderHeader':[('SalesOrderID',0,'INTEGER PRIMARY KEY'),('OrderDate',2,'TEXT NOT NULL'),('Status',5,'INTEGER'),('OnlineOrderFlag',6,'INTEGER'),('CustomerID',10,'INTEGER REFERENCES Customer(CustomerID)'),('SalesPersonID',11,'INTEGER REFERENCES SalesPerson(BusinessEntityID)'),('TerritoryID',12,'INTEGER REFERENCES SalesTerritory(TerritoryID)'),('SubTotal',19,'REAL'),('TaxAmt',20,'REAL'),('Freight',21,'REAL'),('TotalDue',22,'REAL')],
 'SalesOrderDetail':[('SalesOrderID',0,'INTEGER REFERENCES SalesOrderHeader(SalesOrderID)'),('SalesOrderDetailID',1,'INTEGER PRIMARY KEY'),('OrderQty',3,'INTEGER'),('ProductID',4,'INTEGER REFERENCES Product(ProductID)'),('UnitPrice',6,'REAL'),('UnitPriceDiscount',7,'REAL'),('LineTotal',8,'REAL')],
 'ProductCostHistory':[('ProductID',0,'INTEGER REFERENCES Product(ProductID)'),('StartDate',1,'TEXT NOT NULL'),('EndDate',2,'TEXT'),('StandardCost',3,'REAL')]
}
EXPECTED={'ProductCategory':4,'ProductSubcategory':37,'Product':504,'SalesTerritory':10,'Customer':19820,'SalesPerson':17,'SalesOrderHeader':31465,'SalesOrderDetail':121317,'ProductCostHistory':395}

def main():
    collect()
    path=ROOT/'collected'/'AdventureWorks_commercial.sqlite'
    path.parent.mkdir(exist_ok=True)
    if path.exists():path.unlink()
    db=sqlite3.connect(path);db.execute('PRAGMA foreign_keys=ON')
    dictionary=[]
    max_line_error=Decimal(0)
    for table,columns in SCHEMA.items():
        db.execute('CREATE TABLE '+table+' ('+', '.join(name+' '+kind for name,index,kind in columns)+')')
        rows=[]
        with (ROOT/'raw'/f'{table}.csv').open(encoding='utf-8-sig',newline='') as f:
            for original in csv.reader(f,delimiter='\t',quoting=csv.QUOTE_NONE):
                row=[]
                for name,index,kind in columns:
                    value=original[index]
                    row.append(None if value=='' else int(value) if kind.startswith('INTEGER') else float(value) if kind.startswith('REAL') else value)
                rows.append(row)
                if table=='SalesOrderDetail':
                    expected=Decimal(original[6])*(1-Decimal(original[7]))*Decimal(original[3])
                    max_line_error=max(max_line_error,abs(expected-Decimal(original[8])))
        assert len(rows)==EXPECTED[table],(table,len(rows))
        db.executemany('INSERT INTO '+table+' VALUES ('+','.join('?' for c in columns)+')',rows)
        dictionary.extend({'table':table,'column':name,'source_index_0_based':index,'sqlite_type':kind,'source_file':f'raw/{table}.csv'} for name,index,kind in columns)
    assert max_line_error<=Decimal('0.000001')
    db.execute('CREATE INDEX idx_order_date ON SalesOrderHeader(OrderDate)')
    db.execute('CREATE INDEX idx_detail_order ON SalesOrderDetail(SalesOrderID)')
    db.execute('CREATE INDEX idx_cost_product_dates ON ProductCostHistory(ProductID,StartDate,EndDate)')
    db.executescript((ROOT/'vues.sql').read_text())
    db.commit()
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    assert not db.execute('PRAGMA foreign_key_check').fetchall()
    assert db.execute('SELECT COUNT(*) FROM v_ventes').fetchone()[0]==121317
    mismatch=db.execute('SELECT MAX(ABS(h.SubTotal - x.total)) FROM SalesOrderHeader h JOIN (SELECT SalesOrderID,SUM(LineTotal) total FROM SalesOrderDetail GROUP BY SalesOrderID) x ON x.SalesOrderID=h.SalesOrderID').fetchone()[0]
    assert mismatch<=.0001,mismatch
    assert db.execute('SELECT MAX(ABS(TotalDue-SubTotal-TaxAmt-Freight)) FROM SalesOrderHeader').fetchone()[0]<.0001
    assert db.execute('SELECT COUNT(*) FROM SalesOrderHeader WHERE Status != 5').fetchone()[0]==0
    result={'tables':EXPECTED,'date_min':db.execute('SELECT MIN(date(OrderDate)) FROM SalesOrderHeader').fetchone()[0],'date_max':db.execute('SELECT MAX(date(OrderDate)) FROM SalesOrderHeader').fetchone()[0],'line_revenue':db.execute('SELECT SUM(LineTotal) FROM SalesOrderDetail').fetchone()[0],'header_subtotal':db.execute('SELECT SUM(SubTotal) FROM SalesOrderHeader').fetchone()[0],'max_order_rounding_difference':mismatch,'max_line_formula_error':str(max_line_error),'cost_missing_lines':db.execute('SELECT COUNT(*) FROM v_ventes WHERE CoutUnitaireHistorique IS NULL').fetchone()[0],'join_rows':121317,'integrity':'ok','foreign_key_errors':0,'sqlite_version':sqlite3.sqlite_version}
    # Reconciliation des vues catégorielles et territoriales avec les détails, hors taxes et fret.
    for dimension in ['Categorie','Territoire','SegmentClient']:
        total=db.execute('SELECT SUM(total) FROM (SELECT SUM(Revenu) total FROM v_ventes GROUP BY '+dimension+')').fetchone()[0]
        assert abs(total-result['line_revenue'])<.001
    (ROOT/'reports'/'controles.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    with (ROOT/'collected'/'dictionnaire.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(dictionary[0]));w.writeheader();w.writerows(dictionary)
    db.close();print(json.dumps(result,indent=2))
if __name__=='__main__':main()
