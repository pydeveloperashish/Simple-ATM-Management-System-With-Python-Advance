Software Architecture: Layered Design Architecture
<!-- User Interface
    ↓
Presentation (Controller)
    ↓
Application (Business usecase like: BorrowBookService)
    ↓
Domain Model (Business Entities like Book.borrow())
    ↓
Persistence (Gateway/Repository like: BookRepository)
    ↓
Data (Database) -->

In this diagram, the arrows go downwards. It is very intuitive:

1) User clicks a button (UI).
2) Presentation handles the click.
3) Application/Domain decides what happens (Logic).
4) Persistence saves the result to the Data.