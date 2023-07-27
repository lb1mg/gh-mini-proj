from dotenv import load_dotenv
load_dotenv()
import time
import asyncio

from app.managers.github_manager import CachedGithubManager

if __name__ == '__main__':
    DEMO_USER = 'miguelgrinberg'
    s = time.perf_counter()
    result = asyncio.run(CachedGithubManager.fetch_user(DEMO_USER))
    print(f'Time taken: {time.perf_counter()-s}')