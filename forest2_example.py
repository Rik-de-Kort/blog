from datetime import date
import os
import pandas as pd
import pyodbc


def calculate_waterfall(row):
  if not pd.isna(row['carbon_emissions']):
    row['mapping_level'] = 'DATA'
  else:
    if not pd.isna(row['carbon_emissions_subsector']):
      row['carbon_emissions'] = row['carbon_emissions_subsector'] / row['enterprise_value_sector'] * row['enterprise_value']
      row['mapping_level'] = 'SUBSECTOR'
    elif not pd.isna(row['carbon_emissions_sector']):
      row['carbon_emissions'] = row['carbon_emissions_sector'] / row['enterprise_value_sector'] * row['enterprise_value'] 
      row['mapping_level'] = 'SECTOR'
    else:
      row['mapping_level'] = 'NO MAPPING'
    return row

class CarbonCalculator:
  def __init__(
      self,
      portfolios: list[str],
      db_conn: pyodbc.Connection,
      read_portfolio_func: Callable[[self.db_conn, str], pd.DataFrame],
    ):
      self.portfolios = portfolios
      self.db_conn = db_conn
      self.read_portfolio_func = read_portfolio_func

  def fetch_portfolio_data(self):
    data = []
    for portfolio in self.portfolios:
      data.append(self.read_portfolio_func(self.db_conn, portfolio))
    return pd.concat(data)

  def fetch_median_data(self):
    if self._median_data is not None:
      return self._median_data
    with self.db_conn.cursor() as cur:
      cur.execute('select * from median_data')
      results = cur.fetchall()
      df = pd.DataFrame(cur, columns=[name for name, *_ in cur.description])
    df['median_date'] = date.today()
    rows = df.to_dict(orient='records')
    return {row['sector']: row for row in rows} | {row['subsector']: row for row in rows}

  def calculate_carbon(self):
    all_data = self.fetch_portfolio_data()
    medians = self.fetch_median_data()
    df_median = pd.DataFrame(medians.values())
    with_medians = (all_data
      .join(df_median, left_on='subsector', right_on='subsector', rsuffix='_subsector')
      .join(df_median, left_on='sector', right_on='sector', rsuffix='_sector')
    )
    rows = with_medians.to_dict(orient='records')
    result = []
    for row in rows:
      result.append(calculate_waterfall(row))
    self.carbon_results = result

def read_portfolio_from_db(conn: pyodbc.Connection, portfolio_name: str):
  with conn.cursor() as cur:
    results = cur.execute(
      'select * from table1 join table2 on table1.sedol = table2.securityid where table2.pfname = ?',
      portfolio_name
    ).fetchall()
    names = [name for name, *_ in cur.description]
  return pd.DataFrame(results, columns=names)

conn = pydobc.connect(os.environ['PYODBC_CONNECTION_STRING'])
calculator = CarbonCalculator(
  ['listed_equities', 'real_estate', 'credits'],
  conn,
  read_portfolio_from_db,
)
calculator.calculate_carbon()
results_df = pd.DataFrame(calculator.carbon_results)
results_df.to_excel(f'{date.today().isoformat()}_carbon.xlsx')

