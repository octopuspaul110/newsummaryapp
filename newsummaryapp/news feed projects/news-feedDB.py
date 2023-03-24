import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE news(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                urlToImage TEXT,
                categories TEXT,
                source TEXT,
                publishedAt SMALLDATETIME
            )
        ''')
        print("Table created successfully")
    except Error as e:
        print(e)


def get_articles():
    articles = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM article")
        rows = cur.fetchall()

        for i in rows:
            article = {}
            article["ID"] = i["ID"]
            article["title"] = i["title"]
            article["content"] = i["content"]
            article["urlToImage"] = i["urlToImage"]
            article["categories"] = i["categories"]
            article["source"] = i["source"]
            article["publishedAt"] = i["publishedAt"]
            articles.append(article)
    
    except:
        articles = []
    
    return articles     

def get_article_by_title(title):
    article = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM articles WHERE title = ?",(title,))
        row = cur.fetchone()

        article["ID"] = row["ID"]
        article["title"] = row["title"]
        article["content"] = row["content"]
        article["urlToImage"] = row["urlToImage"]
        article["categories"] = row["categories"]
        article["source"] = row["source"]
        article["publishedAt"] = row["publishedAt"]

    except:
        article= {}
    
    return  article

    
def main():
    database = r"C:\Users\User\Desktop\news feed projects\database\newsDatabase.db"
    conn = create_connection(database)
    if conn is not None:
        create_table(conn)
        conn.close()
    else:
        print("Error creating database connection")

if __name__ == '__main__':
    main()
