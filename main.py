import csv
import pymysql
import sys



def delete_row_by_id(conn, index_id):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM main WHERE index_id = %s"
            cursor.execute(query, str(index_id,))
        conn.commit()
        print(f"Row with index_id = {index_id} deleted successfully.")
    except Exception as e:
        print(f"Error while deleting row: {e}")

def input_row(input_file):
    # CSV 파일 열기 및 데이터베이스 삽입
    csv_file_path = input_file

    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # NULL 처리를 위해 공백 문자열은 None으로 변환
            first = None if row['first'] == '' else int(row['first'])
            second = None if row['second'] == '' else int(row['second'])
            third = None if row['third'] == '' else int(row['third'])
            
            # 데이터 삽입
            query = """
            INSERT INTO main (domain, question_number, first, second, third)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (int(row['domain']), int(row['question_number']), first, second, third))

    # 변경 사항 저장 및 연결 종료
    conn.commit()

    print("Data is inserted successfully")

def delete_rows_in_range(conn, start_id, end_id):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM main WHERE index_id BETWEEN %s AND %s"
            cursor.execute(query, (start_id, end_id))
        conn.commit()
        print(f"Rows with index_id between {start_id} and {end_id} deleted successfully.")
    except Exception as e:
        print(f"Error while deleting rows: {e}")


if __name__ == "__main__":
    try:
            # MySQL 연결
        conn = pymysql.connect(
            host='localhost',
            user='user',
            password='your_password',
            database='cisa',
            charset='utf8mb4',
            port = 40040 # 기본포트, 연결이 안된다면 열려있는 포트를 확인하고 직접 수정할것
        )
        cursor = conn.cursor()
        print("DB is connected successfully!")
    except:
        print("DB connection Failed")
        sys.exit()


    while True:
        mode = 0
        print("="*20)
        print("Select mode")
        print("""
    [1] Add
    [2] Delete specific row
    [3] Delete rows in range
    [9] Exit
            """)
        print("="*20)
        mode = int(input())

        if mode == 1:
            try: 
                input_file = input("input file name :")
                input_row(input_file)
            except:
                print("Error!")
                continue
            
        elif mode == 2:
            try:
                index_id = input("index_id :")
                delete_row_by_id(conn, int(index_id))
            except:
                print("Error!")
                continue
        elif mode == 3:
            try:
                start_id = input("input start_id: ")
                end_id = input("input enb_id: ")
                delete_rows_in_range(conn, int(start_id), int(end_id))
            except:
                print("Error!")
                continue
        elif mode == 9:
            print("Thank you!")
            sys.exit()

        else:
            print("wrong.")