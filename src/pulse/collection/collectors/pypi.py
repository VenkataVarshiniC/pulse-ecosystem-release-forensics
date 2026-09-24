"""PyPI collection adapter for planned tasks."""

from pulse.collection.planner import CollectionTask, TaskKind
from pulse.packages.pypi import PyPIClient


class PyPICollector:
    def __init__(self, client: PyPIClient) -> None:
        self.client = client

    def supports(self, kind: TaskKind) -> bool:
        return kind is TaskKind.PYPI_VERSION

    def collect(self, task: CollectionTask) -> dict[str, object]:
        package = self.client.package(
            task.parameters["package"], version=task.parameters["version"]
        )
        return package.model_dump(mode="json")
