import psycopg2
import Owner
import User

hostname = 'localhost'
database = 'project'    #input your own database name here
username = 'postgres'
pwd = ''  #input your own password for pgAdmin4
port_id = 5432
cur = None
conn = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )

    cur = conn.cursor()

    logged_in = False
    while(True):
        print("---Welcome to Look Inna Book!---\n\nPlease select an option: \n 1. Sign up\n 2. Sign in\n 3. Sign in as owner")
        choice = int(input())
        if(choice==1):
            cur.execute("SELECT * FROM users")
            cur.fetchall()
            id = int(cur.rowcount)+1
            name = input("Enter your name: ")
            username = input("Enter your username: ")
            password = input("Enter new password: ")
            shipping_address = input("Enter your shipping address: ")
            billing_address = input("Enter your billing address: ")
            cur.execute("insert into users values({0}, '{1}', '{2}', '{3}', '{4}', '{5}');".format(id,name,username,password,shipping_address,billing_address))
            conn.commit()
        elif(choice==2):
            logged_in,uid = User.signin(cur)
            if(logged_in==True):
                print("Successful authorization")
                print("User's id: "+str(uid))
                User.Main_session(cur,conn,uid)
            else:
                print("Invalid username or password")
        elif(choice==3):
            username = input("Enter username: ")
            password = input("Enter password: ")
            cur.execute("SELECT * FROM owner WHERE username = '{0}' AND password = '{1}'".format(username,password))
            if(cur.fetchone()==None):
                print(cur.fetchone())
                print("Invalid username or password")
            else:
                print(cur.fetchone())
                print("Successful authorization")
                Owner.owner(cur, conn)
                #logged_in = True
        else:
            print("Invalid input")

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()