import argparse
from pathlib import Path
import yaml

from agents.core.base import Agent, AgentContext, ToolRegistry, new_run
from agents.tools.prompt_pack import load_prompt_pack, save_text, save_json
from agents.tools.pantheon import load_pantheon, find_by_name, find_nearest, render_archetype_card
from agents.tools.memory_client import make_memory_client


def register_tools(ctx: AgentContext, registry: ToolRegistry):
    client = make_memory_client(ctx.memory_base_url)
    pantheon_state = {"loaded": False, "state": None}

    # Tools must accept a single dict of inputs and return a dict
    def _load_prompt_pack(inputs: dict):
        md_path = inputs.get("md_path")
        if not isinstance(md_path, str) or not md_path:
            raise ValueError("load_prompt_pack requires 'md_path' string input")
        res = load_prompt_pack(md_path)
        # seed scratch for templating in later steps
        ctx.scratch["prompt_text"] = res.get("text", "")
        ctx.scratch["prompt_path"] = res.get("path", md_path)
        return res

    def _save_text(inputs: dict):
        out_path = inputs.get("out_path")
        if not isinstance(out_path, str) or not out_path:
            raise ValueError("save_text requires 'out_path' string input")
        content = inputs.get("content", "")
        return save_text(out_path, content)

    def _memory_add(inputs: dict):
        item = inputs.get("item", {})
        return client["add"](item)

    def _memory_search(inputs: dict):
        raw = inputs.get("params", {})
        # Map to server schema (MemoryQuery): q, tags, limit
        payload = {
            "q": raw.get("q", raw.get("text", "")),
            "tags": raw.get("tags", []),
            "limit": raw.get("limit", 10),
        }
        results = client["search"](payload)
        # Stash in scratch for later steps
        ctx.scratch["search_results"] = results
        # Build simple markdown summary
        lines = ["# Recent Memories", ""]
        for m in results:
            line = f"- {m.get('timestamp','')} | {', '.join(m.get('tags', []))} | {m.get('content','')[:120]}"
            lines.append(line)
        ctx.scratch["search_markdown"] = "\n".join(lines)
        return {"count": len(results)}

    registry.register("load_prompt_pack", _load_prompt_pack)
    registry.register("save_text", _save_text)
    registry.register("memory_add", _memory_add)
    registry.register("memory_search", _memory_search)
    
    # Pantheon tools
    def _pantheon_load(inputs: dict):
        path = inputs.get("path", "data/pantheon/entries.json")
        pantheon_state["state"] = load_pantheon(path)
        pantheon_state["loaded"] = True
        return {"loaded": True, "path": path, "count": len(pantheon_state["state"]["entries"]) }

    def _pantheon_select(inputs: dict):
        if not pantheon_state["loaded"]:
            pantheon_state["state"] = load_pantheon()
            pantheon_state["loaded"] = True
        name = inputs.get("name")
        e = find_by_name(pantheon_state["state"], name) if name else None
        ctx.scratch["pantheon_selected"] = e
        return {"found": bool(e), "name": name}

    def _pantheon_nearest(inputs: dict):
        if not pantheon_state["loaded"]:
            pantheon_state["state"] = load_pantheon()
            pantheon_state["loaded"] = True
        ra = float(inputs.get("ra", 0.0))
        dec = float(inputs.get("dec", 0.0))
        k = int(inputs.get("k", 3))
        nearest = find_nearest(pantheon_state["state"], ra, dec, k)
        items = [e for _, e in nearest]
        ctx.scratch["pantheon_nearest"] = items
        # also build a markdown list for convenience
        lines = []
        for e in items:
            lines.append(f"- {e.get('name')} — RA {e.get('ra_deg')}°, Dec {e.get('dec_deg')}° | Tags: {', '.join(e.get('tags', []))}")
        ctx.scratch["nearest_list"] = "\n".join(lines)
        return {"count": len(nearest)}

    def _pantheon_render_card(inputs: dict):
        e = ctx.scratch.get("pantheon_selected")
        if not e:
            return {"error": "no selection"}
        card = render_archetype_card(e)
        ctx.scratch["pantheon_card_md"] = card
        return {"chars": len(card)}

    registry.register("pantheon_load", _pantheon_load)
    registry.register("pantheon_select", _pantheon_select)
    registry.register("pantheon_nearest", _pantheon_nearest)
    registry.register("pantheon_render_card", _pantheon_render_card)
    # Optional: expose save_json for future workflows
    def _save_json(inputs: dict):
        out_path = inputs.get("out_path")
        if not isinstance(out_path, str) or not out_path:
            raise ValueError("save_json requires 'out_path' string input")
        data = inputs.get("data", {})
        return save_json(out_path, data)
    registry.register("save_json", _save_json)


def main():
    parser = argparse.ArgumentParser(description="Run an agent workflow")
    parser.add_argument("workflow", help="Path to workflow YAML under agents/workflows")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL for the API")
    parser.add_argument("--var", action="append", default=[], help="Set scratch variable key=value (repeatable)")
    args = parser.parse_args()

    ctx = new_run(Path("data/agents/runs"))
    # seed scratch so workflow can reference ${scratch.run_id}
    ctx.scratch["run_id"] = ctx.run_id
    ctx.memory_base_url = args.base_url

    # parse vars into scratch
    for item in args.var:
        if not isinstance(item, str) or "=" not in item:
            continue
        k, v = item.split("=", 1)
        v = v.strip()
        # try to coerce types
        if v.lower() in ("true", "false"):
            val = v.lower() == "true"
        else:
            try:
                if "." in v:
                    val = float(v)
                else:
                    val = int(v)
            except ValueError:
                val = v
        ctx.scratch[k.strip()] = val

    registry = ToolRegistry()
    register_tools(ctx, registry)

    # Load workflow YAML
    wf_dict = yaml.safe_load(Path(args.workflow).read_text(encoding="utf-8"))

    agent = Agent(ctx=ctx, tools=registry)
    result = agent.run_workflow(wf_dict)
    print(f"Run {ctx.run_id} completed. Outputs in {ctx.out_dir}")
    return 0 if result else 1


if __name__ == "__main__":
    raise SystemExit(main())
