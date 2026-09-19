import re
from dataclasses import dataclass
from typing import List


@dataclass
class DocumentSection:
    title: str
    level: int
    content: str


class MarkdownSectionParser:
    """Parse Markdown documents into sections."""

    HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    def parse(self, content: str) -> List[DocumentSection]:
        lines = content.splitlines()

        sections: List[DocumentSection] = []

        current_title = None
        current_level = 0
        current_lines: List[str] = []

        for line in lines:
            match = self.HEADING_PATTERN.match(line)

            if match:
                # Save the previous heading/section.
                if current_title is not None:
                    sections.append(
                        DocumentSection(
                            title=current_title,
                            level=current_level,
                            content="\n".join(current_lines).strip(),
                        )
                    )

                current_level = len(match.group(1))
                current_title = match.group(2).strip()
                current_lines = []

            else:
                current_lines.append(line)

        # Save the final section.
        if current_title is not None:
            sections.append(
                DocumentSection(
                    title=current_title,
                    level=current_level,
                    content="\n".join(current_lines).strip(),
                )
            )

        # Handle content that appeared before the first heading.
        if current_title is None and current_lines:
            sections.append(
                DocumentSection(
                    title="Document",
                    level=0,
                    content="\n".join(current_lines).strip(),
                )
            )

        return sections