import re,csv,argparse

parser = argparse.ArgumentParser()
parser.add_argument('txeqRulesCSV', help='CSV file containing rules content',type=str)
args = parser.parse_args()

fileName = args.txeqRulesCSV
outputFileName = 'output.csv'

with open(fileName,'rb') as f:
    reader = csv.reader(f)
    ekm_list = list(reader)

#Create field names in the output CSV
with open(outputFileName,'a') as a:
    writer = csv.writer(a,delimiter=',')
    writer.writerow(['module_name','maint_validation','version','data_type','section','synonym_type','synonym_value','order_sentence'])
a.close()

for row in ekm_list:
    for field in row:
        primaries = re.findall(r'whose\sprimary\smnemonic\sis\s.*?d\d\d\d\d\d\s(.*?)\s2516',field)
        for primary in primaries:
            with open(outputFileName,'a') as a:
                writer = csv.writer(a,delimiter=',')
                writer.writerow([row[0],row[1],row[2],row[3],row[4],'Primary',primary])
            a.close()
for row in ekm_list:
    for field in row:
        synonyms = re.findall(r'that\swas\sordered\sas\s\d.*?\d\d\d[\d|\.0]*?\s(.*?)\s2516',field)
        for synonym in synonyms:
            with open(outputFileName,'a') as a:
                writer = csv.writer(a,delimiter=',')
                writer.writerow([row[0],row[1],row[2],row[3],row[4],'Synonym',synonym])
            a.close()
for row in ekm_list:
    for field in row:
        action_template_synonyms = re.findall(r'\d\\T([^o\\xyrhea].*?)\\S\d*?\\M(.*?)\\C',field)
        for synonym in action_template_synonyms:
            with open(outputFileName,'a') as a:
                writer = csv.writer(a,delimiter=',')
                writer.writerow([row[0],row[1],row[2],row[3],row[4],'Synonym',synonym[1],synonym[0]])
            a.close()
