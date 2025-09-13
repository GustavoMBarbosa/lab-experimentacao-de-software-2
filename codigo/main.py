import requests
import csv
from datetime import datetime, timezone
import time
import os
import subprocess
import sys
import glob

# ==============================
# Configurações
# ==============================
TOKEN = ""  # Coloque aqui seu token do GitHub
URL = "https://api.github.com/graphql"
HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
CLONE_DIR = "repositorios"
CSV_OUTPUT = "arquivos/repositorios_java.csv"
CK_JAR = "codigo/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Query GraphQL para buscar repositórios Java ordenados por estrelas
query = """
query ($cursor: String) {
  search(query: "language:Java sort:stars-desc", type: REPOSITORY, first: 20, after: $cursor) {
    nodes {
      ... on Repository {
        name
        url
        owner { login }
        stargazerCount
        createdAt
        updatedAt
        primaryLanguage { name }
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

# ==============================
# Utilitários para parsing do CSV do CK (robusto)
# ==============================
def _find_column(header_list, substrings):
    """Encontra a primeira coluna cujo nome contém alguma das substrings (case-insensitive)."""
    if not header_list:
        return None
    lowered = [h.lower() for h in header_list]
    for sub in substrings:
        for idx, h in enumerate(lowered):
            if sub in h:
                return header_list[idx]  # retorna o nome original do cabeçalho
    return None

def _to_float_safe(value):
    try:
        if value is None or value == "":
            return 0.0
        # remove espaços e troca vírgula por ponto se houver
        s = str(value).strip().replace(",", ".")
        return float(s)
    except Exception:
        return 0.0

# ==============================
# Coleta de repositórios
# ==============================
def fetch_repositories(max_repos=1000):
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
            time.sleep(1)

        except Exception as e:
            print(f"Erro na requisição: {e}")
            print("Tentando novamente em 10 segundos...")
            time.sleep(10)

    return all_repos[:max_repos]

# ==============================
# Clonar repositórios
# ==============================
def clone_repository(repo_url, repo_name):
    os.makedirs(CLONE_DIR, exist_ok=True)
    repo_path = os.path.join(CLONE_DIR, repo_name)

    if os.path.exists(repo_path):
        print(f"Repositório {repo_name} já existe, pulando clone.")
        return repo_path

    try:
        print(f"Clonando {repo_name}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return repo_path
    except Exception as e:
        print(f"Erro ao clonar {repo_name}: {e}")
        return None

# ==============================
# Executar CK
# ==============================
def run_ck(repo_path):
    """
    Executa o CK e retorna métricas resumidas (LOC, Comentarios, CBO, DIT, LCOM).
    """
    try:
        if not os.path.exists(CK_JAR):
            print(f"Arquivo {CK_JAR} não encontrado.")
            return None

        output_dir = repo_path  # CK já salva no próprio repo

        # roda o CK
        subprocess.run(
            ["java", "-jar", CK_JAR, repo_path, "true", "0", "false", output_dir],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Tenta achar o arquivo *class.csv dentro da pasta
        class_files = glob.glob(os.path.join(output_dir, "*class.csv"))

        # Se não achou, tenta o formato "repositorios/<nome>class.csv"
        if not class_files:
            repo_name = os.path.basename(repo_path)
            alt_path = os.path.join(CLONE_DIR, repo_name + "class.csv")
            if os.path.exists(alt_path):
                class_files = [alt_path]

        if not class_files:
            print(f"Nenhum arquivo *class.csv encontrado para {repo_path}")
            return None

        ck_class_file = class_files[0]

        # lê o class.csv
        with open(ck_class_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            if not headers:
                print(f"{ck_class_file} sem cabeçalho")
                return None

            loc_col = _find_column(headers, ["loc", "lines", "nloc"])
            comments_col = _find_column(headers, ["comment", "comments", "loccomment"])
            cbo_col = _find_column(headers, ["cbo"])
            dit_col = _find_column(headers, ["dit"])
            lcom_col = _find_column(headers, ["lcom"])

            loc_total = comments_total = cbo_total = dit_total = lcom_total = 0.0
            count = 0

            for row in reader:
                loc_total += _to_float_safe(row.get(loc_col))
                comments_total += _to_float_safe(row.get(comments_col))
                cbo_total += _to_float_safe(row.get(cbo_col))
                dit_total += _to_float_safe(row.get(dit_col))
                lcom_total += _to_float_safe(row.get(lcom_col))
                count += 1

            if count == 0:
                return None

            return (
                loc_total / count,
                comments_total / count,
                cbo_total / count,
                dit_total / count,
                lcom_total / count,
            )

    except Exception as e:
        print(f"Erro ao executar CK em {repo_path}: {e}")
        return None


# ==============================
# Salvar em CSV
# ==============================
def save_to_csv(repos, filename=CSV_OUTPUT):
    now = datetime.now(timezone.utc)

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Owner", "Name", "Stars",
            "IdadeAnos", "Releases",
            "LOC", "Comentarios", "CBO", "DIT", "LCOM"
        ])

        for i, r in enumerate(repos):
            created_at = datetime.fromisoformat(r["createdAt"].replace("Z", "+00:00"))
            idade_meses = (now.year - created_at.year) * 12 + (now.month - created_at.month)
            idade_anos = idade_meses / 12

            # Agora roda o clone e CK em TODOS os repositórios
            repo_path = clone_repository(r["url"], r["name"])
            if not repo_path:
                loc = comments = cbo = dit = lcom = "CLONE_ERROR"
            else:
                metrics = run_ck(repo_path)
                if metrics:
                    loc, comments, cbo, dit, lcom = metrics
                else:
                    loc = comments = cbo = dit = lcom = "CK_ERROR"

            # formata valores para escrita
            def _fmt(x):
                if x is None:
                    return ""
                if isinstance(x, (float, int)):
                    return f"{x:.2f}"
                return str(x)

            writer.writerow([
                r["owner"]["login"],
                r["name"],
                r.get("stargazerCount", ""),
                f"{idade_anos:.2f}",
                r.get("releases", {}).get("totalCount", 0),
                _fmt(loc),
                _fmt(comments),
                _fmt(cbo),
                _fmt(dit),
                _fmt(lcom)
            ])

def extrair_metricas_ck(repo_path):
    class_files = glob.glob(os.path.join(repo_path + "*class.csv"))
    method_files = glob.glob(os.path.join(repo_path + "*method.csv"))
    if not class_files:
        return "CK_ERROR", "CK_ERROR", "CK_ERROR", "CK_ERROR"

    class_csv = class_files[0]

    locs, cbos, dits, lcoms = [], [], [], []
    with open(class_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                locs.append(int(row.get("loc", 0)))
                cbos.append(int(row.get("cbo", 0)))
                dits.append(int(row.get("dit", 0)))
                lcoms.append(float(row.get("lcom", 0)))
            except Exception:
                continue

    if not locs:  
        return "CK_ERROR", "CK_ERROR", "CK_ERROR", "CK_ERROR"

    return (
        sum(locs),                              # LOC total
        round(sum(cbos) / len(cbos), 2),        # CBO médio
        round(sum(dits) / len(dits), 2),        # DIT médio
        round(sum(lcoms) / len(lcoms), 2)       # LCOM médio
    )




# ==============================
# Main
# ==============================
def main():
    # checagens iniciais
    if not TOKEN:
        print(" Atenção: você precisa preencher o TOKEN do GitHub para rodar a coleta.")
        return

    if not os.path.exists(CK_JAR):
        print(f" O arquivo JAR do CK não foi encontrado: {CK_JAR}")
        print("Coloque o jar do CK no mesmo diretório do script ou ajuste a variável CK_JAR.")
        return

    print("Iniciando coleta dos 1000 repositórios Java mais populares no GitHub...")
    repos = fetch_repositories(1000)
    print(f"Coleta finalizada! Total de repositórios coletados: {len(repos)}")

    print("Salvando dados em CSV...")
    save_to_csv(repos)
    print(f"Arquivo '{CSV_OUTPUT}' salvo com sucesso.")

if __name__ == "__main__":
    main()
