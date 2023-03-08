import unittest
import requests
from textwrap import dedent


class User:
    def __init__(self, name, login, url, public_repos, followers, following):
        self.name = name
        self.login = login
        self.html_url = url
        self.public_repos = public_repos
        self.followers = followers
        self.following = following

    def __repr__(self):
        rep = f"Usuário: {self.name}\nUrl: {self.html_url}"
        return rep


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


def get_user(username: str) -> User:
    r = requests.get(url=f"https://api.github.com/users/{username}")
    data = r.json()
    name = data['name']
    login = data['login']
    url = data['url']
    public_repos = data['public_repos']
    followers = data['followers']
    following = data['following']
    user = User(name, login, url, public_repos, followers, following)
    return user


def get_user_repos(username: str) -> dict:
    r = requests.get(url=f"https://api.github.com/users/{username}/repos")
    data = r.json()
    repos_dict = {}
    for repo in data:
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        repos_dict[repo_name] = repo_url
    return repos_dict


def create_string_from_repos_dict(repos: dict) -> str:
    repos_string = ""
    for repo_name, repo_url in repos.items():
        repos_string += f"""
                {repo_name}: {repo_url}"""
    return repos_string


def create_user_report_file(user: User, repos: dict) -> None:
    repos_string = create_string_from_repos_dict(repos)
    with open(f"{user.login}.txt", "w") as report_file:
        report_file.write(dedent(
            f"""
            Nome: {user.name}
            Perfil: {user.html_url}
            Número de repositórios públicos: {user.public_repos}
            Número de seguidores: {user.followers}
            Número de usuários seguidos: {user.following}
            Repositórios: {repos_string}
            """
        ).strip("\n"))


def make_user_report() -> None:
    username = input(
        "Por favor, insira o nome do usuário sobre o qual o relatório deve ser gerado: ")
    user_instance = get_user(username)
    repos_dict = get_user_repos(username)
    create_user_report_file(user_instance, repos_dict)
    print("Relatório criado com  sucesso")
    return None


if __name__ == "__main__":
    # unittest.main()
    make_user_report()
