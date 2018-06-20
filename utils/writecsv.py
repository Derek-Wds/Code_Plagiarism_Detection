import csv

def write_csv(list, file):
    out = open(file,'a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    csv_write.writerow(list)
