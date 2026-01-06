from app.application.models.entities import ScreenerResult


class ScreenerUseCase(Protocol):
    def execute(self) -> ScreenerResult:
        ...
