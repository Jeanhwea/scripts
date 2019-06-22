#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


class GitRepoCLI:

  def __init__(self):
    self.remote = 'github'
    self.username = 'Jeanhwea'

  def getRepos(self):
    if self.remote == 'github':
      url = 'https://api.github.com/users/{user}/repos'.format(
          user=self.username
      )
      repos = requests.get(url).json()
      for repo in repos:
        print(u'{name}: {desc}'.format(
            name=repo['name'],
            desc=repo['description']
        ))

  def apply(self):
    self.getRepos()


def main():
  cli = GitRepoCLI()
  cli.apply()


if __name__ == '__main__':
  main()
