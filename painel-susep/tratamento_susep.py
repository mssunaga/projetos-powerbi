##### Libraries
import pandas as pd
import numpy as np


###### Carregamento dos dados 
path = r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\BaseCompleta'

# Bases de seguros (Geral e por UF)
seguros = pd.read_csv(path+"\Ses_seguros.csv", sep=';', decimal=',')
ufs = pd.read_csv(path+"\SES_UF2.csv", sep=';', decimal=',', encoding='latin-1')

# Bases de apoios (Nome das cias/grupo economico e ramos * ramos ajustados manualmente com base na Susep para determinar oos grupos)
grp_eco = pd.read_csv(path+"\Ses_grupos_economicos.csv", sep=';', encoding='latin-1')
ramos = pd.read_csv(path+"\Ses_ramos.csv", sep=';', encoding='latin-1')



###### Tratando a base geral

# Filtrando datas (201001 em diante)
seguros2 = seguros.query("damesano > 201400")
seguros2.groupby(['damesano'])['coramo'].count()


# Base seguros + ramos
bd2 = pd.merge(seguros2, ramos, how='left', left_on=['coramo'], right_on=['coramo'])

# Check tamanho de ambos
bd2
seguros2.shape
# Check se tem algum valor nulo após o join no grupo
bd2['grupo'].isnull().sum()
bd2.groupby(['grupo'])['coenti'].count()


# Base uf com ramos + cias e grupo economico
bd4 = pd.merge(bd2, grp_eco, how='left', left_on=['coenti','damesano'], right_on=['coenti','damesano'])

# Check se tem algum valor nulo após o join no grupo
bd4.groupby(['noenti'])['coenti'].count()
bd4['nogrupo'].isnull().sum()
bd4

# Removendo blank space nos nomes das cias/grp_eco
bd4['nogrupo'] = bd4['nogrupo'].str.strip()
bd4['noenti'] = bd4['noenti'].str.strip()



# Aplicando condição: Se o grupo é independente ou outros grupos, retornar o nome da cia.
bd4['nme_grupo'] = np.where((bd4['nogrupo'] == 'INDEPENDENTE') | (bd4['nogrupo'] == 'OUTROS GRUPOS'),bd4['noenti'],bd4['nogrupo'])


# Depara feito na etapa de ufs para ajuste dos grupos economicos
depara = pd.read_excel(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\nomegrupos_ajustado.xlsx')


# Trazendo os grupos ajustados (depara feito nas etapa para a base de ufs)
bd6 = pd.merge(bd4, depara, how='left', left_on=['nme_grupo'], right_on=['nme_grupo'])
# Verificando se algum valor ficou nulo
bd6['nme_grupos_ajuste'].isnull().sum()



# Checando os valores nulos no join com o depara para tratar
tratar2 = bd6[bd6['nme_grupos_ajuste'].isnull()]
tratar2.to_excel(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\tratar2.xlsx')


# Ajustes de colunas
list(bd6.columns)

# Ajustes finais
# Ajuste de data para o powerbi
bd6['diamesano'] = bd6['damesano'].astype(str)
bd6['year'] = bd6['diamesano'].str.slice(stop=4).astype(np.int64)
bd6['month'] = bd6['diamesano'].str.slice(start=-2).astype(np.int64)
bd6['day'] = 1
bd6['data'] = pd.to_datetime(bd6[['day','month','year']])

bd6.head()

# Dropando colunas que não serão usadas e renomeando
listadrop = ['damesano','coenti_y','cogrupo_y','cod_concat','obs','nme_grupo',
'diamesano','day','month','year']

for d in listadrop:
  bd6.drop(d, axis=1, inplace=True)


# Renomeando algumas colunas
bd6 = bd6.rename(columns={"coenti_x": "coenti", "cogrupo_x": "cogrupo", "grupo": "ramos_grupos",
"nme_grupos_ajuste": "noenti_grupos_eco"})
bd6.head()

# Exportando .csv para usar no PowerBI
bd6.to_csv(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\base_susep_geral.csv', index=False)




################################################################################################################################




###### Tratamento para a base de UF (Não usado no painel)

# Filtrando datas (201001 em diante)
ufs2 = ufs.query("damesano > 201000")
ufs2.groupby(['damesano'])['ramos'].count()


# Joins das bases
# Base uf + ramos
bd1 = pd.merge(ufs2, ramos, how='left', left_on=['ramos'], right_on=['coramo'])
# Check tamanho de ambos
bd1
ufs2.shape
# Check se tem algum valor nulo após o join no grupo
bd1['grupo'].isnull().sum()
bd1.groupby(['grupo'])['coenti'].count()


# Base uf com ramos + cias e grupo economico
bd3 = pd.merge(bd1, grp_eco, how='left', left_on=['coenti','damesano'], right_on=['coenti','damesano'])


# Checando os valores nulos no join com grupo economico
# Valores tratados e ajustados no arquivo de grupos economicos, na próxima não ocorre valor nulo nesta etapa
tratar = bd3[bd3['nogrupo'].isnull()]
tratar.to_excel(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\tratar.xlsx')

# Check se tem algum valor nulo após o join no grupo
bd3.groupby(['noenti'])['coenti'].count()
bd3['nogrupo'].isnull().sum()
bd3

# Removendo blank space nos nomes das cias/grp_eco
bd3['nogrupo'] = bd3['nogrupo'].str.strip()
bd3['noenti'] = bd3['noenti'].str.strip()


# Tratamento nome das cias

# Aplicando condição: Se o grupo é independente ou outros grupos, retornar o nome da cia.
bd3['nme_grupo'] = np.where((bd3['nogrupo'] == 'INDEPENDENTE') | (bd3['nogrupo'] == 'OUTROS GRUPOS'),bd3['noenti'],bd3['nogrupo'])

# Gerando contagem dos campos para extrair, validar e agrupar corretamente casos em que 
# a cia aparecia multiplas vezes e estava dentro do grupo independepente/outros grupos
validar = bd3.groupby(['nme_grupo'])['coenti'].count()
validar.to_excel(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\nomegrupos.xlsx')

# Carregando após os ajustes
depara = pd.read_excel(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\nomegrupos_ajustado.xlsx')


# Trazendo os grupos ajustados
bd6 = pd.merge(bd3, depara, how='left', left_on=['nme_grupo'], right_on=['nme_grupo'])
# Verificando se algum valor ficou nulo
bd6['nme_grupos_ajuste'].isnull().sum()

# Ajustes de colunas
list(bd6.columns)

# Ajustes finais
# Ajuste de data para o powerbi
bd6['diamesano'] = bd6['damesano'].astype(str)
bd6['year'] = bd6['diamesano'].str.slice(stop=4).astype(np.int64)
bd6['month'] = bd6['diamesano'].str.slice(start=-2).astype(np.int64)
bd6['day'] = 1
bd6['data'] = pd.to_datetime(bd6[['day','month','year']])

bd6.head()

# Dropando colunas que não serão usadas e renomeando
listadrop = ['salvados','recuperacao','coenti_y','diamesano','obs']

for d in listadrop:
  bd6.drop(d, axis=1, inplace=True)


# Renomeando algumas colunas
bd6 = bd6.rename(columns={"coenti_x": "coenti", "nme_grupos_ajuste": "nme_cias_grupos"})
bd6

# Exportando .csv para usar no PowerBI
bd6.to_csv(r'C:\Users\marce\Documents\Power BI Desktop\00.Dashboard_Susep\base_susep_ufs.csv', index=False)
