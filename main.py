import csv_conversion_functions as convert
import sys

def main():
    l = convert.batch_results_to_hit_results(sys.argv[1])
    for i in l:
        print i, "\n"
    
if __name__ == "__main__":
    main()