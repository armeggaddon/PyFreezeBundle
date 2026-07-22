import uvicorn
import settings


print("Initializing the service")

try:
    uvicorn.run("settings:app", host="0.0.0.0", port=8099)
except Exception as e:
    print(e)