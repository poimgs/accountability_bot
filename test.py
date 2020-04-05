import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

get_data_query = "SELECT * FROM accountability"
result = cursor.execute(get_data_query)
rows = result.fetchall()
# last_index = rows[-1][0]

# index_to_insert = last_index + 1

# row_to_insert = (index_to_insert, current_time, message)
# insert_query = "INSERT INTO accountability values (?,?,?)"
# cursor.execute(insert_query, row_to_insert)
print(rows)
# print(index_to_insert)
if rows:
    print("true")
else:
    print('the heck')

connection.commit()

connection.close()