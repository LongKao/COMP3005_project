def owner(cur, conn):
    while(True):
        print("---Welcome to Administration!---\n\nPlease select an option: \n1. Add a new book\n2. Remove a book\n3. Add a new publisher\n4. Access sales report\n5. Log out")
        choice = int(input())
        print('\n')
        if(choice==1):
            isbn = input("Enter book's ISBN: ")
            author = input("Enter book's author: ")
            name = input("Enter book's titel: ")
            genre = input("Enter books genre: ")
            publisher = input("Enter pbulisher: ")
            page_num = input("Enter number of pages: ")
            price = input("Enter book's price: ")
            cur.execute("insert into book values('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6})".format(isbn, author, name, genre, publisher, page_num, price))
            conn.commit()
        elif(choice==2):
            isbn = input("Enter ISBN of a book you want to remove: ")
            cur.execute("delete from book where ISBN = '{0}'".format(isbn))
            conn.commit()
        elif(choice==3):
            cur.execute("SELECT * FROM publisher")
            cur.fetchall()
            id = int(cur.rowcount)+1
            name = input("Enter publisher's name: ")
            address = input("Enter publisher's address")
            email = input("Enter publisher's email")
            phone_num = input("Enter pbulisher's phone number: ")
            bank_account = input("Enter publisher's bank information")
            cur.execute("insert into publisher values({0},{1},{2},{3},{4},{5}".format(id,name,address,email,phone_num,bank_account))
            conn.commit()
        elif(choice==4):
            report(cur,conn)
        elif(choice==5):
            break
        else:
            print("Invalid input\n\n")

def report(cur,conn):    
    total_sales = 0
    while(True):
        print("1. Show total sales\n2. Show sales per genre\n3. Show sales per author\n4. Show sales per publisher\n5. Exit\n")
        choice = int(input())
        if(choice==1):
            cur.execute("select total_cost from orders")
            result = cur.fetchall()
            for i in result:
                total_sales = total_sales+i[0]
            print("\n"+str(total_sales))
            input("\nPress to continue...\n")
        elif(choice==2):
            cur.execute("SELECT genre, SUM (price) FROM order_book GROUP BY genre;")
            result = cur.fetchall()
            print(result)
            input("\nPress to continue...\n")
        elif(choice==3):
            cur.execute("SELECT author, SUM (price) FROM order_book GROUP BY author;")
            result = cur.fetchall()
            print(result)
            input("\nPress to continue...\n")
        elif(choice==4):
            cur.execute("SELECT publisher, SUM (price) FROM order_book GROUP BY publisher;")
            result = cur.fetchall()
            print(result)
            input("\nPress to continue...\n")
        elif(choice==5):
            break
        else:
            print("Invalid input\n")