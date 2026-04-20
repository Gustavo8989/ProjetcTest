from winotify import Notification, audio

# Criar a notificação
toast = Notification(
    app_id="Meu Robô Python", title="Tarefa Concluída", msg="O script terminou de rodar com sucesso!", duration="short"
)
toast.set_audio(audio.Default, loop=False)
toast.show()
