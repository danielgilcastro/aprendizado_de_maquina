# Aula 2 — Exercício: Energia

Consulte também as [instruções da atividade](./exercicio-instrucoes.md).

## Identificação do grupo

- **Grupo:** [Digite o número ou nome do grupo]
- **Integrantes:** [Digite os nomes]
- **Data:** [Digite a data]

## Situação

Uma distribuidora de energia atende cerca de 2 milhões de clientes. A diretoria quer usar os dados que já possui para operar melhor: reduzir perdas, planejar a manutenção da rede e entender como as pessoas consomem.

## Dados disponíveis

- Leituras mensais de consumo por cliente nos últimos 5 anos. Quando o medidor não pode ser lido — portão fechado, cachorro ou morador ausente —, o sistema registra uma estimativa calculada a partir dos meses anteriores.
- Cadastro: tipo de ligação (residencial, comercial ou industrial), bairro e data de instalação.
- Histórico de interrupções de fornecimento por região.
- Registros de inspeção técnica, feitos quando houve suspeita de irregularidade.
- Chamados abertos na central de atendimento.

## Data frames de exemplo para análise

Os exemplos abaixo são dados fictícios, criados apenas para praticar as análises. Eles representam as informações disponíveis no cenário e podem ser executados em Python com `pandas`.

```python
import pandas as pd

# Cadastro dos clientes
clientes = pd.DataFrame({
	"cliente_id": [1001, 1002, 1003, 1004, 1005],
	"tipo_ligacao": ["residencial", "comercial", "industrial", "residencial", "comercial"],
	"bairro": ["Centro", "Jardins", "Distrito Industrial", "Centro", "Jardins"],
	"data_instalacao": pd.to_datetime([
		"2018-03-12", "2020-07-05", "2016-11-20", "2022-01-15", "2019-09-30"
	])
})

# Leituras mensais; medicao_estimada indica que o valor foi calculado pelo sistema
leituras = pd.DataFrame({
	"cliente_id": [1001, 1001, 1002, 1002, 1003, 1003, 1004, 1005],
	"mes": pd.to_datetime([
		"2024-01-01", "2024-02-01", "2024-01-01", "2024-02-01",
		"2024-01-01", "2024-02-01", "2024-02-01", "2024-02-01"
	]),
	"consumo_kwh": [210, 225, 980, 1020, 5400, 5100, 180, 760],
	"medicao_estimada": [False, True, False, False, True, False, False, True]
})

# Interrupções registradas por região
interrupcoes = pd.DataFrame({
	"regiao": ["Centro", "Jardins", "Distrito Industrial", "Centro", "Jardins"],
	"data": pd.to_datetime([
		"2024-01-08", "2024-01-12", "2024-01-15", "2024-02-03", "2024-02-10"
	]),
	"duracao_minutos": [35, 120, 45, 20, 90],
	"clientes_afetados": [320, 180, 75, 140, 210]
})

# Inspeções técnicas após suspeita de irregularidade
inspecoes = pd.DataFrame({
	"inspecao_id": [1, 2, 3, 4, 5],
	"cliente_id": [1001, 1002, 1003, 1004, 1005],
	"data_inspecao": pd.to_datetime([
		"2024-02-05", "2024-02-06", "2024-02-07", "2024-02-08", "2024-02-09"
	]),
	"irregularidade_confirmada": [False, False, True, False, True]
})

# Chamados registrados na central de atendimento
chamados = pd.DataFrame({
	"chamado_id": [501, 502, 503, 504, 505],
	"cliente_id": [1001, 1002, 1003, 1004, 1005],
	"data_abertura": pd.to_datetime([
		"2024-01-10", "2024-01-18", "2024-01-20", "2024-02-02", "2024-02-11"
	]),
	"categoria": ["leitura", "interrupcao", "leitura", "interrupcao", "faturamento"],
	"resolvido": [True, True, False, True, False]
})
```

