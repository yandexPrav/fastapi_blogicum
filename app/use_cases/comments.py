"""Comment domain use-cases."""

from app.errors import DomainNotFoundError, InfrastructureError
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository
from app.use_cases.helpers import enrich_infrastructure_error


class CommentUseCase:
    def __init__(
        self,
        comment_repo: CommentRepository,
        post_repo: PostRepository,
        user_repo: UserRepository,
    ):
        self.comment_repo = comment_repo
        self.post_repo = post_repo
        self.user_repo = user_repo

    def list_comments(self, *, post_id: int | None = None, skip: int = 0, limit: int = 50):
        try:
            return self.comment_repo.get_all(post_id=post_id, skip=skip, limit=limit)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="comment", action="list"
            ) from exc

    def get_comment(self, comment_id: int):
        try:
            comment = self.comment_repo.get_by_id(comment_id)
            if not comment:
                raise DomainNotFoundError(
                    "Комментарий не найден",
                    details={"entity": "comment", "id": comment_id},
                )
            return comment
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="comment", action="get", extra={"id": comment_id}
            ) from exc

    def create_comment(self, payload: dict):
        try:
            if not self.post_repo.get_by_id(payload["post_id"]):
                raise DomainNotFoundError(
                    "Публикация не найдена",
                    details={"entity": "post", "id": payload["post_id"]},
                )
            if not self.user_repo.get_by_id(payload["author_id"]):
                raise DomainNotFoundError(
                    "Автор не найден",
                    details={"entity": "user", "id": payload["author_id"]},
                )
            return self.comment_repo.create(payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="comment", action="create"
            ) from exc

    def update_comment(self, comment_id: int, payload: dict):
        try:
            comment = self.comment_repo.get_by_id(comment_id)
            if not comment:
                raise DomainNotFoundError(
                    "Комментарий не найден",
                    details={"entity": "comment", "id": comment_id},
                )
            return self.comment_repo.update(comment, payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="comment", action="update", extra={"id": comment_id}
            ) from exc

    def delete_comment(self, comment_id: int):
        try:
            comment = self.comment_repo.get_by_id(comment_id)
            if not comment:
                raise DomainNotFoundError(
                    "Комментарий не найден",
                    details={"entity": "comment", "id": comment_id},
                )
            self.comment_repo.delete(comment)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="comment", action="delete", extra={"id": comment_id}
            ) from exc

