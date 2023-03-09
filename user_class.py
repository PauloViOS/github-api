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
