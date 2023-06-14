from dataclasses import dataclass, field
from typing import Any

from dashboards.component import Component


@dataclass
class MatchForm(Component):
    template_name: str = "football/components/match_form.html"
    value: Any = field(default_factory=list)
