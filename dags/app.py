# dag - directed acyclic graph

# tasks : 1) fetch open library data (extract) 2) clean data (transform) 3) create and store data in table on postgres (load)
# operators : Python Operator and PostgresOperator
# hooks - allows connection to postgres
# dependencies

from datetime import datetime, timedelta
from airflow import DAG
import requests
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook



def get_open_library_data_books(num_books, ti):
    # Base URL of the Amazon search results for data science books
    # Base URL of the Amazon search results for data science books

    books = []

    # Search for books with a keyword
    url = "https://openlibrary.org/search.json?q=python+programming"

    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        with open('data.txt', 'w') as f:
            f.write(str(data))

        # Print first 5 books
        for book in data['docs'][:num_books]:
            title = book.get('title')
            authers = ",".join(book.get('author_name', []))
            first_published = book.get('first_publish_year')

            books.append({
                "Title": title,
                "Author": authers,
                "first_published": first_published
            })

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    # Limit to the requested number of books

    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(books)

    # Remove duplicates based on 'Title' column
    df.drop_duplicates(subset="Title", inplace=True)

    #print(df.head())

    # Push the DataFrame to XCom
    ti.xcom_push(key='book_data', value=df.to_dict('records'))


# 3) create and store data in table on postgres (load)

def insert_book_data_into_postgres(ti):
    book_data = ti.xcom_pull(key='book_data', task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data found")

    postgres_hook = PostgresHook(postgres_conn_id='books_connection')
    insert_query = """
    INSERT INTO books (title, authors, first_published)
    VALUES (%s, %s, %s)
    """
    for book in book_data:
        postgres_hook.run(insert_query, parameters=(book['Title'], book['Author'], book['first_published']))


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 6, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_store_amazon_books',
    default_args=default_args,
    description='A simple DAG to fetch book data from Amazon and store it in Postgres',
    schedule=timedelta(days=1),
)

# operators : Python Operator and PostgresOperator
# hooks - allows connection to postgres


fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_open_library_data_books,
    op_args=[50],  # Number of books to fetch
    dag=dag,
)

create_table_task = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='books_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT,
        first_published TEXT
    );
    """,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

# dependencies

fetch_book_data_task >> create_table_task >> insert_book_data_task