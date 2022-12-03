# Ateiciai, kad butu galima skaiciuoti git cmmitus
import requests
from urllib.parse import parse_qs, urlparse

# def get_commits_count(self, owner_name: str, repo_name: str) -> int:
#     """
#     Returns the number of commits to a GitHub repository.
#     """
#     url = f"https://api.github.com/repos/{owner_name}/{repo_name}/commits?per_page=1"
#     r = requests.get(url)
#     links = r.links
#     rel_last_link_url = urlparse(links["last"]["url"])
#     rel_last_link_url_args = parse_qs(rel_last_link_url.query)
#     rel_last_link_url_page_arg = rel_last_link_url_args["page"][0]
#     commits_count = int(rel_last_link_url_page_arg)
#     return commits_count
# print(get_commits_count)

