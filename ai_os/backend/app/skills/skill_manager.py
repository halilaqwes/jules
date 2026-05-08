import os

class SkillManager:
    def __init__(self, skills_dir: str = None):
        import tempfile
        # Default to a safe temp directory if not provided, avoiding hardcoded /tmp for cross-platform compatibility
        self.skills_dir = skills_dir if skills_dir else os.path.join(tempfile.gettempdir(), "skills", "skills")

    def search_skills(self, query: str, limit: int = 3) -> str:
        """Search the skills directory for files matching the query and return their contents."""
        if not os.path.exists(self.skills_dir):
            return ""

        matched_skills = []
        try:
            # We will just do a simple keyword search over directory names
            keywords = query.lower().split()
            for item in os.listdir(self.skills_dir):
                item_path = os.path.join(self.skills_dir, item)
                if os.path.isdir(item_path):
                    # Check if any keyword matches the folder name
                    if any(kw in item.lower() for kw in keywords):
                        # Look for a README.md or .md file inside
                        for file in os.listdir(item_path):
                            if file.endswith(".md"):
                                try:
                                    with open(os.path.join(item_path, file), "r", encoding="utf-8") as f:
                                        content = f.read()
                                        matched_skills.append(f"--- Skill: {item} ---\n{content[:1000]}...\n") # Truncate for context limit
                                except Exception:
                                    pass
                        if len(matched_skills) >= limit:
                            break
                elif item.endswith(".md"): # Handle case where skills are directly in root as files
                    if any(kw in item.lower() for kw in keywords):
                        try:
                            with open(item_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                matched_skills.append(f"--- Skill: {item} ---\n{content[:1000]}...\n")
                        except Exception:
                            pass
                        if len(matched_skills) >= limit:
                            break
        except Exception as e:
            print(f"Error loading skills: {e}")

        if matched_skills:
            return "Active Skills (Antigravity):\n" + "\n".join(matched_skills)
        return ""

skill_manager = SkillManager()
