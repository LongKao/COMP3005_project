def signup(cur, conn):
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

def signin(cur):
    username = input("Enter username: ")
    password = input("Enter password: ")
    cur.execute("SELECT * FROM users WHERE username = '{0}' AND password = '{1}'".format(username,password))
    result = cur.fetchone()
    if(result==None):
        return False, None
    else:
        return True, int(result[0])

def Main_session(cur,conn,uid):
    print("Please select an option:\n\n1. Browse/place order\n2. Log out")
    choice = int(input("\n"))
    if(choice==1):
        browse(cur,conn,uid)

def browse(cur,conn,uid):
    cart =[]
    total = 0
    while(True):
        print("Please select an option:\n\n1. Browse by author\n2. Browse by genre\n3. Browse by publisher\n4. Browse by ISBN\n5. List all available books\n6. Add a book in cart\n7. Place order\n8. Track order\n9. Log out")
        choice = int(input("\n"))
        if(choice==1):
            author = input("Enter Author's name: ")
            cur.execute("select * from book natural join stock where author = '%s'" %author)
            conn.commit()
            print("\nBooks by %s:\n" %author)
            print(cur.fetchall())
            input("\nPress to continue...\n")
        elif(choice==2):
            genre = input("Enter genre: ")
            cur.execute("select * from book natural join stock where genre = '%s'" %genre)
            conn.commit()
            print("\n%s books:\n" %genre)
            print(cur.fetchall())
            input("\nPress to continue...\n")
        elif(choice==3):
            publisher = input("Enter publisher: ")
            cur.execute("select * from book natural join stock where publisher = '%s'" %publisher)
            conn.commit()
            print("\nBooks published by %s:\n" %publisher)
            print(cur.fetchall())
            input("\nPress to continue...\n")
        elif(choice==4):
            isbn = input("Enter ISBN: ")
            cur.execute("select * from book natural join stock where ISBN = '%s'" %isbn)
            conn.commit()
            print("\nBooks with ISBN of %s:\n" %isbn)
            print(cur.fetchall())
            input("\nPress to continue...\n")
        elif(choice==5):
            print("All available books:\n")
            cur.execute("select * from book natural join stock")
            conn.commit()
            print(cur.fetchall())
            input("\nPress to continue...\n")
        elif(choice==6):
            
            while(True):
                choice = input("Enter title of a book to add to cart. To exit enter (e): \n")
                if(choice=="e"):break
                else:
                    cur.execute("select * from book natural join stock where name = '%s'" %choice)
                    result = cur.fetchone()
                    if(result==None):
                        print("Book is not available\n")
                    else:
                        print("Book is added to the cart\n")
                        cart.append(choice)
                        total = total+result[6]
        elif(choice==7):
            if(len(cart)==0):
                print("No books in the cart\n")
                input("Press to continue...\n")
            else:
                print("Your current cart: \n")
                for i in cart:
                    cur.execute("select author, name, genre, price from book natural join stock where name = '%s'"%i)
                    conn.commit()
                    result = cur.fetchone()
                    print(result)
                print("Your total is: %s\n" %total)
                finilize = int(input("Would you like to (1) checkout or (2) keep browsing?\n"))
                if(finilize == 1):
                    shipping_address = input("\nPlease enter you shipping address: ")
                    billing_address = input("\nPlease enter your billing_address: ")
                    cur.execute("SELECT * FROM orders")
                    cur.fetchall()
                    id = int(cur.rowcount)+1
                    book_list = ""
                    for i in cart:
                        book_list = book_list + i + ', '
                    book_list = book_list[:len(book_list)-2]
                    cur.execute("insert into orders values({0},{1},'{2}','{3}','{4}',{5})".format(id,uid,book_list,shipping_address,billing_address,total))
                    conn.commit()
                    addToOrderBook(cur,conn,cart)
                    cart = []
                    total = 0
                    print("Your order has been placed!\n")
                    input("Press to continue...\n")
                elif(finilize==2):continue
        elif(choice==8):
            cur.execute("select * from orders where uid = '{0}'".format(uid))
            result = cur.fetchall()
            if(result==[]):
                print("No orders available\n")
                input("Press to continue...\n")
            else:
                print("Current order('s): \n")
                print(result)
                input("\nPress to continue...\n")
        elif(choice==9):
            break
        else:
            print("Invalid input\n")
    
def addToOrderBook(cur,conn,cart):
    for i in cart:
        cur.execute("SELECT * FROM order_book")
        cur.fetchall()
        id = int(cur.rowcount)+1
        cur.execute("select author, name, genre, publisher, price, ISBN from book where name = '%s'"%i)
        result = cur.fetchall()
        print(result)
        cur.execute("insert into order_book values({0},'{1}','{2}','{3}','{4}',{5})".format(id,result[0][0],result[0][1],result[0][2],result[0][3],result[0][4]))
        conn.commit()
        cur.execute("update stock set quantity = quantity-1 where isbn = '%s'"%result[0][5])
        conn.commit()