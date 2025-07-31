from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

# Configure Sybase database connection
connection_string = (
        "DRIVER={Sybase ASE ODBC Driver};"
        "SERVER=your_sybase_server;"
        "PORT=5000;"
        "DATABASE=your_database;"
        "UID=your_username;"
        "PWD=your_password;"
)

def get_db_connection():
      return pyodbc.connect(connection_string)

@app.route('/books', methods=['GET'])
def get_books():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books")
        books = cursor.fetchall()
        conn.close()
        return jsonify([{"id": row[0], "title": row[1], "author": row[2]} for row in books])

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (data['title'], data['author']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=? WHERE id=?", (data['title'], data['author'], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Book updated successfully"})

if __name__ == '__main__':
    app.run(debug=True)

