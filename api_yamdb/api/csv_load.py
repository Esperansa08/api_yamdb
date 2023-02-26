import csv
import sqlite3


csv_files = {'category.csv': 'reviews_category',
              'genre.csv': 'reviews_genre',
              'comments.csv': 'reviews_comment',
              'genre_title.csv': 'reviews_genretitle',
              'review.csv': 'reviews_review',
              'titles.csv': 'reviews_title'}
             # 'users.csv': 'users_user'}

con = sqlite3.connect(r"D:/Dev/api_yamdb/api_yamdb/db.sqlite3")
cur = con.cursor()


for csv_file in csv_files:


    with open(f'D:/Dev/api_yamdb/api_yamdb/static/data/{csv_file}','r', encoding="utf-8",) as fin:
        reader = csv.reader(fin)
        row1 = next(reader) 
        row1_str =  ','.join(row1) 
        question_marks = ["?"] * len(row1)
        to_add = ','.join(question_marks)
        cur.executemany(f"INSERT INTO {csv_files.get(csv_file)} ({row1_str}) VALUES ({to_add});", reader)

cur.execute(f"CREATE TABLE IF NOT EXISTS {csv_files.get(csv_file)} ({row1_str});")
con.commit()
con.close()
