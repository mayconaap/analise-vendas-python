#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Projeto 1: Análise de Vendas Pessoais
Autor: Seu Nome
Descrição: Script para análise de um arquivo CSV de vendas
"""

import csv
from datetime import datetime
from collections import defaultdict
import os

def carregar_dados(nome_arquivo):
    """
    Função para carregar os dados do arquivo CSV
    Retorna uma lista de dicionários com os dados
    """
    dados = []
    try:
        with open(nome_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                # Convertendo tipos de dados
                linha['quantidade'] = int(linha['quantidade'])
                linha['preco_unitario'] = float(linha['preco_unitario'])
                dados.append(linha)
        print(f"✓ Dados carregados com sucesso! {len(dados)} registros encontrados.")
        return dados
    except FileNotFoundError:
        print(f"✗ Erro: Arquivo {nome_arquivo} não encontrado!")
        return None
    except Exception as e:
        print(f"✗ Erro inesperado: {e}")
        return None

def calcular_faturamento_total(dados):
    """
    Calcula o faturamento total de todas as vendas
    """
    total = 0
    for venda in dados:
        faturamento_venda = venda['quantidade'] * venda['preco_unitario']
        total += faturamento_venda
    return total

def produto_mais_vendido(dados):
    """
    Encontra o produto com maior quantidade vendida
    """
    vendas_por_produto = defaultdict(int)
    
    for venda in dados:
        produto = venda['produto']
        vendas_por_produto[produto] += venda['quantidade']
    
    # Encontrando o produto com maior quantidade
    produto_top = max(vendas_por_produto.items(), key=lambda x: x[1])
    return produto_top[0], produto_top[1]

def media_vendas_por_dia(dados):
    """
    Calcula a média de vendas (em R$) por dia
    """
    vendas_por_dia = defaultdict(float)
    
    for venda in dados:
        data = venda['data']
        faturamento = venda['quantidade'] * venda['preco_unitario']
        vendas_por_dia[data] += faturamento
    
    media = sum(vendas_por_dia.values()) / len(vendas_por_dia)
    return media, dict(vendas_por_dia)

def top_3_dias(dados):
    """
    Retorna os 3 dias com maior faturamento
    """
    faturamento_por_dia = defaultdict(float)
    
    for venda in dados:
        data = venda['data']
        faturamento = venda['quantidade'] * venda['preco_unitario']
        faturamento_por_dia[data] += faturamento
    
    # Ordenando do maior para o menor e pegando os 3 primeiros
    top_dias = sorted(faturamento_por_dia.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_dias

def gerar_relatorio(dados):
    """
    Gera um relatório completo com todas as análises
    """
    print("\n" + "="*50)
    print("📊 RELATÓRIO DE VENDAS".center(50))
    print("="*50)
    
    # Cabeçalho com data da análise
    data_analise = datetime.now().strftime("%d/%m/%Y %H:%M")
    print(f"Data da análise: {data_analise}")
    print("-"*50)
    
    # 1. Faturamento Total
    faturamento = calcular_faturamento_total(dados)
    print(f"\n💰 Faturamento Total: R$ {faturamento:,.2f}")
    
    # 2. Produto mais vendido
    produto, quantidade = produto_mais_vendido(dados)
    print(f"\n🏆 Produto mais vendido: {produto}")
    print(f"   Quantidade: {quantidade} unidades")
    
    # 3. Média de vendas por dia
    media, vendas_dia = media_vendas_por_dia(dados)
    print(f"\n📈 Média de vendas por dia: R$ {media:,.2f}")
    
    # 4. Top 3 dias com maior faturamento
    top_dias = top_3_dias(dados)
    print(f"\n🥇 Top 3 dias com maior faturamento:")
    for i, (dia, valor) in enumerate(top_dias, 1):
        print(f"   {i}. {dia}: R$ {valor:,.2f}")
    
    # 5. Resumo por produto
    print(f"\n📦 Resumo por produto:")
    resumo_produtos = defaultdict(lambda: {'quantidade': 0, 'faturamento': 0.0})
    
    for venda in dados:
        p = venda['produto']
        resumo_produtos[p]['quantidade'] += venda['quantidade']
        resumo_produtos[p]['faturamento'] += venda['quantidade'] * venda['preco_unitario']
    
    for produto, info in resumo_produtos.items():
        print(f"   • {produto}:")
        print(f"     - Quantidade: {info['quantidade']} unidades")
        print(f"     - Faturamento: R$ {info['faturamento']:,.2f}")
    
    print("\n" + "="*50)
    print("✅ FIM DO RELATÓRIO".center(50))
    print("="*50)

def main():
    """
    Função principal do programa
    """
    print("🔍 INICIANDO ANÁLISE DE VENDAS")
    print("-"*30)
    
    # Verifica se o arquivo existe no diretório atual
    arquivo = 'vendas.csv'
    
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado no diretório atual!")
        print(f"📁 Diretório atual: {os.getcwd()}")
        return
    
    # Carrega os dados
    dados = carregar_dados(arquivo)
    
    if dados:
        # Gera o relatório
        gerar_relatorio(dados)
        
        # Pergunta se quer salvar o relatório em um arquivo
        salvar = input("\n💾 Deseja salvar este relatório em um arquivo? (s/n): ")
        if salvar.lower() == 's':
            with open('relatorio_vendas.txt', 'w', encoding='utf-8') as f:
                # Redireciona a saída para o arquivo
                import sys
                stdout_original = sys.stdout
                sys.stdout = f
                gerar_relatorio(dados)
                sys.stdout = stdout_original
            print("✅ Relatório salvo como 'relatorio_vendas.txt'")
    else:
        print("❌ Não foi possível realizar a análise.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()