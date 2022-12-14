## Documentação

#### Objetivo geral

###### Este painel foi desenvolvido com a intenção de aprimorar minhas habilidades pessoais/profissionais com as ferramentas PowerBI e Python, utilizando dados reais e respondendo a algumas perguntas de negócios sobre o setor escolhido, permitindo uma melhor experiência com tratamento de dados, regras de setor e possibilidade de validação real dos resultados.

#
#### Sobre

###### O painel apresenta um overview do mercado segurador no Brasil a partir de dados obtidos junto à SUSEP. A SUSEP é entidade reguladora do mercado de seguros, abragendo a supervisão dos ramos relacionados à seguros, além de previdência e capitalização.

#
#### Perguntas de negócios

###### As questões abaixo foram definidas para direcionar a execução desse projeto na ferramenta de BI:
###### 1) Como é a evolução de prêmios e sinistros nesse mercado em visões anuais e YTD, permitindo filtragem;
###### 2) Quais os principais players (grupos econômicos) do mercado (mkt share, prêmios);
###### 3) Quais os principais ramos do mercado segurador em tamanho de prêmios;
###### 4) Quais ramos possuem relação de custos elevadas e o tamanho de mercado do ramo em questão a partir da visão prêmios.

#
#### Definições básicas de termos sobre o mercado segurador 

###### Prêmios = valores pagos à seguradora pelos clientes referente a suas apólices de seguros.
###### Sinistros = valores de sinistros pagos pela seguradora aos clientes quando há ocorrência do risco que foi segurado na apólice.
###### Despesas comerciais = valores gastos pelas companhias para comercialização de seguros. (ex.: pagamento de comissão aos corretores de seguros, intermediários que fazem a venda efetiva de alguns tipos de seguro)
###### Sinistralidade = é um indicador que mostra a relação entre os valores gastos em sinistros e o valor em prêmios ganhos. (sinistros ocorridos/prêmios ganhos)

#
#### Dados e tratamento

> Fonte de dados
###### A fonte primária de dados é a base do SES disponível no site da SUSEP [aqui](http://www2.susep.gov.br/menuestatistica/ses/principal.aspx)
###### Trata-se de uma base compactada em um arquivo .zip com diversos arquivos .csv. A documentação explicando cada coluna de cada arquivo se encontra no mesmo site também.
###### Os dados possuem um histórico longo, mas a partir de 2014 houve mudança no conceito de prêmios, então o período escolhido para o painel foi a partir de 2014. Os dados estão atualizados até 08/2022, última data disponível enquanto a criação do painel foi realizada. Uma vez que houver atualização, o processo está estruturado para tratar os dados automaticamente e a documentação permite a memória de ajustes necessários que estiverem fora do processo automático.

