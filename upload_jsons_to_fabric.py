import os
import requests
from msal import PublicClientApplication
from dotenv import load_dotenv

# Load .env values
load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
LAKEHOUSE_NAME = os.getenv("LAKEHOUSE_NAME")
FOLDER_PATH = os.getenv("LOCAL_FOLDER_PATH")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://onelake.microsoft.com/.default"]

# Step 1: Authenticate and get access token
def get_access_token():
    app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    accounts = app.get_accounts()
    result = app.acquire_token_silent(SCOPE, account=accounts[0]) if accounts else None
    if not result:
        result = app.acquire_token_interactive(SCOPE)
    return result["access_token"]

# Step 2: Upload files to Lakehouse
def upload_to_lakehouse(access_token, local_folder_path):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }

    for root, _, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_folder_path)
            lakehouse_path = f"Files/{relative_path.replace(os.sep, '/')}"
            
            upload_url = (
                f"https://onelake.dfs.fabric.microsoft.com/workspaces/{WORKSPACE_ID}/"
                f"lakehouses/{LAKEHOUSE_NAME}/paths/{lakehouse_path}?resource=filesystem"
            )

            with open(local_file_path, "rb") as f:
                response = requests.put(upload_url, headers=headers, data=f.read())
                if response.status_code in [200, 201]:
                    print(f"[✓] Uploaded: {lakehouse_path}")
                else:
                    print(f"[x] Failed: {lakehouse_path} — {response.status_code} — {response.text}")

if __name__ == "__main__":
    token = get_access_token()
    upload_to_lakehouse(token, FOLDER_PATH)