### Exemplos de análises

```python
# Consumo médio por tipo de ligação
consumo_por_tipo = (leituras.merge(clientes, on="cliente_id")
					.groupby("tipo_ligacao", as_index=False)["consumo_kwh"]
					.mean())

# Clientes com leituras estimadas
clientes_com_estimativa = leituras[leituras["medicao_estimada"]]

# Total de interrupções e duração média por região
resumo_interrupcoes = (interrupcoes.groupby("regiao", as_index=False)
					   .agg(total_interrupcoes=("regiao", "size"),
							duracao_media_minutos=("duracao_minutos", "mean")))

# Perfil de consumo para agrupamento (aprendizado não supervisionado)
perfil_clientes = (leituras.groupby("cliente_id", as_index=False)
				   .agg(consumo_medio_kwh=("consumo_kwh", "mean"),
						quantidade_leituras_estimadas=("medicao_estimada", "sum")))
```

## Tarefa

Quais problemas podem ser resolvidos com aprendizado de máquina neste cenário?

Para cada problema, registre:

- o tipo do problema;
- o que o modelo devolveria;
- quais dados alimentariam o modelo.

Preencha no mínimo duas respostas: uma de aprendizado supervisionado e outra de aprendizado não supervisionado.

---

## Resposta 1 — problema supervisionado

### Problema ou pergunta

[Digite aqui o problema que o modelo deve resolver.]

### Tipo

- [ ] Supervisionado
- [ ] Não supervisionado

**Tarefa de aprendizado** (por exemplo: classificação ou regressão):  
[Digite aqui.]

### O que o modelo devolveria

[Descreva a saída do modelo: uma categoria, um número, uma probabilidade etc.]

### Quais dados alimentariam o modelo

[Liste apenas os dados disponíveis que seriam usados como entrada e, se houver, indique a variável-alvo.]

### Justificativa

[Explique brevemente por que esse tipo de aprendizado é adequado ao problema.]

---

## Resposta 2 — problema não supervisionado

### Problema ou pergunta

[Digite aqui o problema que o modelo deve resolver.]

### Tipo

- [ ] Supervisionado
- [ ] Não supervisionado

**Tarefa de aprendizado** (por exemplo: agrupamento ou detecção de anomalias):  
[Digite aqui.]

### O que o modelo devolveria

[Descreva a saída do modelo: grupos de clientes, casos atípicos, padrões etc.]

### Quais dados alimentariam o modelo

[Liste os dados disponíveis que seriam usados como entrada.]

### Justificativa

[Explique brevemente por que esse tipo de aprendizado é adequado ao problema.]

---

## Resposta adicional 1 — opcional

### Problema ou pergunta

[Digite aqui.]

### Tipo

- [ ] Supervisionado
- [ ] Não supervisionado

**Tarefa de aprendizado:** [Digite aqui.]  
**O que o modelo devolveria:** [Digite aqui.]  
**Quais dados alimentariam o modelo:** [Digite aqui.]  
**Justificativa:** [Digite aqui.]

---

## Resposta adicional 2 — opcional

### Problema ou pergunta

[Digite aqui.]

### Tipo

- [ ] Supervisionado
- [ ] Não supervisionado

**Tarefa de aprendizado:** [Digite aqui.]  
**O que o modelo devolveria:** [Digite aqui.]  
**Quais dados alimentariam o modelo:** [Digite aqui.]  
**Justificativa:** [Digite aqui.]

---

## Revisão final

- [ ] A Resposta 1 é um problema supervisionado e possui uma variável-alvo identificável.
- [ ] A Resposta 2 é um problema não supervisionado e não depende de rótulos prontos.
- [ ] As saídas dos modelos estão descritas de forma concreta.
- [ ] Todos os dados citados existem na lista fornecida.
- [ ] As escolhas foram justificadas.

---

*Conteúdo transcrito e adaptado de `exercicio.jpeg` para preenchimento digital.*















