from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
import xml.etree.ElementTree as ET
import pandas as pd
import tempfile

app = FastAPI()

def parse_tally_xml(file_path):
    transactions = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    for voucher in root.findall('.//VOUCHER'):
        voucher_type = voucher.find('VOUCHERTYPENAME').text if voucher.find('VOUCHERTYPENAME') is not None else ""
        
        if voucher_type == "Receipt":
            voucher_number = voucher.find('VOUCHERNUMBER').text if voucher.find('VOUCHERNUMBER') is not None else "NA"
            parent_amount = 0
            children = []
            
            for ledger_entry in voucher.findall('.//ALLLEDGERENTRIES.LIST'):
                ledger_name = ledger_entry.find('LEDGERNAME').text if ledger_entry.find('LEDGERNAME') is not None else "NA"
                amount = float(ledger_entry.find('AMOUNT').text) if ledger_entry.find('AMOUNT') is not None else 0
                parent_amount += amount
                
                child_transaction = {
                    'Transaction Type': 'Child',
                    'Vch No.': voucher_number,
                    'Vch Type': 'Receipt',
                    'Ref No.': 'NA',
                    'Ref Type': 'NA',
                    'Ref Date': 'NA',
                    'Debtor and Particulars': ledger_name,
                    'Ref Amount': amount,
                    'Amount': 'NA',
                    'Amount Verified': 'NA'
                }
                transactions.append(child_transaction)
            
            parent_transaction = {
                'Transaction Type': 'Parent',
                'Vch No.': voucher_number,
                'Vch Type': 'Receipt',
                'Ref No.': 'NA',
                'Ref Type': 'NA',
                'Ref Date': 'NA',
                'Debtor and Particulars': 'NA',
                'Ref Amount': 'NA',
                'Amount': parent_amount,
                'Amount Verified': 'Yes' if parent_amount == sum(t['Ref Amount'] for t in transactions if t['Transaction Type'] == 'Child' and t['Vch No.'] == voucher_number) else 'No'
            }
            transactions.insert(-len(children), parent_transaction)
    
    return transactions

def generate_excel(transactions, output_file):
    df = pd.DataFrame(transactions)
    df.to_excel(output_file, index=False)

@app.post("/generate-response/")
async def generate_response(file: UploadFile):
    if file.content_type != "application/xml":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an XML file.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_excel:
        # Save the uploaded XML file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_xml:
            temp_xml.write(await file.read())
            temp_xml.seek(0)
            
            # Parse the XML and generate the Excel
            transactions = parse_tally_xml(temp_xml.name)
            generate_excel(transactions, temp_excel.name)
        
        return FileResponse(temp_excel.name, filename="response_file.xlsx")
