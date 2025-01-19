import pandas as pd
import pytest
from unittest import mock
import shutil
from project import ProductionData, OliveOilProduction

#Fixture which allows us to set up test data
@pytest.fixture
def setup_test_data():
    file = 'C:/Users/Rayza/OneDrive/Desktop/python_project/proj_root/olive_oil_census2020.csv'
    test_file = 'test_olive_oil_census2020.csv'
    
    #Create a copy of the dataset file
    shutil.copyfile(file, test_file)

    # Create an instance of ProductionData and override _read_csv and _write_csv
    production_data = ProductionData()
    production_data._read_csv = lambda: pd.read_csv(test_file).to_dict(orient='records')
    production_data._write_csv = lambda rows: pd.DataFrame(rows).to_csv(test_file, index=False, encoding='utf-8')

    return production_data

def test_read_csv(setup_test_data):
    production_data = setup_test_data
    rows = production_data._read_csv()
    assert len(rows) > 0

def test_add_production(setup_test_data):
    production_data = setup_test_data
    rows = production_data._read_csv()
    initial_len = len(rows)
    
    # Create a new olive oil production record
    new_record = OliveOilProduction(
        prod_ID=786,
        year='2021',
        unit_type='Industrial',
        extraction_type='Others',
        region_name='Alentejo',
        olive_quant_ton='103',
        oil_press_num='3',
        oil_prod_hl='65'
    )

    #Add record to rows and write inside csv file
    rows.append(new_record.to_dict())
    production_data._write_csv(rows)
    updated_rows = production_data._read_csv()

    #Check record is created
    assert len(updated_rows) == initial_len + 1
    assert any(row['prod_ID'] == 786 for row in updated_rows)

def test_find_production_by_ID(setup_test_data):
    production_data = setup_test_data
    find_inputs = ['515']
 
    #Mock user input and activate function
    with mock.patch('builtins.input', side_effect=find_inputs):
        result = production_data.find_production_by_ID(
            prod_ID=int(find_inputs[0]))
        #Check that record has been found
        assert result is True

    #Check record exists in the data  
    rows = production_data._read_csv()
    assert any(row['prod_ID'] == int(find_inputs[0]) for row in rows)

def test_find_production_by_ID_fail(setup_test_data):
    production_data = setup_test_data
    find_inputs = ['840']

    with mock.patch('builtins.input', side_effect=find_inputs):
        result = production_data.find_production_by_ID(
            prod_ID=int(find_inputs[0]))
        #Check that record has not been found
        assert result is False

    rows = production_data._read_csv()
    assert not any(row['prod_ID'] == int(find_inputs[0]) for row in rows)

def test_find_production(setup_test_data):
    production_data = setup_test_data

    find_inputs = [
        '2015',
        'Industrial', 
        'Continuous three phases', 
        'Alentejo']

    with mock.patch('builtins.input', side_effect=find_inputs):
        result = production_data.find_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3])
        # Check that record has been found
        assert result is True   

    #Check record data matches the criteria
    rows = production_data._read_csv()
    assert any(
        row['year'] == int(find_inputs[0]) and
        row['unit_type'] == find_inputs[1] and
        row['extraction_type'] == find_inputs[2] and
        row['region_name'] == find_inputs[3]
        for row in rows)

def test_find_production_fail(setup_test_data):
    production_data = setup_test_data

    find_inputs = [
	'2018', 
	'Industrial', 
	'Continuous three phases', 
	'Madeira']

    with mock.patch('builtins.input', side_effect=find_inputs):
        result = production_data.find_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3])
        
        #Check that record has not been found
        assert result is False 

def test_update_production(setup_test_data):
    production_data = setup_test_data

    find_inputs = [
        '2020', 
        'Private', 
        'Continuous three phases', 
        'Alentejo']
    update_inputs = ['1800', '8', '3000']

    #Mock find and update inputs together and activate function
    with mock.patch("builtins.input", side_effect=find_inputs + update_inputs):
        update = production_data.update_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3],
            olive_quant_ton=float(update_inputs[0]),
            oil_press_num=int(update_inputs[1]),
            oil_prod_hl=float(update_inputs[2])
        )
        # Check that record has been updated
        assert update is True

    rows = production_data._read_csv()

    #Check that record updated data matches the user input
    assert any(
    row['olive_quant_ton'] == float(update_inputs[0])
    and row['oil_press_num'] == int(update_inputs[1])
    and row['oil_prod_hl'] == float(update_inputs[2]) 
    for row in rows)

def test_update_production_fail(setup_test_data):
    production_data = setup_test_data

    find_inputs = [
        '2018',
        'Private',
        'Continuous three phases',
        'Portugal']
    update_inputs = ['1800','8','3000']

    #Mock find and update inputs together and activate function
    with mock.patch("builtins.input", side_effect=find_inputs + update_inputs):
        update = production_data.update_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3],
            olive_quant_ton=float(update_inputs[0]),
            oil_press_num=int(update_inputs[1]),
            oil_prod_hl=float(update_inputs[2])
        )
        # Check that record has not been updated
        assert update is False

def test_delete_production(setup_test_data):
    production_data = setup_test_data
    find_inputs = [
        '2020',
        'Industrial',
        'Continuous three phases',
        'Alentejo']

    with mock.patch("builtins.input", side_effect=find_inputs):
        delete = production_data.delete_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3])
        # Check that record has been deleted
        assert delete is True

    # Check that record data matches criteria
    rows = production_data._read_csv()

    assert not any(
        row['year'] == int(find_inputs[0]) and
        row['unit_type'] == find_inputs[1] and
        row['extraction_type'] == find_inputs[2] and
        row['region_name'] == find_inputs[3]
        for row in rows
    )

def test_delete_production_fail(setup_test_data):
    production_data = setup_test_data
    find_inputs = [
        '2017', 
        'Industrial', 
        'Traditional', 
        'Madeira']

    with mock.patch("builtins.input", side_effect=find_inputs):
        delete = production_data.delete_production(
            year=int(find_inputs[0]),
            unit_type=find_inputs[1],
            extraction_type=find_inputs[2],
            region_name=find_inputs[3])
        
        # Check that record has not been deleted
        assert delete is False