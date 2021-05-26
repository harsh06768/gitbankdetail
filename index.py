DB_HOST  = "b3gpddyhj9qmcm0s4izt-postgresql.services.clever-cloud.com"  
DB_NAME = "b3gpddyhj9qmcm0s4izt"
DB_USER = "ulztggfbvw7ayutdq5vw"
DB_PASS = "DgUYvZ9m4ReVunKykGcX"


from logging import debug
from flask import Flask ,  jsonify, request 
import psycopg2

conn= psycopg2.connect(dbname=DB_NAME, user=DB_USER, password= DB_PASS, host=DB_HOST)
cur= conn.cursor()

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Enter the valid endpoint  to get the result => Example: "http://127.0.0.1:5000/api/branches/autocomplete?q=PATNA&limit=3&offset=0"'         

#endpoint for the branch 
@app.route('/api/branches/autocomplete', methods=['GET'])
def get_mul():
    
        q = request.args.get('q')
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if q or limit :
            #conn= psycopg2.connect(dbname=DB_NAME, user=DB_USER, password= DB_PASS, host=DB_HOST)
            #cur= conn.cursor()
            cur.execute(" SELECT * FROM branches WHERE branch=%s ORDER BY ifsc ASC LIMIT %s OFFSET %s;", (q,limit,offset))
            row = cur.fetchall()

            branch =[]
            content = {}
            for result in row:
                content  = {'"ifsc"': result[0],'"bank_id"': result[1], '"branch"': result[2],'"address"': result[3], '"city"': result[4],'"district"': result[5], '"state"': result[6] }
                branch.append(content)
                content = {}
            
            return jsonify({'"branches"':branch}) 

        else:
            resp= jsonify('Error Possible Reason :1. Input params invalid or Null  \n 2. Branch not found in database')  
            resp.status_code = 500
            return resp 

    


# endpoint for the city 
@app.route('/api/city', methods=['GET'])
def get_jal():
    
        q = request.args.get('q')
        limit = request.args.get('limit')
        #offset = request.args.get('offset')
        
        if q or limit :
            
            cur.execute(" SELECT * FROM branches WHERE city=%s ORDER BY ifsc ASC LIMIT %s;", (q,limit))
            row = cur.fetchall()

            branch =[]
            content = {}
            for result in row:
                content  = {'"ifsc"': result[0],'"bank_id"': result[1], '"branch"': result[2],'"address"': result[3], '"city"': result[4],'"district"': result[5], '"state"': result[6] }
                branch.append(content)
                content = {}
            
            return jsonify({'"branches"':branch}) 

        else:
            resp= jsonify('Error Possible Reason :1. Input params invalid or Null  \n 2. city not found in database')  
            resp.status_code = 500
            return resp 


   








if __name__ == "__main__":
    app.run(debug=True)    

