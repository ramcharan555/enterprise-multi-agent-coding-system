from dataclasses import dataclass, field


@dataclass
class CodeChunk:
    chunk_id: str
    chunk_type: str
    name: str
    file_path: str
    start_line: int
    end_line: int
    source: str
    parent: str | None = None
    children: list[str] = field(default_factory=list)

    imports: list[str] = field(default_factory=list)
    inherits_from: list[str] = field(default_factory=list)
    calls: list[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "chunk_id": self.chunk_id,
            "chunk_type": self.chunk_type,
            "name": self.name,
            "file_path": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "source": self.source,
            "parent": self.parent,
            "children": self.children,
            "imports": self.imports,
            "inherits_from": self.inherits_from,
            "calls": self.calls,
        }