import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["founder-board", "founder-marketing", "founder-cfo", "founder-consumer", "founder-launch",
          "founder-pricing", "founder-offer", "founder-competitors", "founder-brand", "founder-ops", "founder-plan"]
ABOUT = ("Eleven free Gemini skills that test a business before you launch it: a board trained on Hormozi, "
         "Thiel and Jobs, a marketing director, a CFO, and a consumer panel of 100 buyer agents. Free, MIT.")


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


EM = chr(0x2014)  # built in code so this file does not trip its own check


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt", ".sh", ".svg")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_eleven_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 300, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"<SKILL_DIR>/([\w.\-/]+\.(?:py|md))", text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS_DIR, s, tool))), "%s: %s" % (s, tool))

    def test_plugin_manifests_and_rules(self):
        with open(os.path.join(ROOT, "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "gemini-founder-skill")
        self.assertEqual(plugin["description"], ABOUT)
        self.assertTrue(os.path.isfile(os.path.join(ROOT, plugin["logo"])))
        with open(os.path.join(ROOT, "plugins", "gemini-founder-skill", "plugin.json"), encoding="utf-8") as fh:
            nested = json.load(fh)
        self.assertEqual(nested["name"], "gemini-founder-skill")
        self.assertEqual(nested["description"], ABOUT)
        with open(os.path.join(ROOT, "gemini-extension.json"), encoding="utf-8") as fh:
            ext = json.load(fh)
        self.assertEqual(ext["name"], "gemini-founder-skill")
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "rules", "AGENTS.md")))
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "rules", "GEMINI.md")))
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "scripts", "install.sh")))
        self.assertTrue(os.path.isfile(os.path.join(ROOT, "scripts", "verify.sh")))

    def test_readme_documents_plugin_and_skills(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# Gemini Founder Skill"))
        for line in (
            "## Overview",
            "## Quick Start & Installation",
            "bash scripts/install.sh",
            "## How to Use: Step-by-Step",
            "## Deterministic Python Tools",
            "## Fine Print & Guardrails",
            "## License & Acknowledgements",
            "https://github.com/Jakeschincariol/founder-skill",
        ):
            self.assertIn(line, readme)
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)

    def test_examples_parse(self):
        for rel in ("founder-cfo/example.json", "founder-consumer/customer.example.json"):
            with open(os.path.join(SKILLS_DIR, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_no_em_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                self.assertNotIn(EM, fh.read(), os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
