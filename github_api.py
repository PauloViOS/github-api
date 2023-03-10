import requests
from textwrap import dedent
from user_class import User


def get_user(username: str) -> User:
    """
    Função que chama o endpoint da API sobre as informções do usuário,
    serializa as informações recebidas e cria uma instância de User com elas.
    Enquanto um usuário com o nome fornecido não for encontrado,
    a função irá pedir por um novo nome e bater na API.
    """
    r = requests.get(url=f"https://api.github.com/users/{username}")
    while r.status_code == 404:
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
    make_user_report()
