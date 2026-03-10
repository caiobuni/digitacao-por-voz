# Verbatim Windows Dictation App Implementation Plan

## Goal Description

The goal is to develop "Verbatim", a Windows background application that sits in the system tray and starts up with Windows. 
When the user holds **Ctrl + Espaço**, the application will record the user's speech. Upon releasing the keys, the recorded audio is sent to Groq's Whisper V3 API to be transcribed. 
The transcription is configured with a prompt to ensure words are written correctly and sentences are well-punctuated, without forcing a highly formal language tone. 
The resulting text is then automatically placed into the system clipboard and pasted wherever the cursor currently is. We will also maintain a log file of all transcriptions (with date/time), accessible via the system tray icon.

## User Review Required

> [!IMPORTANT]
> **Hotkey combination**: You requested `Ctrl + Fn`. A tecla `Fn` é gerida a nível de hardware e não envia sinal direto ao Windows. Mudamos para `Ctrl + Espaço`. We will use the `pynput` library to capture this. Se ainda preferir outro atalho, é perfeitamente possível ajustar.

> [!WARNING]
> **Real-time Typing vs Edit-in-Place**: O Wispr Flow usa edição dinâmica na tela (enviando "Backspaces" ou deletando palavras para reescrever com o novo contexto). Isso é ***muito complexo e propenso a falhas*** no Windows, pois depende do aplicativo em que você está digitando responder perfeitamente aos Backspaces.
>
> Em vez disso, a API do Groq (Whisper V3) não suporta "streaming" palavra por palavra nativamente. 
> A solução viável e segura que propomos para atender ao seu pedido de "frase em frase":
> **Voice Activity Detection (VAD)**: Enquanto você segura `Shift + \`, se o sistema detectar uma pequena pausa na sua fala (ex: 0.5s ou 1s), ele envia o áudio capturado até ali, transcreve, e digita a frase pronta com pontuação perfeita. Ele continua gravando a próxima frase e repete o processo. Isso elimina a necessidade de enviar comandos de apagar (Backspace).

> [!NOTE]
> **Groq prompt**: We will use a system prompt or context prompt for Whisper along the lines of: *"Transcreva o áudio corrigindo pontuação e palavras incorretas, mantendo o tom natural da fala."* 
> 
> **Startup behavior**: To make it start with Windows, we will add an automatic script to place a shortcut in the Windows Startup folder or modify the Registry. 

## Proposed Changes

We will create a Python project structure in `c:\projetos_opencode\verbatim` with the following key files:

### Application Core

#### [NEW] main.py
The entry point of the application. It will initialize the global hotkey listener, the audio recorder, the Groq API handler, and the system tray icon. It will manage the threading required to run the tray icon and the listener concurrently.

#### [NEW] recorder.py
Handles the audio recording using `sounddevice` and `soundfile` in combination with `webrtcvad` or a simple volume threshold to detect speech pauses (Silence Detection).
- Starts a continuous stream while the hotkey is held.
- Yields completed phrases (audio buffers) whenever a silence threshold is met.

#### [NEW] transcriber.py
Handles the interaction with the Groq API.
- Accepts audio buffers from `recorder.py` in real-time or near real-time.
- Sends the audio data to `whisper-large-v3`.
- Returns the transcribed text immediately.

#### [NEW] typer.py
Handles text output.
- Takes the transcribed text, copies it to the clipboard using `pyperclip`.
- Simulates the `Ctrl+V` keypress to paste the text at the active cursor using `pynput` keyboard controller.

#### [NEW] logger.py
Handles saving the transcription logs.
- Appends date, time, and the transcribed text to a `transcriptions.md` file.
- Provides a function to open this file in the default text editor.

#### [NEW] tray.py
Handles the system tray icon using `pystray` and `Pillow`.
- Shows an icon.
- Provides a context menu with options: "Abrir Histórico" (Open Log) and "Sair" (Quit).
- Triggers the application termination cleanly when Quit is selected.

#### [NEW] startup.py
A utility to register the application with Windows Startup (e.g., creating a `.vbs` or adding a registry key so it runs hidden on boot).

### Dependencies

#### [NEW] requirements.txt
Will include: `sounddevice`, `soundfile`, `numpy`, `groq`, `pynput`, `pystray`, `pyperclip`, `Pillow`, `python-dotenv`.

## Verification Plan

### Automated Tests
- We will test the audio capture module to ensure it records audio of sufficient length and quality without truncating.
- We will test the Groq API connection and prompt formatting.

### Manual Verification
- We will manually test holding `Shift + \` to record speech and verify that releasing the keys triggers transcription and pasting into an open text editor.
- Check if the icon appears in the tray and "Open Log" opens the correct file.
- Check Windows Startup functionality after a mock restart or by executing the startup registration script manually.
