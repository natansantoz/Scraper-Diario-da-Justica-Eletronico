## Scraper Que Faz O Download dos [Diáriosda Justiça Eletrônico](http://www.stf.jus.br/portal/diariojusticaeletronico/pesquisardiarioeletronico.asp) do Dia Especificado


A solução é um conjunto de funções que recebe uma data e fazem o download dos diários daquele dia.

- Para isso, por meio de requisições GET:

  - É obtido o HTML da página correspondente a data;
  - São extraídas as urls referentes aos respectivos PDF's;
  - É feito o download dos PDF's;
  - É retornada uma lista com os hashs MD5 dos nomes dos PDF's.


# ![Gif-Execucao](https://github.com/natansantoz/Scraper-Diario-da-Justica-Eletronico/blob/master/imagens/gif-updated.gif)
