import pdfplumber
import pandas as pd
import re

pdf_path = "24073001397364CBIN_ChallanReceipt.pdf"
excel_path = "Bank_Statement.xlsx"

def is_float(value):
	value = value.replace(',','')
	if value is None:
		return False
	try:
		
		return float(value)
	except:
		return False

def extract_statement_lines(lines):
    statement_lines = []
    
    # Regex pattern
    pattern = re.compile(r"(\d{2} \w{3} \d{2})\s+([A-Z\s]+)\s+([A-Za-z0-9\s]+)?\s+([\d,\.]+)?\s+([\d,\.]+)?\s+([\d,\.]+)")
    
    pattern = re.compile(r"(\d{2} \w{3} \d{2})\s")

    tran=[]
    bal=0
    tr=0
    dd=0
    cr=0
    for i in range(0,len(lines)):
    	dd=0
    	cr=0
    	line = lines[i]
    	match = pattern.search(line)
    	# print(line.split(" "))
    	# print('---------------')
    	try:
    		if tran[0] != '':
    			l_sp = line.split(" ")
    			if l_sp[0] == 'DD' or l_sp[0] == 'CR':
    				tran[1]=l_sp[0]
    			if is_float(l_sp[-1]) and is_float(l_sp[-2]):
    				tr=is_float(l_sp[-2])
    				if tran[1] == 'DD':
    					dd=tr
    				if tran[1] == 'CR':
    					cr=tr
    				l_sp[-1]=''
    				l_sp[-2]=''
    				# bal=is_float(l_sp[-1])
    				tran[2] = tran[2] + ' ' + ' '.join(l_sp)
    				statement_lines.append([tran[0],tran[1],tran[2],dd,cr,bal])
    				
    				continue
    			if is_float(l_sp[-1]):
    				tr=is_float(l_sp[-1])
    				if tran[1] == 'DD':
    					dd=tr
    				if tran[1] == 'CR':
    					cr=tr
    				l_sp[-1]=''
    				l_sp[-2]=''
    				# bal=is_float(l_sp[-1])
    				tran[2] = tran[2] + ' ' + ' '.join(l_sp)
    				statement_lines.append([tran[0],tran[1],tran[2],dd,cr,bal])
    				
    				continue


    	except Exception as e:
    		tran=[]
    		bal=0
    		tr=0
    		dd=0
    		cr=0

    	if match:
    		l_sp = line.split(" ")
    		# print(l_sp[-1])
    		if l_sp[3] == 'DD' or l_sp[3] == 'CR' or l_sp[3] == 'BALANCEBROUGHTFORWARD' or l_sp[3] == 'BALANCECARRIEDFORWARD':
	    		if is_float(l_sp[-1]):
	    			tr=is_float(l_sp[-1])
	    			l_sp[-1]=''
	    		if l_sp[-1] == '' and is_float(l_sp[-2]):
	    			tr=is_float(l_sp[-2])
	    			l_sp[-2]=''
	    		if is_float(l_sp[-1]) and is_float(l_sp[-2]):
	    			tr=is_float(l_sp[-1])
	    			bal=is_float(l_sp[-2])
	    			l_sp[-1]=''
	    			l_sp[-2]=''


    		tran=[l_sp[0]+'/'+l_sp[1]+'/'+l_sp[2],l_sp[3]]
    		tran.append(" ".join(l_sp[4:]))

    		if l_sp[3] == 'BALANCEBROUGHTFORWARD' or l_sp[3] == 'BALANCECARRIEDFORWARD':
    			statement_lines.append([tran[0],tran[1],dd,cr,tr])
    			tran=[]
    			bal=0
    			tr=0
    			dd=0
    			cr=0
    			continue
    		# print(statement_lines)
    		# statement_lines.append(match.groups())

    return statement_lines

statements = []
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        lines = page.extract_text().split("\n") if page.extract_text() else []
        statements.extend(extract_statement_lines(lines))

print('-'*90)
for statement in statements:
	pass
	print(statement[-5],statement[-3],statement[-2],statement[-1])
# Convert extracted data to DataFrame
# columns = ["Date", "Transaction Type", "Details", "Paid Out", "Paid In", "Balance"]
# df = pd.DataFrame(statements, columns=columns)

# # Save to Excel
# df.to_excel(excel_path, index=False)

# print(f"Bank statement extracted and saved to: {excel_path}")
