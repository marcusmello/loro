# pylint:disable=missing-module-docstring
# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=too-few-public-methods
# pylint:disable=no-name-in-module

from environs import Env
from pydantic import BaseModel

env = Env()


class RestPath(BaseModel):
    root: str
    create: str = str()
    create_error = str()
    read: str = str()
    update: str = str()
    update_error: str = str()
    delete: str = str()

    def generate(self):
        self.create = "{}/create".format(self.root)
        self.create_error = "{}/create-error".format(self.root)
        self.read = self.root
        self.update = "{}/update".format(self.root)
        self.update_error = "{}/update-error".format(self.root)
        self.delete = "{}/delete".format(self.root)


answers_paths = RestPath(root="/answers")
answers_paths.generate()


class UrlPaths(BaseModel):
    answers = answers_paths


class CorsOrigins(BaseModel):
    paths: dict = UrlPaths().dict()
    protocols: list = env.list("ALLOWED_PROTOCOLS", default=["http"])
    main_domain: str = env.str("APP_HOSTNAME", default="localhost")
    main_port: int = env.int("APP_PORT", default=80)
    domains: list = env.list("EXTRA_DOMAINS_OR_IPS", default=list())
    ports: list = env.list("EXTRA_PORTS", default=list())

    def generate(self):
        self.domains.append(self.main_domain)
        self.ports.append(self.main_port)

        all_paths = []
        all_paths = [
            r[1]
            for r in [route.items() for route in self.paths.values()][0]
            if r[1] not in all_paths
        ]
        simple_urls = [
            "{}://{}{}".format(protocol, domain, path)
            for protocol in self.protocols
            for domain in self.domains
            for path in all_paths
        ]
        port_urls = [
            "{}://{}:{}{}".format(protocol, domain, port, path)
            for protocol in self.protocols
            for domain in self.domains
            for port in self.ports
            for path in all_paths
        ]

        return simple_urls + port_urls
