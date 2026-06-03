for f in /path/to/functions/*.sql; do
    psql -d your_database_name -f "$f"
done