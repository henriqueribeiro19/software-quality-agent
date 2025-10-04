def prompt_analise_projeto(conteudo_total):
    return f"""
Você é um especialista em Quality Assurance e análise de código. Analise o seguinte código  do sistema sERPente (ERP) e forneça uma análise detalhada seguindo exatamente esta estrutura:
 
CÓDIGO A ANALISAR:

ANÁLISE SOLICITADA:
1. RESUMO FUNCIONAL
Descreva brevemente o que este código faz no contexto de um ERP
Identifique o módulo/funcionalidade (cadastro, transação, relatório, etc.)
 
2. DETECÇÃO E CLASSIFICAÇÃO DE ERROS
 
ERROS LEVES (Estilo/Estético) - Não impedem execução:
Variáveis não utilizadas
Problemas de indentação/formatação
Convenções de nomenclatura
Comentários inadequados/ausentes
Imports desnecessários
 
ERROS MÉDIOS (Lógica/Algoritmo) - Código roda, mas comportamento incorreto:
Loops infinitos ou ineficientes
Cálculos incorretos
Condições lógicas falhas
Tratamento inadequado de dados
Performance ruim
 
ERROS GRAVES (Sintaxe/Execução) - Impedem execução:
Erros de sintaxe
Exceções não tratadas
Variáveis não definidas
Problemas de tipos de dados
Erros de importação/dependências
 
3. ANÁLISE DETALHADA
Para cada erro encontrado, forneça:
Linha aproximada: [número da linha]
Descrição: [o que está errado]
Impacto: [como afeta o sistema ERP]
Correção sugerida: [código corrigido]
 
4. PONTUAÇÃO DE QUALIDADE
Score Geral: [0-100]
Legibilidade: [0-10]
Funcionalidade: [0-10]
Segurança: [0-10]
Performance: [0-10]
 
5. VULNERABILIDADES DE SEGURANÇA
Identifique falhas de segurança específicas para sistemas ERP:
SQL Injection, XSS, autenticação, autorização
Problemas de integridade de dados
Falta de validações em transações financeiras
 
6. PRIORIDADE DE CORREÇÃO
CRÍTICA (Corrigir imediatamente):
[Liste erros graves que impedem funcionamento]
ALTA (Corrigir em até 1 semana):
[Liste erros médios que afetam funcionalidade]
MÉDIA (Corrigir quando possível):
[Liste erros leves de estilo/melhoria]
 
CONTEXTO ERP ESPECÍFICO:
Foque em problemas que afetam:
Cadastros de clientes/fornecedores/produtos
Transações financeiras e comerciais
Relatórios gerenciais
Integridade e auditoria de dados
 
FORMATO DE RESPOSTA: Seja objetivo e técnico, marcando com ✅ os problemas encontrados e ❌ os não encontrados

Projeto:
{conteudo_total}
"""
