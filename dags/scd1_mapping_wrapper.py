import mysql.connector
def scd1_mapping(
    conn,
    source_table,
    target_table,
    key_columns,
    update_columns
):
    """
    Generic SCD-1 mapping function
    """
    try:
        cursor = conn.cursor()

        key_cols = ", ".join(key_columns)
        upd_cols = ", ".join(update_columns)

        update_stmt = ", ".join(
            [f"{col} = VALUES({col})" for col in update_columns]
        )

        sql = f"""
            INSERT INTO {target_table} ({key_cols}, {upd_cols})
            SELECT {key_cols}, {upd_cols}
            FROM {source_table}
            ON DUPLICATE KEY UPDATE
                {update_stmt},
                updated_at = NOW();
        """

        cursor.execute(sql)
        conn.commit()

        print(f"✅ SCD-1 load completed for {target_table}")

    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"SCD-1 mapping failed: {e}")

    finally:
        cursor.close()
