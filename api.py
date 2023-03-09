from unittest import TestCase, main
from unittest.mock import patch
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


class TestMethods(TestCase):

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

    def test_make_get_user_request(self):
        """
        Teste unitário que mocka a chamada da API do
        github com infos do usuário
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = get_user('PauloViOS')
        assert response != None

    def test_create_user_instance(self):
        """
        Teste unitário que verifica propriedades da classe Usuário
        dados determinados parâmetros
        """
        parameters = {
            'name': 'Paulo',
            'login': 'paulo_do_github',
            'html_url': 'https://github.com/paulo_do_github',
            'public_repos': 10,
            'followers': 500,
            'following': 1000,
        }
        expected_user = User(
            parameters['name'],
            parameters['login'],
            parameters['html_url'],
            parameters['public_repos'],
            parameters['followers'],
            parameters['following']
        )
        for prop, value in vars(expected_user).items():
            assert value == parameters[prop]

    def test_get_user_repos(self):
        """
        Teste unitário que mocka a chamada da API
        do github com infos dos repos do usuário
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = get_user_repos('PauloViOS')
        assert response != None

    def test_create_dict_from_user_repos(self):
        pass

    def test_create_string_from_dict(self):
        """
        Teste unitário que verifica a criação da string a
        partir do dict com informações dos repositórios
        do usuário
        """
        test_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
        }
        expected_string = """
                a: 1
                b: 2
                c: 3"""
        result_string = create_string_from_repos_dict(test_dict)
        assert expected_string == result_string

    def test_create_user_file(self):
        pass


def get_user(username: str) -> User:
    """
    Função que chama o endpoint da API sobre as informções do usuário,
    serializa as informações recebidas e cria uma instância de User com elas.
    Enquanto um usuário com o nome fornecido não for encontrado,
    a função irá pedir por um novo nome e bater na API.
    """
    r = requests.get(url=f"https://api.github.com/users/{username}")
    data = r.json()
    while 'message' in data.keys():
        username = input(
            "Usuário inexistente. Por favor, insira um usuário válido do GitHub: ")
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
    """
    Função que chama o endpoint da API sobre os repos do usuário, serializa as
    informações recebidas e cria uma instância de User com elas
    """
    r = requests.get(url=f"https://api.github.com/users/{username}/repos")
    data = r.json()
    repos_dict = {}
    for repo in data:
        repo_name = repo["name"]
        repo_url = repo["html_url"]
        repos_dict[repo_name] = repo_url
    return repos_dict


def create_string_from_repos_dict(repos: dict) -> str:
    """
    Função para transformar as informações do dict em string,
    uma vez que o método write aceita apenas strings
    """
    repos_string = ""
    for repo_name, repo_url in repos.items():
        repos_string += f"""
                {repo_name}: {repo_url}"""
    return repos_string


def create_user_report_file(user: User, repos: dict) -> None:
    """
    Função que gera o arquivo txt
    """
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
    """
    Função principal que gera o relatório do usuário
    """
    username = input(
        "Por favor, insira o nome do usuário sobre o qual o relatório deve ser gerado: ")
    user_instance = get_user(username)
    repos_dict = get_user_repos(username)
    create_user_report_file(user_instance, repos_dict)
    print("Relatório criado com  sucesso")
    return None


if __name__ == "__main__":
    main(verbosity=1)
    # make_user_report()
