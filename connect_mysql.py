import sshtunnel
import json
import mysql.connector
import MySQLdb

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0
with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='Bullopear', ssh_password='pythonpassword',
    remote_bind_address=('Bullopear.mysql.pythonanywhere-services.com', 3306)
    ) as tunnel:
    connection = MySQLdb.connect(
    user='Bullopear',
    passwd='dbpassword',
    host='127.0.0.1', port=tunnel.local_bind_port,
    db='Bullopear$DAILYOI_change',)
    cursor=connection.cursor()
    query = f"SELECT records, filtered FROM NIFTY WHERE date = (SELECT MAX(date) FROM NIFTY ORDER BY filtered DESC LIMIT 1);"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    records=json.loads(result[0][0])
    filtered=json.loads(result[0][1])
    result_dict={'records':records, 'filtered':filtered}
    fetched_data=result_dict
    time = fetched_data['records']['timestamp']

print(time)