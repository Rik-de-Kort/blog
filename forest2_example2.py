from datetime import date
import os
import pandas as pd
import pyodbc

def calculate_waterfall(emissions, enterprise_value, emissions_subsector, enterprise_value_subsector, emissions_sector, enterprise_value_sector):
  if emissions is not None:
    emissions = emissions
    mapping_level = 'DATA'
  elif emissions_subsector is not None:
    emissions = emissions_subsector / enterprise_value_subsetor * enterprise_value
    mapping_level = 'SUBSECTOR'
  elif emissions_sector is not None:
    emissions = emissions_sector / enterprise_value_sector * enterprise_value
    mapping_level = 'SECTOR'
  else:
    emissions = None
    mapping_level = 'NO MAPPING'

  return emissions, mapping_level

def query(cur: pyodbc.Cursor, sql: str, data):
  results = cur.execute(sql, data)
  names = [name for name, *_ in cur.description]
  return [dict(zip(names, row)) for row in results]

def read_portfolio(cur: pyodbc.Cursor, portfolio_name):
  return query(
    cur,
    'select * from table1 join table2 on table1.sedol = table2.securityid where table2.pfname = ?',
    (portfolio_name,)
  )

def read_medians(cur: pyodbc.Cursor):
  medians = query(
    cur,
    'select * from median_data'
  )
  subsector = {r['subsector']: (r['emissions'], r['enterprise_value']) for r in medians} 
  sector = {r['sector']: (r['emissions'], r['enterprise_value']) for r in medians}
  return subsector, sector

def calculate_carbon(portfolio_data, subsector_data, sector_data):
  for row in portfolio_data:
    subsector_data = subsector_medians.get(row['subsector'], {})
    sector_data = sector_medians.get(row['sector'], {})
    row['emissions'], row['mapping_level'] = calculate_waterfall(
      row['emissions'], row['enterprise_value'],
      subsector_data.get('emissions'), subsector_data.get('enterprise_value'),
      sector_data.get('emissions'), sector_data.get('enterprise_value'),
    )
  return portfolio_data


portfolios = ['listed_equities', 'real_estate', 'credits']

with pyodbc.connect(os.environ['PYODBC_CONNECTION_STRING']) as conn:
  with conn.cursor() as cur:
    portfolio_data = [row for portfolio in portfolios for row in read_portfolio(cur, portfolio)]
    subsector_medians, sector_medians = read_medians(cur)

results = calculate_carbon(portfolio_data, subsector_medians, sector_medians)

pd.DataFrame(results).to_excel(f'{date.today().isoformat()}_carbon.xlsx')
