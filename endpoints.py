# ====== Dash Base Path ======
BASE_PATH = "/linkvana"

# ====== Dash Page Routes ======
HOME_PAGE       = f"{BASE_PATH}/home"
LINKS_PAGE      = f"{BASE_PATH}/links"
ANALYTICS_PAGE  = f"{BASE_PATH}/analytics"
UPDATE_PAGE     = f"{BASE_PATH}/update"

# ====== API Base URL ======
# BASE_API = "http://localhost:8080/api"  # Local dev nếu chạy ngoài container
BASE_API = "http://alm-api/api"  # Khi chạy trong container của cluster

# ====== API Endpoints ======
CREATE_SHORTLINK = f"{BASE_API}/ShortUrl"
GET_EVENTS       = f"{BASE_API}/ShortUrl"
SOFT_DELETE      = f"{BASE_API}/ShortUrl/softdel"
HARD_DELETE      = f"{BASE_API}/ShortUrl/"
UPDATE           = f"{BASE_API}/ShortUrl/"
IMPORT           = f"{BASE_API}/ShortUrl/import"
EXPORT           = f"{BASE_API}/ShortUrl/export"
