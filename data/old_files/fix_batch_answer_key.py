import json
import csv
import sys

def main():
    #open input and qualified workers .csv files
    results = csv.reader(open(sys.argv[1], 'rU'), delimiter = ",")
    writer = csv.writer(open(sys.argv[2], 'wb'), delimiter = ",")
    
    for row in results:
        try:
            if row[0] == "337F8MIIMZYWOTYYBADHICIZVLJ04Z" or row[0] == "3X4Q1O9UBH7EAX80FTDZBPYRK0QO7I":
                row[35] = "0-7 1-5 1-6 1-8 1-9 2-5 2-6 2-8 2-9 3-5 3-6 3-8 3-9 4-0 5-1 6-2 7-3 7-4 8-3 8-4 9-3 9-4 10-10"
            
            if row[0] == "3MZ3TAMYTL8EWUHCQCY0W9T59TJRI3" or row[0] == "3XUSYT70ITM9OPHR4LEALGC588DD0A":
                row[35] = "{}"
                row[36] = "0-0 0-1 1-0 1-1"
            
            if row[36] == "[]" or not row[36] :
                row[36] = "{}"
            
            if row[37] == "[]" or not row[37] :
                row[37] = "{}"
                
            if row[38] == "[]" or not row[38]:
                row[38] = "{}"
        
            print(row)
            writer.writerow(row)
        except:
            pass
    
    return
    
    
if __name__ == "__main__":
    main()