import csv

def write_csv(list):
    out = open('hash.csv','a', newline='')
    csv_write = csv.writer(out,dialect='excel')
    csv_write.writerow(list)
