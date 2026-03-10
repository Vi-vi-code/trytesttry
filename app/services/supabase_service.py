from supabase import create_client, Client
from app.config import settings

# Initialize Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Placeholder: Replace with your actual table name
TABLE_NAME = "your_table_name"


def fetch_data(limit: int = 10) -> list:
    """Fetch data from the configured Supabase table."""
    response = supabase.table(TABLE_NAME).select("*").limit(limit).execute()
    return response.data


def fetch_by_query(column: str, value: str) -> list:
    """Fetch data filtered by a specific column value."""
    response = supabase.table(TABLE_NAME).select("*").eq(column, value).execute()
    return response.data
