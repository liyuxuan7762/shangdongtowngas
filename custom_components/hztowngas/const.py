"""Constants for the TownGas Meter integration."""

DOMAIN = "hztowngas"

CONF_AUTH_CODE = "auth_code"
CONF_ACCESS_TOKEN = "access_token"
CONF_REFRESH_TOKEN = "refresh_token"
CONF_SUBS_ID = "subs_id"
CONF_SUBS_CODE = "subs_code"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_TOKEN_REFRESH_INTERVAL = "token_refresh_interval"
CONF_TOKEN_EXPIRES_IN = "token_expires_in"
CONF_TOKEN_CREATE_TIME = "token_create_time"

DEFAULT_SCAN_INTERVAL = 21600          # seconds — data fetch every 6 hours
DEFAULT_TOKEN_REFRESH_INTERVAL = 1800  # seconds — token refresh every 30 min (keepalive)
DEFAULT_HOST = "weixin.towngasvcc.com"
DEFAULT_CLIENT_ID = "pe92a8wechatYH0105"
SIGN_SALT = "hbasesoft.com-prod"
OAUTH_PATH = "/vcc-oauth"
API_PATH = "/nv1/vcc-cbs"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 NetType/WIFI "
    "MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090c33) XWEB/14315 Flue"
)
