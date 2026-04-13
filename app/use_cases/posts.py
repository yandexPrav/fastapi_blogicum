"""Post domain use-cases."""

from app.errors import DomainNotFoundError, InfrastructureError
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository
from app.use_cases.helpers import enrich_infrastructure_error


class PostUseCase:
    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def list_posts(self, *, skip: int = 0, limit: int = 20, published_only: bool = False):
        try:
            return self.post_repo.get_all(
                skip=skip, limit=limit, published_only=published_only
            )
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(exc, entity="post", action="list") from exc

    def get_post(self, post_id: int):
        try:
            post = self.post_repo.get_detailed_by_id(post_id)
            if not post:
                raise DomainNotFoundError(
                    "Публикация не найдена",
                    details={"entity": "post", "id": post_id},
                )
            return post
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="post", action="get", extra={"id": post_id}
            ) from exc

    def create_post(self, payload: dict):
        try:
            if not self.user_repo.get_by_id(payload["author_id"]):
                raise DomainNotFoundError(
                    "Автор не найден",
                    details={"entity": "user", "id": payload["author_id"]},
                )
            return self.post_repo.create(payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(exc, entity="post", action="create") from exc

    def update_post(self, post_id: int, payload: dict):
        try:
            post = self.post_repo.get_by_id(post_id)
            if not post:
                raise DomainNotFoundError(
                    "Публикация не найдена",
                    details={"entity": "post", "id": post_id},
                )
            return self.post_repo.update(post, payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="post", action="update", extra={"id": post_id}
            ) from exc

    def delete_post(self, post_id: int):
        try:
            post = self.post_repo.get_by_id(post_id)
            if not post:
                raise DomainNotFoundError(
                    "Публикация не найдена",
                    details={"entity": "post", "id": post_id},
                )
            self.post_repo.delete(post)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="post", action="delete", extra={"id": post_id}
            ) from exc

