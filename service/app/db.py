import uuid
from clickhouse_driver import Client

class ClickHouseLogManager:
    def __init__(self, host='clickhouse', port=9000, user='admin', password='admin123', database='logs_db'):
        self.client = Client(host=host, port=port, user=user, password=password, database=database)

    def create_log_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS log (
            id UUID,
            timestamp DateTime DEFAULT now(),
            Timestamp DateTime,
            level String,
            message String,
            url String,
            module String,
            kind_of String
        ) ENGINE = MergeTree()
        ORDER BY id
        """
        self.client.execute(create_table_query)
        print("Table 'log' created successfully.")

    def insert_log_entry(self, level, message, url=None, module=None, kind_of=None):
        log_id = str(uuid.uuid4())
        insert_query = "INSERT INTO log (id, level, message, url, module, kind_of) VALUES"
        self.client.execute(insert_query, [(log_id, level, message, url, module, kind_of)])
        print("Log entry inserted successfully.")

    def read_log_entries(self):
        select_query = "SELECT * FROM log"
        result = self.client.execute(select_query)
        for row in result:
            print(row)

    def update_log_entry(self, id, new_message):
        update_query = "ALTER TABLE log UPDATE message = %s WHERE id = %s"
        self.client.execute(update_query, (new_message, id))
        print("Log entry updated successfully.")

    def delete_log_entry(self, id):
        delete_query = "ALTER TABLE log DELETE WHERE id = %s"
        self.client.execute(delete_query, (id,))
        print("Log entry deleted successfully.")
