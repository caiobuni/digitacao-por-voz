# Verbatim App: Épicos e Histórias de Usuário

## Epic 1: Captura e Transcrição de Áudio
**Como** usuário, **quero** que o sistema grave minha voz e a transcreva com alta precisão **para que** eu não precise digitar o texto manualmente.

### Histórias:
- [ ] **STORY 1.1:** Gravação por Atalho. **Como** usuário, **quero** poder segurar `Ctrl + Espaço` para iniciar a gravação do meu microfone e soltar para parar, **para ter** controle exato de quando o sistema está me ouvindo.
- [ ] **STORY 1.2:** Transcrição via Groq Whisper. **Como** sistema, **preciso** enviar o áudio capturado para a API do Groq (Whisper V3) de forma rápida e segura (usando a `.env`), **para obter** o texto transcrito com a pontuação e ortografia corretas.
- [ ] **STORY 1.3:** Detecção de Silêncio (VAD). **Como** usuário, **quero** que se eu falar uma frase e fizer uma pausa, o sistema já envie essa frase para transcrição e digite na tela antes mesmo de eu soltar a tecla, **para** eu ver o texto aparecendo mais rapidamente (frase a frase).

## Epic 2: Inserção de Texto e Histórico
**Como** usuário, **quero** que o texto transcrito apareça magicamente onde eu estava digitando e fique salvo em um log **para que** eu tenha um registro do que ditei.

### Histórias:
- [ ] **STORY 2.1:** Digitação Automática. **Como** sistema, **preciso** colocar o texto transcrito na área de transferência e simular o comando `Ctrl+V` **para que** o texto apareça no campo de texto ativo (Word, Chrome, etc.).
- [ ] **STORY 2.2:** Restauração da Área de Transferência. **Como** usuário, **quero** que, após o sistema colar o texto transcrito, minha área de transferência original seja restaurada, **para não** perder o que eu havia copiado anteriormente.
- [ ] **STORY 2.3:** Log de Transcrições. **Como** usuário, **quero** que todas as transcrições sejam salvas em um arquivo Markdown (`transcriptions.md`) com data e hora.

## Epic 3: Interface em Segundo Plano e Inicialização
**Como** usuário, **quero** que o aplicativo rode discretamente no fundo e inicie com o Windows **para que** esteja sempre pronto para uso sem atrapalhar minha tela.

### Histórias:
- [ ] **STORY 3.1:** Ícone na Bandeja do Sistema (System Tray). **Como** usuário, **quero** ver um ícone do Verbatim perto do relógio do Windows.
- [ ] **STORY 3.2:** Menu de Contexto. **Como** usuário, **quero** clicar com o botão direito no ícone da bandeja e ter opções para "Abrir Histórico" e "Sair".
- [ ] **STORY 3.3:** Startup Script. **Como** usuário, **quero** que o app inicie junto com o Windows no modo Oculto (`.vbs`).
