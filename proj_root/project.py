import pandas as pd

class OliveOilProduction:

    def __init__(self,prod_ID, year, unit_type, extraction_type, region_name, olive_quant_ton, oil_press_num, oil_prod_hl):
        self.prod_ID = prod_ID
        self.year = year
        self.unit_type = unit_type
        self.extraction_type = extraction_type
        self.region_name = region_name 
        self.olive_quant_ton = olive_quant_ton
        self.oil_press_num = oil_press_num
        self.oil_prod_hl = oil_prod_hl

    def to_dict (self):
        return {
            'prod_ID' : self.prod_ID,
            'year': self.year,
            'unit_type' : self.unit_type,
            'extraction_type' : self.extraction_type,
            'region_name' : self.region_name,
            'olive_quant_ton' : self.olive_quant_ton,
            'oil_press_num' : self.oil_press_num,
            'oil_prod_h' : self.oil_prod_hl 
            }
        

class ProductionData:
    field_names = [
        'prod_ID',
        'year',
        'unit_type',
        'extraction_type',
        'region_name',
        'olive_quant_ton',
        'oil_press_num',
        'oil_prod_hl'
        ]
    
    def __init__(self, file_path='proj_root/olive_oil_census2020.csv'):
        self.file_path = file_path

    def _read_csv(self, file_path):
        try:
            # Read CSV using pandas
            df = pd.read_csv(file_path, encoding='utf-8')
            rows = df.to_dict(orient='records')
            return rows
        except FileNotFoundError :
            print ("File not found")
            return[]
    
    def _write_csv (self, file_path, rows):
        pd.DataFrame(rows).to_csv(file_path, index=False, encoding='utf-8')

    def count_rows(self):
        rows = self._read_csv()
        return len(rows)
        
    def add_production(self):
        print ("Enter data for the following variables:")

        # Collect input of the new record
        year = int(input("Year:"))
        unit_type = input("Oil press unit type:")
        extraction_type = input("Extraction method:")
        region_name = input("Region name:")
        olive_quant_ton = float(input("Olive quantity used (ton):"))
        oil_press_num = int(input("Number of oil presses: "))
        oil_prod_ton = float(input("Olive oil produced (hl):"))
    
        # Produce a new prod_ID
        prod_ID = self.count_rows() + 1

        production= OliveOilProduction(
            prod_ID= prod_ID,
            year= year,
            unit_type= unit_type,
            extraction_type= extraction_type,
            region_name= region_name,
            olive_quant_ton= olive_quant_ton,
            oil_press_num= oil_press_num,
            oil_prod_hl= oil_prod_ton
        )

        rows = self._read_csv()
        rows.append(production.to_dict())
        #Write new record to cvs
        self._write_csv(rows)
        print(f"New production added with prod_ID: {prod_ID}")

    def find_production_by_ID(self, prod_ID):
        rows = self._read_csv()

        #Filtering for record with prod_ID input criteria
        target_row= [row for row in rows if(
            row['prod_ID'] == prod_ID)]
        
        # If a record with input criteria exists, return matching record
        if len(target_row) == 1:
            self._write_csv(target_row)
            print("Record found.")
            return True
        else:
            # If the criteria doesn't match   
            print("Production ID not valid")
            return False

    def find_production(self, year, unit_type, extraction_type, region_name):
        rows = self._read_csv()

        #Filtering for record with input criteria
        target_row = [ row for row in rows if (
                row['year'] == year 
                and row['unit_type'] == unit_type 
                and row['extraction_type']== extraction_type 
                and row['region_name'] == region_name)]

        #If a record with input criteria exists, return matching record
        if len(target_row) == 1:
            self._write_csv(target_row)
            print("Record found.")
            return True
        else:
            # If the criteria doesn't match   
            print("No matching record found")
            return False  
    
    def update_production(self, year, unit_type, extraction_type, region_name, olive_quant_ton, oil_press_num, oil_prod_hl):
        rows = self._read_csv()
    
        #Filtering for record with input criteria
        target_row = [row for row in rows if (
            row['year'] == year 
            and row['unit_type'] == unit_type 
            and row['extraction_type']== extraction_type 
            and row['region_name'] == region_name)]
        
        #If a record with input criteria exists, input these values to update
        if len(target_row) == 1:
            for row in rows:
                row['olive_quant_ton'] = olive_quant_ton
                row['oil_press_num'] = oil_press_num
                row['oil_prod_hl'] = oil_prod_hl
                
            #Write new values 
            self._write_csv(rows)
            print("Record Updated")
            return True
        #If criteria doesn't match = No records found
        elif len(target_row) < 1:
            print("No matching record found")
            return False
    
    def delete_production(self, year, unit_type, extraction_type, region_name):
        rows = self._read_csv()
    
        #Filtering for records which don't meet criteria
        not_row = [row for row in rows if not (
            row['year'] == year 
            and row['unit_type'] == unit_type 
            and row['extraction_type']== extraction_type 
            and row['region_name'] == region_name)]
        
        #Checking if the filtered rows are less the original number
        if len(not_row) < len(rows):
            self._write_csv(not_row)
            print("Record deleted")
            return True
        else:
            print("No matching record found")
            return False
 