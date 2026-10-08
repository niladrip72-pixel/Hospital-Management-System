# Case Study: Library Book Management System

# Problem Description:

# A library needs a system to manage its books, track borrowers, monitor overdue books, and handle book search and inventory updates. The system should:

# Allow adding new books without losing the existing inventory.

# Store book details such as title, author, genre, and availability status.

# Allow librarians to display all book records in a structured format.

# Retrieve borrowing history for any book.

# If a book title is not found, display a proper message.

# Identify books marked as "Rare" or "Reference Only" and protect them from being issued or modified.

# Analyze which genre has the highest number of books.

# Allow partial title search (e.g., all books with "Data" in the title).

# Determine the most borrowed book in an optimized way.

# Demonstrate the effect of shallow vs deep copy on book records.

#-----------IMPORTING COPY AND LOGGING MODULES---------------

import copy,logging

logging.basicConfig(
    filename="library.log",
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s"
)

#---------------DEFINE A LIBRARY CLASS--------------------

class Library:  
    def __init__(self):
        self.books:dict={}

#------------------ADD BOOKS--------------------

    def add_books(self):
        try:
            book_id:int=int(input("Enter the book ID of the book= "))
            if book_id in self.books:
                print("The book already exists.")
                return
            title:str=input("\nEnter the title of the book= ")
            author:str=input("\nEnter the name of the author= ")
            genre:str=input("\n Enter the genre= ")
            status:str="Available"
            book_type:str=input("Enter the book type (Normal / Rare / Reference Only) : ")
            self.books[book_id]={
                "Title" : title,
                "Author" : author,
                "Genre" : genre,
                "Status" : status,
                "Type" : book_type,
                "Borrow_count" : 0,   # Let, Intially the number of borrower is 0
                "History" : []        # Takig a list in History. 
            }
            logging.info(f"{title} Book is added.")
            print("\n Book Added Successfully !!!")
        except ValueError:
            print("Invalid Book ID.")
            logging.warning("Give the correct data type or you should have give an integer input in book_id.")

#------------------DISPLAY BOOKS-----------------

    def display_books(self):
        if not self.books:
            print("No Books available.")
            return
        print("\n")
        print("-"*150)
        print(f"{'ID' : <10}"
              f"{'Title' : <25}"
              f"{'Author' : <20}"
              f"{'Genre' : <15}"
              f"{'Status' : <15}"
              f"{'Type' : <15}")
        print("-"*150)
        for book_id,details in self.books.items():
            print(
                f"{book_id : <10}"
                f"{details['Title'] : <25}"
                f"{details['Author'] : <20}"
                f"{details['Genre'] : <15}"
                f"{details['Status'] : <15}"
                f"{details['Type'] : <15}"
            )

#---------------SEARCH BOOKS---------------------

    def search_books(self):
        title:str=input("\nEnter the exact title : ").lower()  # We change whole title into the lower case so we can dynamically search.
        found:bool=False  # Inittially no matching book is found yet
        for details in self.books.values():
            if details["Title"].lower()==title:
                print("\n Book has been Founded.")
                print(details)
                found:bool=True
                break
            if not found:
                print("Book not founded.")

#-----------------PARTIAL SEARCH-------------------

    def partial_search(self):
        keyword:str=input("Enter keyword : ").lower()
        found:bool=False
        print("\n Matching Books: \n")
        for details in self.books.values():
            if keyword in details["Title"].lower():
                print(details["Title"])
                found:bool=True
        if not found:
            print("No matching books found.")
            logging.error("Give the correct keyword.")

#-----------------ISSUE A BOOK------------------

    def issue_book(self):
        try:
            book_id:int=int(input("Enter the Book ID :"))
            if book_id not in self.books:
                print("Book ID not found.")
                return            
            book=self.books[book_id]   # If book_id in self.books then assign them to a variable. 
            if book["Type"].lower() in ["rare","reference only"]:
                print("This book cannot be issued.")
                logging.warning(f"Issue attempt on protected book : {book["Title"]}")
                return
            if book["Status"]=="Issued":   # If the book already issued than you can not borrow the book.
                print("The Book already issued.")
                return
            borrower:str=input("Enter the name of the borrower : ")
            book["Status"]="Issued"    # When the all previous condition are not follow then the status of the book is "Available"
            book["Borrow_count"] += 1    # Preliminary in the dictionary the borrow_count=0, so each time it increased by 1, when the borrower borrow a book.
            book["History"].append(borrower)   # Here History key word is of type list and it holds the name of the borrowers
            logging.info(f"Book Issued : {book["Title"]} to {borrower}")
            print("Book issued successfully.")
        except ValueError:
            print("Invalid Book ID.")
            logging.warning("You give the wrong data type in book_id it should be integer type.")

#-------------------RETURN A BOOK------------------------

    def return_book(self):
        try:
            book_id:int=int(input("Enter the Book Id = "))
            if book_id not in self.books:
                print("Book Not Found.")
                return
            self.books[book_id]["Status"]="Available"   # If the book is returned then it's status simply changed in the library book status is "Issued" to "Available" and that means the book is returned to the library and it is available now
            print("Book is successfully returned.")
            logging.info(f"Book Returned : {self.books[book_id]["Title"]}")
        except ValueError:
            print("Invalid Input.")
            logging.warning("You have to give an integer value when you enter book_id.")

