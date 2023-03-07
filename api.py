import unittest
import requests


class User:
    def __init__(self, name, url, public_repos, followers, following):
        self.name = name
        self.html_url = url
        self.public_repos = public_repos
        self.followers = followers
        self.following = following


def get_user(username: str) -> User:
    r = requests.get(url=f"https://api.github.com/users/{username}")
    data = r.json()
    name = data['name']
    url = data['url']
    public_repos = data['public_repos']
    followers = data['followers']
    following = data['following']
    user = User(name, url, public_repos, followers, following)
    return user


def get_user_repos(username: str) -> dict:
    pass


def user_report(user: User, repos: dict) -> None:
    pass


class TestMethods(unittest.TestCase):

    def test_user_class_has_minimal_parameters(self):
        """
        Teste unitário relativo ao primeiro passo do desafio, esse cenário
        deve ser mantido na sua resolução.
        """
        parameters = [
            'name', 'html_url', 'public_repos', 'followers', 'following'
        ]
        user = get_user('PauloViOS')
        for param in parameters:
            self.assertTrue(hasattr(user, param))

    def test_create_user_instance(self):
        pass


if __name__ == "__main__":
    unittest.main()
