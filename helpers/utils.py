import csv

def results_to_csv(csv_path: str,
                    *columns):
        
        data = columns

        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)