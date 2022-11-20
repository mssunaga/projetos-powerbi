## Documentação

#### Objetivo geral

###### Este painel foi desenvolvido com a intenção de aprimorar minhas habilidades pessoais/profissionais com as ferramentas PowerBI e Python, utilizando dados reais e respondendo a algumas perguntas de negócios sobre o setor escolhido, permitindo uma melhor experiência com tratamento de dados, regras de setor e possibilidade de validação real dos resultados.
#
#### Sobre

###### Trata-se de um painel de dados com o overview do mercado segurador a partir de dados obtidos junto à SUSEP.
###### A SUSEP é entidade reguladora do mercado de seguros no Brasil, abragendo a supervisão dos ramos relacionados à seguros, além de previdência e capitalização. Para fins de simplificaçãp, uma vez que são operações diferentes, o painel é focado apenas nos ramos de seguros.
###### Ao final desse documento, haverá um vídeo básico explorando o painel pronto e as funcionalidades.
#
#### Perguntas de negócios

###### As questões abaixo foram definidas para direcionar a execução desse projeto na ferramenta de BI:
###### 1) Como é a evolução de prêmios e sinistros nesse mercado em visões anuais e YTD, permitindo filtragem;
###### 2) Quais os principais players (grupos econômicos) do mercado (mkt share, prêmios);
###### 3) Quais os principais ramos do mercado segurador em tamanho de prêmios;
###### 4) Quais ramos possuem relação de custos elevadas e seu tamanho em prêmios.
#
#### Definições de termos sobre o mercado segurador de forma amigável

###### Prêmios = valores pagos à seguradora pelos clientes referente a suas apólices de seguros
###### Sinistros = valores de sinistros pagos pela seguradora aos clientes quando há ocorrência do risco que foi segurado na apólice.
###### Despesas comerciais = valores gastos pelas companhias para comercialização de seguros (ex.: pagamento de comissão aos corretores de seguros, intermediários que fazem a venda efetiva de alguns tipos de seguro)
###### Sinistralidade = é um indicador que mostra a relação entre os valores gastos em sinistros e o valor em prêmios ganhos (sinistros ocorridos/prêmios ganhos)

#
#### Dados e tratamento

> Fonte de dados
###### A fonte primária de dados é a base do SES disponível no site da SUSEP [aqui](http://www2.susep.gov.br/menuestatistica/ses/principal.aspx)
###### Trata-se de uma base compactada em um arquivo .zip com diversos arquivos .csv. A documentação explicando cada coluna de cada arquivo se encontra no mesmo site também.

> Modelagem dos dados
###### A partir da documentação e visualização das tabelas, foi possível identificar a possibilidade de montar um modelo star schema em algum banco de dados ou até mesmo no PowerBI, uma vez que há um arquivo com os valores de prêmios e sinistros geral chamado Ses_seguros.csv, sendo uma tabela fato com as chaves necessárias para trazer as demais informações de outras tabelas como ramos, nome das cias ou divisão geográfica. No entanto, houve a necessidade de tratar ramos e cias, então todo o tratamento foi feito diretamente em Python e automatizado para gerar uma base final tratada e com todos os joins necessários. Essa base única tratada é upada no PowerBI para alimentar o painel.

> Tratamento dos dados
###### O tratamento dos dados principal consiste em fazer o join entre a base principal e as bases de ramos e nomes da companhias para posteriormente ajustá-los. O processo está disponível no arquivo susep.py nesta mesma pasta e comentado. Além disso, alguns outros detalhes como renomear colunas, ajustar datas e limpar colunas desnecessárias também estão nesta parte do processo.
###### Os tratamentos de ramos e cias exigiram partes manuais e consultas à circulares da SUSEP para definir o melhor caminho e estão relatados abaixo.

##### Sobre ramos:
###### Os ramos disponíveis para fazer join com a base principal está disponível na base Ses_ramos.csv.
###### Trata-se de uma base com nível de agregação de ramos detalhado, sem agrupamento macro. Para agrupamento macro, foi (e é sempre) necessário atualizar de acordo com a última codificação atualizada e publicada em circular da SUSEP disponível [aqui](https://www.gov.br/susep/pt-br/documentos-e-publicacoes/normativos/pasta-de-normas-em-consulta-publica/consultas-publicas-passadas)
###### Neste projeto, foi utilizada essa última consulta pública (A tabela com a codificação proposta está ao final do arquivo)
[cp-no-13-quadro-de-sugestoes.xlsx](https://github.com/mssunaga/projetos-powerbi/files/10048271/cp-no-13-quadro-de-sugestoes.xlsx)


#
#### Visualização do painel em vídeo

https://user-images.githubusercontent.com/116302387/202878040-da34e735-4a33-4ab2-9a53-09770cfe33e4.mp4




