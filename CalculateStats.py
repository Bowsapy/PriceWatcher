from GetURLS import cursor, conn

def CalculateMinPrice():
    cursor.execute("""UPDATE statistics
    SET min_price = (
        SELECT MIN(price)
        FROM history
        WHERE history.product_id = statistics.product_id);""")
    conn.commit()  # <--- musí být commit


def CalculateMaxPrice():
    cursor.execute("""UPDATE statistics
    SET max_price = (
        SELECT MAX(price)
        FROM history
        WHERE history.product_id = statistics.product_id);""")
    conn.commit()  # <--- musí být commit

def CalculateAvgPrice():
    cursor.execute("""UPDATE statistics
    SET avg_price = (
        SELECT AVG(price)
        FROM history
        WHERE history.product_id = statistics.product_id);""")
    conn.commit()  # <--- musí být commit

def CalculateActPrice():
    cursor.execute("""UPDATE STATISTICS
                   SET act_price = (SELECT price FROM history
                WHERE history.product_id = statistics.product_id
                
                ORDER BY date DESC
                LIMIT 1)""")
    conn.commit()



CalculateAvgPrice()
CalculateMinPrice()
CalculateMaxPrice()
CalculateActPrice()
conn.close()
