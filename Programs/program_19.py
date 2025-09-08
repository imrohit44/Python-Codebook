class QueryBuilder:
    def __init__(self):
        self._select_columns = []
        self._from_table = None
        self._where_conditions = []
        self._order_by_columns = []
        self._limit_value = None

    def select(self, *columns):
        """Specifies the columns to select."""
        if not columns:
            self._select_columns = ["*"]
        else:
            self._select_columns.extend(columns)
        return self # Enable method chaining

    def from_table(self, table_name: str):
        """Specifies the table name."""
        if not table_name:
            raise ValueError("Table name cannot be empty.")
        self._from_table = table_name
        return self

    def where(self, condition: str):
        """Adds a WHERE clause condition."""
        if not condition:
            raise ValueError("WHERE condition cannot be empty.")
        self._where_conditions.append(condition)
        return self

    def order_by(self, *columns, asc: bool = True):
        """Adds an ORDER BY clause."""
        if not columns:
            raise ValueError("ORDER BY columns cannot be empty.")
        
        order = "ASC" if asc else "DESC"
        for col in columns:
            self._order_by_columns.append(f"{col} {order}")
        return self

    def limit(self, n: int):
        """Adds a LIMIT clause."""
        if not isinstance(n, int) or n <= 0:
            raise ValueError("LIMIT value must be a positive integer.")
        self._limit_value = n
        return self

    def build(self) -> str:
        """Constructs and returns the SQL query string."""
        if not self._from_table:
            raise ValueError("Table name must be specified using from_table().")

        # SELECT part
        select_part = "SELECT " + (", ".join(self._select_columns) if self._select_columns else "*")

        # FROM part
        from_part = f"FROM {self._from_table}"

        # WHERE part
        where_part = ""
        if self._where_conditions:
            where_part = "WHERE " + " AND ".join(self._where_conditions)

        # ORDER BY part
        order_by_part = ""
        if self._order_by_columns:
            order_by_part = "ORDER BY " + ", ".join(self._order_by_columns)

        # LIMIT part
        limit_part = ""
        if self._limit_value is not None:
            limit_part = f"LIMIT {self._limit_value}"

        # Assemble the query parts
        query_parts = [select_part, from_part, where_part, order_by_part, limit_part]
        # Filter out empty parts and join them with spaces
        return " ".join(part for part in query_parts if part).strip() + ";"

# Example Usage:
if __name__ == "__main__":
    # Basic query
    query1 = QueryBuilder().select("id", "name").from_table("users").build()
    print("Query 1:", query1)
    # Expected: SELECT id, name FROM users;

    # Query with WHERE clause
    query2 = QueryBuilder()\
        .select("*")\
        .from_table("products")\
        .where("price > 100")\
        .where("category = 'Electronics'")\
        .build()
    print("Query 2:", query2)
    # Expected: SELECT * FROM products WHERE price > 100 AND category = 'Electronics';

    # Query with ORDER BY and LIMIT
    query3 = QueryBuilder()\
        .select("item_name", "stock_count")\
        .from_table("inventory")\
        .order_by("stock_count", asc=False)\
        .limit(5)\
        .build()
    print("Query 3:", query3)
    # Expected: SELECT item_name, stock_count FROM inventory ORDER BY stock_count DESC LIMIT 5;

    # Complex query
    query4 = QueryBuilder()\
        .select("customer_id", "order_date", "total_amount")\
        .from_table("orders")\
        .where("order_date >= '2024-01-01'")\
        .where("total_amount > 500")\
        .order_by("total_amount", asc=False)\
        .order_by("order_date")\
        .limit(10)\
        .build()
    print("Query 4:", query4)
    # Expected: SELECT customer_id, order_date, total_amount FROM orders WHERE order_date >= '2024-01-01' AND total_amount > 500 ORDER BY total_amount DESC, order_date ASC LIMIT 10;

    # Edge cases / errors
    try:
        QueryBuilder().select("name").build()
    except ValueError as e:
        print("Error (expected):", e)
    # Expected: Error (expected): Table name must be specified using from_table().