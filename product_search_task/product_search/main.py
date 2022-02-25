from flask import Flask
from numpy import outer
import pandas as pd 
import sqlite3 as sql
import subprocess 
import os 
app = Flask(__name__)

@app.route('/')
def product_app():
    #current_location=os.getcwd()+"/product_search"
    # reading dataframe
    ## This could have been dynamic but for time being I am only showing dataframe as html
    try:
        #reading from the database
        conn=sql.connect(current_location+'/Database/product_details.db')
        df=pd.read_sql("SELECT * FROM product_details", conn)
        df=df.loc[:, df.columns!='index']
        return df.to_html()
    except Exception as e:
        print(f'Exception: {e}')
        return "<h1>Error in Code</h1>"
  
# main function
if __name__ == '__main__':
    # running the search operation and creating database
    current_location=os.getcwd()+"/product_search"
    
    try:
        subprocess.call(['sh',current_location+'/spiders/run_scripts.sh'])
    except Exception as e:
        print(f'Exception: {e}')
        
    app.run(host='0.0.0.0',port=5432)
