class TOCParser:
    @staticmethod
    def parse_toc(toc_text):
        parsed_toc = {}
        lines = toc_text.split("\n")
        current_chapter = None
        current_section = None

        for line in lines:
            if "Chapter" in line:
                current_chapter = line.strip()
                parsed_toc[current_chapter] = {}
            elif "Section" in line:
                current_section = line.strip()
                parsed_toc[current_chapter][current_section] = []
            else:
                if current_section:  # Make sure we are inside a section
                    parsed_toc[current_chapter][current_section].append(line.strip())

        return parsed_toc