#-------------------BORROWER HISTORY--------------------

    def borrow_history(self):
        try:
            book_id:int=int(input("Enter the Book ID : "))
            if book_id not in self.books:
                print("Book not found.")
                return
            history:list=self.books[book_id]["History"]   # Perticular book_id history will be stored in history
            if not history:
                print("No borrower history has been founded.")
                return
            print("\n---------- Borrow History:------------")
            for person in history:
                print(person,end=" ")  # History in self.books is a list sequence datatype so thats why we can see all the borrower by using the for loop.
        except ValueError:
            print("Invalid Book ID.")

#--------------------MODIFY BOOKS------------------------

    def modify_books(self):
        try:
            book_id:int=int(input("Enter the Book ID = "))
            if book_id not in self.books:
                print("Book not Found.")
                return
            book=self.books[book_id]
            if book["Type"].lower() in ["rare","reference only"]:
                print("Protected : Book cannot be modified.")
                logging.warning(f"Modification attempt on {book["Title"]}")
                return
           
           # If above all condition are not matched then it simply modify the titles,author and genre 
            title:str=input("Enter the New title of the book: \n")
            author:str=input("Enter the New Author: \n")
            genre:str=input("Enter the New Genre : \n")
            book["Title"]=title
            book["Author"]=author
            book["Genre"]=genre
            logging.info(f"{book_id} : Book Modified.")
            print("\nThe book is modified successfully.")
        except ValueError:
            logging.warning("book_id takes only the integers.")
            print("Invalid Book ID.")

#---------------HIGHEST GENRE-------------------

    def highest_genre(self):
        if not self.books:
            print("No books available.")
            return
        genre_count={}    # Creates an empty dictionary to store genre frequencies.
        for book in self.books.values():
            genre=book["Genre"]
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre]=1
        highest = max(genre_count,key=genre_count.get)    # genre_count.get()  give all the current values of the present genre values and the max produce the maximum values and its stored in highest. Without key the all keys will be printed but if we give the key= then it shows the value in the perticular genre, example= programming=8 , science=10 so the key=genre_count().get give the values 8 and 10
        print(f" Genre with Highest Books : "
              f" {highest}  ({genre_count[highest]})")

#-----------------MOST BORROWED BOOK--------------------

    def most_borrowed_book(self):
        if not self.books:
            print("No Books Found.")
            return
        max_count=0
        book_name=""
        for book in self.books.values():
            if book["Borrow_count"] > max_count:
                max_count=book["Borrow_count"]
                book_name=book["Title"]
        print(f" Most Borrowed Book :"
              f"{book_name} : ({max_count}) times")

#-------------------SHALLOW COPY AND DEEP COPY-------------------

    def copy_demo(self):
        if not self.books:
            print("Add at least one book first.")
            return
        shallow_copy=copy.copy(self.books)
        deep_copy=copy.deepcopy(self.books)
        first_key=list(self.books.keys())[0]   # First of all keys in the dictionary are changed in a list example = [101,102] the 1st id we check the memory how the copy shares memory.   
        print("\n Original Title : ")
        print(self.books[first_key]["Title"])   # It prints the 1st index's title
        # <---------Shallow copy Test------>
        shallow_copy[first_key]["Title"] = ' changed by Shallow copy'  # It also changed self.books[0th index]["Title"]
        print("\n After shaloow copy change.")
        print("Original :",self.books[first_key]["Title"])
        print("Shallow : ",shallow_copy[first_key]["Title"])
        deep_copy[first_key]["Title"]="Changed by Deep Copy"
        print("\n After Deep Copy change.")
        print("Original : ",self.books[first_key]["Title"])
        print("Deep : ",deep_copy[first_key]["Title"])

#-------------------DEFINING THE MAIN FUNCTION-------------------

def main():
    library:Library=Library()
    while True:
        print("\n")
        print("-----------MENU-----------")
        print("1. Add Book.")
        print("2. Display Books.")
        print("3. Search Exact Title.")
        print("4. Partial Title Search.")
        print("5. Issue The Book")
        print("6. Return The Book.")
        print("7. Borrower History.")
        print("8. Modify Book.")
        print("9. Highest genre.")
        print("10. Most Borrowed Book.")
        print("11. Shallow Vs Deep Copy.")
        print("12. Exit.")
        try:
            choice:int=int(input("Enter your choice = "))
            if choice==1:
                library.add_books()
            elif choice==2:
                library.display_books()
            elif choice==3:
                library.search_books()
            elif choice==4:
                library.partial_search()
            elif choice==5:
                library.issue_book()
            elif choice==6:
                library.return_book()
            elif choice==7:
                library.borrow_history()
            elif choice==8:
                library.modify_books()
            elif choice==9:
                library.highest_genre()
            elif choice==10:
                library.most_borrowed_book()
            elif choice==11:
                library.copy_demo()
            elif choice==12:
                print("The program terminates here. ")
                print("Thank You.")
                break
            else:
                print("Invalid Choice.")
        except ValueError:
            print("Please Enter a Valid Number.")
            logging.warning("Please give the correct choice number.")

#---------------------CALLING THE MAIN FUNCTION--------------------
if __name__=='__main__':
    main()