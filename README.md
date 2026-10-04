# SCRAPPER DO DIÁRIO OFICIAL

Criei esse scrapper pois estou aguardando um retorno de uma restituição de um órgão público e a melhor forma de saber em primeira mão sobre as atualizações, além dos e-mails e consultando os devidos sites do órgão, é via Diário Oficial.

A busca é simples, rodar o programa com o comando:
```bash
python main.py <dias> 
```

O <dias> é só substituir pelo número de dias para trás que deseja pesquisar. 

Se houver alguma menção ao termo pesquisado, subirá o alerta e poderemos consultar diretamente no Diário Oficial para pegar mais detalhes.

Para mudar os termos pesquisados, criar um arquivo .env com a estrutura abaixo:

```
TERMO="FULANO DA SILVA"
```

Você pode adicionar o nome, um CPF, ou protocolo por exemplo.

Obs.: Nomes normalmente devem ser escritos sem acentuação, assim como CPF sem pontos ou traços.
