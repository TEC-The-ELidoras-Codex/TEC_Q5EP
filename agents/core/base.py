from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List
import time, json, yaml


ToolFn = Callable[[Dict[str, Any]], Dict[str, Any]]


@dataclass
class AgentContext:
    run_id: str
    out_dir: Path
    memory_base_url: str = "http://localhost:8000"
    scratch: Dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, ToolFn] = {}

    def register(self, name: str, fn: ToolFn):
        self._tools[name] = fn

    def get(self, name: str) -> ToolFn:
        if name not in self._tools:
            raise KeyError(f"Tool not found: {name}")
        return self._tools[name]


class Agent:
    def __init__(self, ctx: AgentContext, tools: ToolRegistry):
        self.ctx = ctx
        self.tools = tools

    def run_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        steps: List[Dict[str, Any]] = workflow.get("steps", [])
        results: List[Dict[str, Any]] = []
        for i, step in enumerate(steps, start=1):
            tool_name = step.get("tool")
            inputs = self._render_inputs(step.get("inputs", {}))
            tool = self.tools.get(tool_name)
            out = tool(inputs)
            results.append({"step": i, "tool": tool_name, "inputs": inputs, "output": out})
        # persist
        self.ctx.out_dir.mkdir(parents=True, exist_ok=True)
        (self.ctx.out_dir / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        return {"run_id": self.ctx.run_id, "steps": len(results), "out_dir": str(self.ctx.out_dir)}

    def _render_inputs(self, inputs: Dict[str, Any]) -> Any:
        # light templating: replace any occurrences of ${scratch.key} within strings
        # and resolve nested dicts/lists recursively
        def resolve(val: Any):
            if isinstance(val, dict):
                return {k: resolve(v) for k, v in val.items()}
            if isinstance(val, list):
                return [resolve(v) for v in val]
            if isinstance(val, str):
                out = val
                # replace all occurrences
                start = 0
                while True:
                    s = out.find("${scratch.", start)
                    if s == -1:
                        break
                    e = out.find("}", s)
                    if e == -1:
                        break
                    key = out[s + len("${scratch."): e]
                    rep = str(self.ctx.scratch.get(key, ""))
                    out = out[:s] + rep + out[e + 1:]
                    start = s + len(rep)
                return out
            return val
        return resolve(inputs)


def new_run(out_base: Path) -> AgentContext:
    rid = str(int(time.time()))
    return AgentContext(run_id=rid, out_dir=out_base / rid)
