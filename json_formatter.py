#!/usr/bin/env python3
"""
JSON Formatter
Formata arquivos JSON de forma padronizada sem alterar o conteúdo.
Uso: python json_formatter.py <arquivo.json>
Saída: <arquivo>1.json (formatado)
"""

import json
import sys
import os
from pathlib import Path


def format_json_file(input_path: str) -> str:
    """
    Formata um arquivo JSON e salva com sufixo '1'

    Args:
        input_path: Caminho do arquivo JSON de entrada

    Returns:
        Caminho do arquivo formatado
    """
    # Validar arquivo
    path = Path(input_path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")

    if not path.suffix.lower() == '.json':
        raise ValueError(f"O arquivo deve ter extensão .json")

    print(f"[INFO] Lendo: {path.name}")

    # Ler arquivo JSON
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        raise IOError(f"Erro ao ler arquivo: {e}")

    # Gerar nome de saída
    output_path = path.with_stem(path.stem + '1')
    print(f"[INFO] Salvando: {output_path.name}")

    # Salvar com formatação padronizada
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(
            data,
            f,
            indent=2,           # 2 espaços de indentação
            sort_keys=False,     # Manter ordem original das chaves
            ensure_ascii=False,  # Preservar caracteres Unicode (emojis, acentos)
            separators=(',', ': ')  # Separadores padrão com espaços
        )

    print(f"[OK] Arquivo formatado com sucesso!")
    print(f"[STATS] Estatísticas:")
    print(f"   Original: {path.stat().st_size:,} bytes")
    print(f"   Formatado: {output_path.stat().st_size:,} bytes")

    return str(output_path)


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("[ERROR] Uso: python json_formatter.py <arquivo.json>")
        print("        Ex: python json_formatter.py dados.json")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        format_json_file(input_file)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
