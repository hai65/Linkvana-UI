# ====== Dash Page Routes ======
HOME_PAGE       = "/home"
LINKS_PAGE      = "/links"
ANALYTICS_PAGE  = "/analytics"
UPDATE_PAGE     = "/update"


# ====== API Base URL ======
BASE_API = "http://localhost:8080/api"


# ====== API Endpoints ======
CREATE_SHORTLINK = f"{BASE_API}/ShortUrl"
GET_EVENTS       = f"{BASE_API}/ShortUrl"
SOFT_DELETE      = f"{BASE_API}/ShortUrl/softdel"
HARD_DELETE      = f"{BASE_API}/ShortUrl/"
UPDATE           = f"{BASE_API}/ShortUrl/"
