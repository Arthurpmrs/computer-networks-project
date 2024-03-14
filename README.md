# Computer Networks Project

## Funcionalidades
### Aplicação Cliente
Essa aplicação pode se conectar a um servidor e pode:
- Obter a lista de arquivos do servidor
- Fazer download de um arquivo
- Fazer upload de um arquivo para o servidor

Portanto, a aplicação Client precisa ter:
- Cliente TCP para fazer requisições à aplicação Servidor (obter lista de arquivos, fazer download, fazer upload)
- Servidor TCP para receber o arquivo ao fazer download.

### Aplicação Servidor
Já a aplicação Servidor pode:
- Enviar a lista de arquivos disponíveis
- Receber um novo arquivo
- Enviar arquivos que forem requisitados por um host

Portanto, a aplicação Servidor precisa ter:
- Cliente TCP para enviar o arquivo requisitado
- Servidor TCP para receber as requsições de um host (envio de lista de arquivos, envio de arquivo)


Para facilitar, os arquivos disponíveis para download no lado do servidor estão numa pasta. Então, toda vez que a lista de arquivos for requisitada, serão enviadas os metadados dos arquivos dessa pasta.
