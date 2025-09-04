import requests
import csv
from datetime import datetime, timezone
import time

# Configurações
TOKEN = "" # TOKEN GITHUB
URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Query GraphQL para buscar repositórios Java ordenados por estrelas
query = """
query ($cursor: String) {
  search(query: "language:Java sort:stars-desc", type: REPOSITORY, first: 20, after: $cursor) {
    nodes {
      ... on Repository {
        name
        owner { login }
        stargazerCount
        createdAt
        updatedAt
        primaryLanguage { name }
        issues { totalCount }
        closedIssues: issues(states: CLOSED) { totalCount }
        pullRequests(states: MERGED) { totalCount }
        releases { totalCount }
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
"""

def fetch_repositories(max_repos=1000):
    """
    Faz requisições paginadas à API GitHub GraphQL para coletar dados dos repositórios Java mais populares.
    """
    all_repos = []
    cursor = None

    while True:
        try:
            variables = {"cursor": cursor}
            response = requests.post(URL, json={"query": query, "variables": variables}, headers=HEADERS)

            if response.status_code != 200:
                raise Exception(f"Erro {response.status_code} ao buscar dados: {response.text}")

            data = response.json()
            if "errors" in data:
                raise Exception(f"Erro na resposta da API: {data['errors']}")

            repos_page = data["data"]["search"]
            all_repos.extend(repos_page["nodes"])

            print(f"Coletados {len(all_repos)} repositórios até agora...")

            if not repos_page["pageInfo"]["hasNextPage"] or len(all_repos) >= max_repos:
                break

            cursor = repos_page["pageInfo"]["endCursor"]
            time.sleep(1)  # evita saturar a API

        except Exception as e:
            print(f"Erro na requisição: {e}")
            print("Tentando novamente em 10 segundos...")
            time.sleep(10)

    return all_repos[:max_repos]

def save_to_csv(repos, filename="arquivos/repositorios_java.csv"):
    """
    Salva os dados coletados em um arquivo CSV.
    """
    now = datetime.now(timezone.utc)

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Owner", "Name", "Stars",
            "IdadeMeses", "PRsMes", "ReleasesMes",
            "DiasDesdeAtualizacao", "LinguagemPrincipal",
            "TotalIssues", "ClosedIssues", "PercentualIssuesFechadas"
        ])

        for r in repos:
            created_at = datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00"))
            idade_meses = (now.year - created_at.year) * 12 + (now.month - created_at.month)

            total_prs = r["pullRequests"]["totalCount"]
            prs_mes = total_prs / idade_meses if idade_meses > 0 else total_prs

            total_releases = r["releases"]["totalCount"]
            releases_mes = total_releases / idade_meses if idade_meses > 0 else total_releases

            updated_at = datetime.fromisoformat(r["updatedAt"].replace("Z", "+00:00"))
            delta_days = (now - updated_at).days

            linguagem = r["primaryLanguage"]["name"] if r["primaryLanguage"] else "N/A"

            total_issues = r["issues"]["totalCount"]
            closed_issues = r["closedIssues"]["totalCount"]
            pct_closed = (closed_issues / total_issues * 100) if total_issues > 0 else 0

            writer.writerow([
                r["owner"]["login"],
                r["name"],
                r["stargazerCount"],
                idade_meses,
                f"{prs_mes:.2f}",
                f"{releases_mes:.2f}",
                delta_days,
                linguagem,
                total_issues,
                closed_issues,
                f"{pct_closed:.2f}"
            ])

def main():
    print("Iniciando coleta dos 1000 repositórios Java mais populares no GitHub...")
    repos = fetch_repositories(10)
    print(f"Coleta finalizada! Total de repositórios coletados: {len(repos)}")

    print("Salvando dados em CSV...")
    save_to_csv(repos)
    print("Arquivo 'repositorios_java.csv' salvo com sucesso.")

if __name__ == "__main__":
    main()

    save_to_csv(repos)
    print("Arquivo 'repositorios_java.csv' salvo com sucesso.")

if __name__ == "__main__":
    main()
