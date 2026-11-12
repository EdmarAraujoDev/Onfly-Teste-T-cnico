# Relatório de Entrega — Consolidador de Reservas de Hotel

## 1. Objetivo

O projeto consiste em um sistema de linha de comando (CLI), desenvolvido em Python, para consolidar dados de reservas de hotéis e gerar um relatório no formato JSON.

Durante a análise e a execução dos testes, foram identificados e corrigidos problemas que afetavam os cálculos financeiros, a contabilização das reservas, a classificação dos hotéis e a leitura dos arquivos CSV.

## 2. Defeitos identificados e corrigidos

### 2.1. Conversão de moedas

**Causa raiz:** A lógica de conversão dos valores das reservas não aplicava corretamente as taxas de câmbio para calcular os valores em reais.

**Correção:** Ajuste da conversão monetária utilizando as taxas fornecidas no arquivo de câmbio.

### 2.2. Cálculo de diárias

**Causa raiz:** O cálculo das noites reservadas não considerava corretamente a diferença entre as datas de entrada e saída e a quantidade de quartos.

**Correção:** Adequação do cálculo para considerar a diferença em dias entre checkout e check-in, multiplicada pela quantidade de quartos.

### 2.3. Tratamento dos status das reservas

**Causa raiz:** Reservas com status diferente de `CONFIRMED` estavam sendo consideradas indevidamente nos valores faturáveis.

**Correção:** Somente reservas confirmadas passaram a ser consideradas nos cálculos financeiros, nas noites e nas agregações por mês e hotel. Reservas canceladas e no-show continuam contabilizadas nas quantidades gerais e em seus respectivos status.

### 2.4. Ordenação dos hotéis

**Causa raiz:** A classificação dos hotéis não respeitava a ordem decrescente do valor total faturado.

**Correção:** Ajuste da ordenação para apresentar os hotéis pelo maior valor total em reais, com desempate pelo `hotel_id` em ordem crescente.

### 2.5. Limite de leitura do CSV

**Causa raiz:** O repositório de reservas possuía um limite fixo de 200 registros, impedindo o processamento integral de arquivos maiores.

**Correção:** Remoção do limite fixo e inclusão de um teste adicional para verificar o processamento de 250 reservas.

## 3. Estratégia de investigação

A investigação foi realizada por meio da leitura da estrutura do projeto, análise das regras de negócio descritas no desafio, execução da aplicação pela linha de comando e execução dos testes automatizados.

Também foi utilizada uma amostra de validação para comparar os resultados gerados com os valores esperados na especificação.

## 4. Validação

### 4.1. Testes automatizados

Comando utilizado:

```bash
pytest -q
```

Resultado registrado: **6 testes aprovados**, sendo 5 testes originais do desafio e 1 teste adicional de regressão.

O teste adicional verifica se o sistema consegue processar mais de 200 reservas.

### 4.2. Validação da amostra

Comando utilizado:

```bash
PYTHONPATH=src python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json
```

Resultados obtidos:

- Total de reservas: 12
- Reservas confirmadas: 9
- Reservas canceladas: 2
- Reservas no-show: 1
- Total de noites: 28
- Total convertido: R$ 7.566,00
- Média por noite: R$ 270,21

Os resultados, incluindo as agregações mensais e a classificação dos cinco hotéis, foram conferidos com os valores esperados no desafio.

### 4.3. Validação do arquivo completo

Comando utilizado:

```bash
PYTHONPATH=src python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

Resultado registrado:

- Total de reservas: 300
- Reservas confirmadas: 235
- Total de noites: 1.347
- Total convertido: R$ 396.170,00

A execução demonstrou que o sistema processa o arquivo completo, sem interromper a leitura após 200 registros.

## 5. Integração contínua

Foi configurado um fluxo de integração contínua com GitHub Actions para executar os testes automatizados em Python 3.11.

O fluxo executa o `pytest -q` em atualizações de pull requests direcionados à branch principal.

## 6. Considerações finais

As correções foram realizadas preservando a interface de linha de comando, os argumentos de execução, o formato do relatório e os arquivos de dados fornecidos pelo desafio.

Os testes originais foram preservados, e foi adicionado um teste específico para prevenir o retorno do limite de 200 registros.

O projeto foi validado com a amostra fornecida e com o arquivo completo de reservas.
