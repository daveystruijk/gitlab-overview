import os
import json
import gitlab
import dateutil.parser as dateparser
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()  # load from .env
GITLAB_URL = os.getenv('GITLAB_URL')
GITLAB_PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')
GITLAB_ACCESS_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN')

gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_ACCESS_TOKEN)
project = gl.projects.get(GITLAB_PROJECT_ID)


print("\n== Open ==")
mrs = project.mergerequests.list(state='opened', order_by='updated_at', sort='desc')

for mr in mrs:
    title = mr.title
    author_name = mr.author['name']
    print(f"[{author_name}] {title}")

print("\n== Merged ==")
mrs = project.mergerequests.list(state='merged', order_by='updated_at', sort='desc')

for mr in mrs:
    title = mr.title
    updated_at = dateparser.parse(mr.updated_at)
    today = datetime.today()
    today_start = datetime(year=today.year, month=today.month, day=today.day, hour=0, second=0).astimezone()
    last_week_start = today_start - timedelta(days=7)
    if updated_at < last_week_start:
        break
    author_name = mr.author['name']
    print(f"{updated_at.strftime('%a %H:%M')} [{author_name}] {title}")