> Modelagem dos dados
###### A partir da documentação e visualização das tabelas, foi possível identificar na estrutura a possibilidade de montar um modelo star schema diretamente, uma vez que há um arquivo com os valores de prêmios e sinistros geral chamado Ses_seguros.csv, sendo uma tabela fato com as chaves necessárias para trazer as demais informações de outras tabelas como ramos, nome das cias ou divisão geográfica (Não utilizada aqui). No entanto, houve a necessidade de tratar ramos e cias, então todo o tratamento foi feito diretamente em Python e automatizado para gerar uma base final tratada e com todos os joins necessários. Essa base única tratada é upada no PowerBI para alimentar o painel.
###### Simplificação visual das tabelas abaixo:
![Estrutura tabelas - Simplificação visual](https://user-images.githubusercontent.com/116302387/203181986-75b11e1b-56cf-47b6-8c68-b1b2d834aeb4.PNG)

> Tratamento dos dados
###### O tratamento dos dados principal consiste em fazer o join entre a base principal e as bases de ramos e nomes da companhias para posteriormente ajustá-los. O processo está disponível no arquivo susep.py nesta mesma pasta e comentado. Além disso, alguns outros detalhes como renomear colunas, ajustar datas e limpar colunas desnecessárias também estão nesta parte do processo.
###### Os tratamentos de ramos e cias exigiram partes manuais e consultas à circulares da SUSEP para definir o melhor caminho e estão relatados abaixo.

##### Sobre ramos:
###### Os ramos disponíveis para fazer join com a base principal está disponível na base Ses_ramos.csv.
###### Trata-se de uma base com nível de agregação de ramos detalhado, sem agrupamento macro. Para agrupamento macro, foi (e é sempre) necessário atualizar de acordo com a última codificação atualizada e publicada em circular da SUSEP disponível [aqui](https://www.gov.br/susep/pt-br/documentos-e-publicacoes/normativos/pasta-de-normas-em-consulta-publica/consultas-publicas-passadas)
###### Neste projeto, foi utilizada essa última consulta pública (A tabela com a codificação proposta está ao final do arquivo)
[cp-no-13-quadro-de-sugestoes.xlsx](https://github.com/mssunaga/projetos-powerbi/files/10048271/cp-no-13-quadro-de-sugestoes.xlsx)
###### Resultado na coluna 'grupo', exemplo abaixo:
![Ramos macro](https://user-images.githubusercontent.com/116302387/203199155-40aeb5ab-aa12-4787-9cd1-ca7dd308db53.PNG)


##### Sobre grupos econômicos (companhias):
###### A tabela de grupos econômicos precisou de 2 ajustes;
###### 1) Correção de espaços gerados por caracteres que excederam a célula, por exemplo: 
![Correção GEs](https://user-images.githubusercontent.com/116302387/203184327-1833aa5f-2996-44e5-9adf-c21d2cadcfa1.PNG)

###### 2) Agrupamento das companhias, por exemplo: 
![Agrupamento GEs](https://user-images.githubusercontent.com/116302387/203198912-62f533a7-8e4b-42df-a528-4b14610add15.PNG)

> Estruturação no PowerBI - Passos básicos e essenciais
###### O primeiro passo foi a criação da tabela calendário.
Calendario = 
ADDCOLUMNS(
    CALENDARAUTO(),
    "ano", YEAR([Date]),
    "mês", MONTH([Date]),
    "nome_mes", FORMAT([Date],"mmmm")
)
###### Para criação dos gráficos de evolução de prêmios e sinistros, foram necessárias algumas medidas para o funcionamento da proposta de ter barras com os valores do ano e YTD variável.
###### Exemplos abaixo em relação aos valores de prêmios (mesma lógica aplicada para valores de sinistros)
###### Para manter o ano fixo, temos a medida: 
total_premio_fixo = CALCULATE(SUM(base_susep_geral[premio_emitido2]),ALL(Calendario[Date].[Mês])) 
###### Para calcular a linha de variação percentual, temos a medida: 
crescimento_premios = 
VAR premiolastyear =
    CALCULATE([total_premio],DATEADD(Calendario[Date],-1,YEAR))
RETURN
    DIVIDE([total_premio]-premiolastyear,premiolastyear)

###### Para criação dos textos variáveis, foram criadas medidas simples de identificação de maior e menor mês para aplicar em medidas de texto concatenando os textos + as medidas de maior e menor, respondendo às filtragens do relatório.

###### Para criação do box de informação com a lógica de abrir e fechar, foi utilizada a técnica de indicadores e seleção.


#### Visualização final do painel em vídeo
###### Vídeo comprimido em clideo.com para adequar ao documento.
https://user-images.githubusercontent.com/116302387/202878040-da34e735-4a33-4ab2-9a53-09770cfe33e4.mp4


#### Algumas validações dos valores gerados

##### Validação de prêmios e sinistros com a SUSEP:
###### Valores no painel para dois anos em tabela:
![Premios e Sinistro - Tabela painel](https://user-images.githubusercontent.com/116302387/205057060-6a00accf-e78e-4e67-a51f-07e2879b5f53.PNG)
###### Valores na consulta no SES SUSEP [aqui](https://www2.susep.gov.br/menuestatistica/SES/premiosesinistros.aspx?id=54):
![Ses - Premios e Sinistros](https://user-images.githubusercontent.com/116302387/205057304-a3c892e7-96b0-451c-9807-9ffe9a9c8026.PNG)

##### Validação pela receita da Porto Seguro no ramo de Automóvel (fácilmente identificável e comparável):
###### Ano fechado de 2021, de acordo com a apresentação institucional no site de RI da cia, pg.10 [aqui](https://api.mziq.com/mzfilemanager/v2/d/b77a3922-d280-4451-b3ee-0afec4577834/f7aae034-ca90-fb3d-7f58-d149b61735f1?origin=1)

###### Painel:
![Receita porto](https://user-images.githubusercontent.com/116302387/205058809-90a8cbc4-1bf2-4e78-bef4-83cf8f9ab138.PNG)
###### Apresentação institicional Porto Seguro - RI:
![Receita porto RI](https://user-images.githubusercontent.com/116302387/205058903-84b858b6-d935-486f-99a2-b2e1b1005521.PNG)





