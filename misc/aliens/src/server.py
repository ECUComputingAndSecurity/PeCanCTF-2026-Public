import socketserver
import pathlib

GROUPS = {}

article_number = 1

for group_dir in sorted(pathlib.Path("articles").iterdir()):
    if not group_dir.is_dir():
        continue

    GROUPS[group_dir.name] = []

    for article_file in sorted(group_dir.glob("*.txt"), key=lambda p: int(p.stem)):
        content = article_file.read_text()

        message_id = f"<{article_number}@aliensare.real>"

        for line in content.splitlines():
            if line.lower().startswith("message-id:"):
                message_id = line.split(":", 1)[1].strip()
                break

        GROUPS[group_dir.name].append({
            "number": article_number,
            "message_id": message_id,
            "content": content,
        })

        article_number += 1


class NNTPHandler(socketserver.StreamRequestHandler):

    def send_line(self, text):
        self.wfile.write((text + "\r\n").encode())

    def get_article_by_number(self, group, number):
        for article in GROUPS[group]:
            if article["number"] == number:
                return article
        return None

    def handle(self):

        self.send_line("200 NNTP Service Ready (no posting)")

        current_group = None
        current_index = None

        while True:

            line = self.rfile.readline()

            if not line:
                break

            cmd = line.decode(errors="ignore").strip()

            if not cmd:
                continue

            parts = cmd.split()
            verb = parts[0].upper()

            # QUIT
            if verb == "QUIT":
                self.send_line("205 Goodbye")
                break

            # LIST
            elif verb == "LIST":

                self.send_line("215 list follows")

                for group_name, articles in GROUPS.items():

                    if articles:
                        first = articles[0]["number"]
                        last = articles[-1]["number"]
                    else:
                        first = 0
                        last = 0

                    self.send_line(
                        f"{group_name} {last} {first} y"
                    )

                self.send_line(".")

            # GROUP <name>
            elif verb == "GROUP":

                if len(parts) < 2:
                    self.send_line("411 No group specified")
                    continue

                group = parts[1]

                if group not in GROUPS:
                    self.send_line("411 No such group")
                    continue

                current_group = group

                articles = GROUPS[group]

                if articles:
                    current_index = 0
                    first = articles[0]["number"]
                    last = articles[-1]["number"]
                else:
                    current_index = None
                    first = 0
                    last = 0

                self.send_line(
                    f"211 {len(articles)} {first} {last} {group}"
                )

            # STAT
            elif verb == "STAT":

                if current_group is None:
                    self.send_line("412 No group selected")
                    continue

                if len(parts) == 1:

                    if current_index is None:
                        self.send_line("420 No current article")
                        continue

                    article = GROUPS[current_group][current_index]

                else:

                    try:
                        wanted = int(parts[1])
                    except ValueError:
                        self.send_line("423 Invalid article number")
                        continue

                    article = self.get_article_by_number(
                        current_group,
                        wanted
                    )

                    if article is None:
                        self.send_line("423 No such article")
                        continue

                    current_index = GROUPS[current_group].index(article)

                self.send_line(
                    f"223 {article['number']} {article['message_id']}"
                )

            # NEXT
            elif verb == "NEXT":

                if current_group is None:
                    self.send_line("412 No group selected")
                    continue

                if current_index is None:
                    self.send_line("420 No current article")
                    continue

                if current_index + 1 >= len(GROUPS[current_group]):
                    self.send_line("421 No next article")
                    continue

                current_index += 1

                article = GROUPS[current_group][current_index]

                self.send_line(
                    f"223 {article['number']} {article['message_id']}"
                )

            # LAST
            elif verb == "LAST":

                if current_group is None:
                    self.send_line("412 No group selected")
                    continue

                if current_index is None:
                    self.send_line("420 No current article")
                    continue

                if current_index == 0:
                    self.send_line("422 No previous article")
                    continue

                current_index -= 1

                article = GROUPS[current_group][current_index]

                self.send_line(
                    f"223 {article['number']} {article['message_id']}"
                )

            # ARTICLE or HEAD or BODY
            elif verb in ("ARTICLE", "HEAD", "BODY"):

                if current_group is None:
                    self.send_line("412 No group selected")
                    continue

                if len(parts) == 1:

                    if current_index is None:
                        self.send_line("420 No current article")
                        continue

                    article = GROUPS[current_group][current_index]

                else:

                    try:
                        wanted = int(parts[1])
                    except ValueError:
                        self.send_line("423 Invalid article number")
                        continue

                    article = self.get_article_by_number(
                        current_group,
                        wanted
                    )

                    if article is None:
                        self.send_line("423 No such article")
                        continue

                    current_index = GROUPS[current_group].index(article)

                headers, _, body = article["content"].partition("\n\n")

                if verb == "ARTICLE":
                    self.send_line(
                        f"220 {article['number']} {article['message_id']} article follows"
                    )

                    for l in article["content"].splitlines():
                        self.send_line(l)

                    self.send_line(".")

                elif verb == "HEAD":
                    self.send_line(
                        f"221 {article['number']} {article['message_id']} headers follow"
                    )

                    for l in headers.splitlines():
                        self.send_line(l)

                    self.send_line(".")

                elif verb == "BODY":
                    self.send_line(
                        f"222 {article['number']} {article['message_id']} body follows"
                    )

                    for l in body.splitlines():
                        self.send_line(l)

                    self.send_line(".")

            elif verb == "HELP":
                self.send_line("LIST\r\nGROUP <name>\r\nARTICLE\r\nSTAT\r\nHEAD\r\nBODY\r\nNEXT\r\nLAST\r\nQUIT")
                self.send_line(".")

            else:
                self.send_line("500 Unknown command")


if __name__ == "__main__":

    server = socketserver.ThreadingTCPServer(
        ("0.0.0.0", 119),
        NNTPHandler,
    )

    print("NNTP listening on port 119")

    server.serve_forever()