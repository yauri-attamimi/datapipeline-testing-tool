import csv
import sys, getopt
import pandas as pd
import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
  parser = ConfigParser()
  parser.read(filename)

  db = {}
  if parser.has_section(section):
    params = parser.items(section)
    for param in params:
      db[param[0]] = param[1]
  else:
    raise Exception('Section {0} not found in the {1} file'.format(section, filename))

  return db


def connect():
  conn = None
  try:
    params = config()
    print('Connecting to our devdatapipeline PostgreSQL database...')
    conn = psycopg2.connect(**params)
    return conn
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)

def close_connection(conn):
  if conn is not None:
    print('Closing database connection...')
    conn.close()

def read_csv():
  conn = connect()
  with open('data.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0    
    records = []
    for row in csv_reader:
      records.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
      line_count += 1

    sql = """INSERT INTO driver_daily_metrics(date, drn, net_earnings, trips, supply_hours, km_driven, acceptance_rate, cancellation_rate)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""    
    cur = conn.cursor()
    try:
      cur.executemany(sql, records)
      conn.commit()
      print("%d number of records have been successfully inserted into the database." % line_count)
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      cur.close()

  print(f'Processed {line_count} of rows.')
  close_connection(conn)

def main(argv):
  inputfile = ''
  try:
    opts, args = getopt.getopt(argv, "hi:", ["ifile="])
  except getopt.GetOptError:
    print('pipeline_tester.py -i <inputfile>')
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print('pipeline_tester.py -i <inputfile>')
      sys.exit()
    elif opt in ("-i", "--ifile"):
      inputfile = arg

  print('Reading data from "', inputfile, '"')
  xl_file = pd.ExcelFile(inputfile)
  conn = connect()        
  for sheet_name in xl_file.sheet_names:
    print('Processing', sheet_name)
    df = pd.read_excel(inputfile, sheet_name)
    print('Processing records for this column headings:')
    print(df.columns)
    i = 0
    sql = """INSERT INTO test_driver_daily_metrics(date, drn, net_earnings, trips, supply_hours, km_driven, acceptance_rate, cancellation_rate)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
    records = df.values.tolist()
    cur = conn.cursor()
    try:
      cur.executemany(sql, records)
      conn.commit()
      print("%d number of records have been successfully inserted into the database." % len(df.index))
    except (Exception, psycopg2.DatabaseError) as error:
      print(error)
    finally:
      cur.close()

  close_connection(conn)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print('usage: pipeline_tester.py -i <inputfile>')
    sys.exit(1)

  main(sys.argv[1:])
