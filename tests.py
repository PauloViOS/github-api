from unittest import TestCase, main
from unittest.mock import patch

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
        result_string = github_api.create_string_from_repos_dict(test_dict)
        assert expected_string == result_string

    def test_create_user_file(self):
        pass


if __name__ == "__main__":
    main(verbosity=1)
