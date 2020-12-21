import psycopg2

CREDENTIALS = ("""
    host = database-1.cgzopzjcvpsf.ap-southeast-2.rds.amazonaws.com,
    dbname = 'postgres'
    user = 'postgres'
    password = '8NkN1qdiCu7VMd36XYEu'
""")


conn = psycopg2.connect(CREDENTIALS)


cur = conn.cursor()


im = cur.execute("select * from Investor_metrics")
print(im)


# def sql_select(sql):
#     import psycopg2
#     conn = None
#     try:
#         with psycopg2.connect(CREDENTIALS) as conn:
#             with conn.cursor() as curs:
#                 curs.execute(sql)
#                 text_lists = curs.fetchall()
#                 return text_lists
#     except Exception as e:
#         print(e)
#     finally:
#         if conn is not None:
#             conn.close()
#
#
# def get_db_credentials():
#     import psycopg2
#     global cursor
#     global connection
#     connection = psycopg2.connect(CREDENTIALS)
#     cursor = connection.cursor()
#
#
# def write_to_db(to_db_list, table_name, id_tag=None, update_string=None, on_conflict=False):
#     # header = ''
#     # l_names = header.split(',')
#     # update_string = ','.join(["{0} = excluded.{0}".format(e) for e in (l_names)])
#     """
#     :param to_db_list: list of lists
#     :param table_name: str name
#     :param id_tag: primary key
#     :param update_string: list ogf columns
#     :param on_conflict: False by default
#     :return: None
#     """
#     signs = '(' + ('%s,' * len(to_db_list[0]))[:-1] + ')'
#     try:
#         args_str = b','.join(cursor.mogrify(signs, x) for x in to_db_list)
#         args_str = args_str.decode()
#         insert_statement = """INSERT INTO %s VALUES """ % table_name
#         conflict_statement = """ ON CONFLICT DO NOTHING"""
#         if on_conflict:
#             conflict_statement = """ ON CONFLICT ("{0}") DO UPDATE SET {1};""".format(id_tag, update_string)
#         cursor.execute(insert_statement + args_str + conflict_statement)
#         connection.commit()
#     except Exception as e:
#         print(e)
