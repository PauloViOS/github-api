from unittest import TestCase, main
from unittest.mock import patch, Mock, mock_open
import json
from requests import Response
from textwrap import dedent

import github_api
from user_class import User


class TestMethods(TestCase):

    def test_user_class_has_minimal_parameters(self):
        """
        Teste unitário relativo ao primeiro passo do desafio, esse cenário
        deve ser mantido na sua resolução.
        """
        parameters = [
            'name', 'html_url', 'public_repos', 'followers', 'following'
        ]
        user = github_api.get_user('PauloViOS')
        for param in parameters:
            self.assertTrue(hasattr(user, param))

    def test_make_get_user_request(self):
        """
        Teste unitário que mocka a chamada da API do
        github com infos do usuário
        """
        with patch('requests.get') as mock_get:
            mock_get.return_value.ok = True
            response = github_api.get_user('PauloViOS')
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
            response = github_api.get_user_repos('PauloViOS')
        assert response != None

    def test_create_dict_from_user_repos(self):
        """
        Teste unitário que faz a verificação da criação
        do dict com as informações dos repos do usuário
        pesquisado
        """
        mock_response = [
            {
                "id": 1,
                "node_id": "node_id",
                "name": "primeiro_repo",
                "full_name": "user/primeiro_repo",
                "html_url": "primeiro_repo.com",
            },
            {
                "id": 2,
                "node_id": "node_id",
                "name": "segundo_repo",
                "full_name": "user/segundo_repo",
                "html_url": "segundo_repo.com",
            },
            {
                "id": 3,
                "node_id": "node_id",
                "name": "terceiro_repo",
                "full_name": "user/terceiro_repo",
                "html_url": "terceiro_repo.com",
            },
            {
                "id": 4,
                "node_id": "node_id",
                "name": "quarto_repo",
                "full_name": "user/quarto_repo",
                "html_url": "quarto_repo.com",
            }
        ]
        expected_dict = {
            "primeiro_repo": "primeiro_repo.com",
            "segundo_repo": "segundo_repo.com",
            "terceiro_repo": "terceiro_repo.com",
            "quarto_repo": "quarto_repo.com",
        }

        with patch('requests.get') as mock_get:
            mock_resp = Mock()
            mock_resp.json.return_value = mock_response
            mock_get.return_value = mock_resp
            repos_dict = github_api.get_user_repos('user')

        assert repos_dict == expected_dict

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
        result_string = github_api.create_string_from_repos_dict(test_dict)
        assert expected_string == result_string

    def test_create_user_file(self):
        test_user = User(
            'name',
            'login',
            'html_url',
            'public_repos',
            'followers',
            'following'
        )
        expected_dict = {
            "primeiro_repo": "primeiro_repo.com",
            "segundo_repo": "segundo_repo.com",
            "terceiro_repo": "terceiro_repo.com",
            "quarto_repo": "quarto_repo.com",
        }
        expected_file_input = dedent(
            """
            Nome: name
            Perfil: html_url
            Número de repositórios públicos: public_repos
            Número de seguidores: followers
            Número de usuários seguidos: following
            Repositórios: 
                primeiro_repo: primeiro_repo.com
                segundo_repo: segundo_repo.com
                terceiro_repo: terceiro_repo.com
                quarto_repo: quarto_repo.com
            """
        ).strip("\n")
        open_mock = mock_open()
        with patch("github_api.open", open_mock, create=True):
            github_api.create_user_report_file(test_user, expected_dict)

        open_mock.assert_called_with(f"{test_user.login}.txt", "w")
        open_mock.return_value.write.assert_called_once_with(
            expected_file_input)


if __name__ == "__main__":
    main(verbosity=1)
