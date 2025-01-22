import os
from git import Repo

if __name__ == "__main__":
  dir_path = os.path.dirname(os.path.realpath(__file__))
  repo = Repo(dir_path)
  print(repo.head.commit.message.strip())
