import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# We only create the client if we have valid url and key, otherwise we handle it later.
supabase: Client = None

if url and key:
    supabase = create_client(url, key)

def get_supabase() -> Client:
    global supabase
    if supabase is None:
        # Pudo haber sido configurado dinámicamente o re-cargado
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")
        if url and key:
            supabase = create_client(url, key)
    return supabase
