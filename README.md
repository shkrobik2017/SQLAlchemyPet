# SQLAlchemyPetProject
There is my pet project with SQL Alchemy to managing library.

# Task: Library Management System

## Goal:
Develop a management system for a small library, using SQLAlchemy to interact with the SQLite database.

### Stage 1: Database Schema Design
- **Books**: Should include title, author, publication year, and a unique identifier (ID).
- **Users**: Include name, email, and a unique ID.
- **Book Issuance**: A table for tracking which book was issued to a user, with the issue date and return deadline.

### Stage 2: Implementation of Models in SQLAlchemy
- Create SQLAlchemy models for each of the tables defined in the design stage.
- Use the declarative style to define models.
- Add the necessary relationships between tables (e.g., books to users through book issuance).

### Stage 3: CRUD Operations
Implement functionality for creating (C), reading (R), updating (U), and deleting (D) for each table. Include:
- Adding new books, users, and book issuance records.
- Searching for books by various parameters (author, year of publication).
- Updating user information.
- Deleting books, users, and issuance records that are no longer needed.

### Stage 4: Data Analysis Queries
Write queries to answer the following questions:
- Which books are currently checked out by user X?
- Which users have overdue books?
- Which book is the most popular (based on the number of issues)?
