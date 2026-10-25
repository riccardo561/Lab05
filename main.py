import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

# Per risolvere questo esercizio il professore ci ha detto di scaricare la versione di Flet 1.0.4


FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    text_tipo= ft.TextField(label='Tipo')
    text_marca= ft.TextField(label='Marca')
    text_anno= ft.TextField(label='Anno di acquisto')
    text_titolo=ft.Text('Aggiungi un nuovo strumento',size=16)
    contatore=ft.TextField(
        value=0,
        text_align=ft.TextAlign.CENTER,
        read_only=True,
        disabled=True,
        width=75
    )



    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()
    def aumenta_contatore(e):
            contatore.value+=1
            contatore.update()
    def diminuisci_contatore(e):
            contatore.value-=1
            contatore.update()
    def aggiunta_strumento(e):
        if (not text_tipo.value.strip()) or text_tipo.value.isdigit():
            alert.show_alert('Hai inserito un valore errato del tipo')
        elif (not text_marca.value.strip()) or text_marca.value.isdigit():
            alert.show_alert('Hai inserito un valore errato della marca')
        elif (not text_anno.value.strip().isdigit()) or int(text_anno.value) < 0 or int(text_anno.value) > 2026:
            alert.show_alert("Hai inserito un valore errato dell'anno")
        elif not contatore.value > 0:
            alert.show_alert("Hai inserito un valore errato del prezzo")
        else:
            strumento = deposito.aggiungi_strumento(text_tipo.value, text_marca.value, text_anno.value, contatore.value)
            text_tipo.value=''
            text_marca.value=''
            text_anno.value=''
            contatore.value = 0
            aggiorna_lista_strumenti()


    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    bottonplus = ft.Button(content='+', color=ft.Colors.GREEN, on_click=aumenta_contatore)
    bottonminus = ft.Button(content='-', color=ft.Colors.RED, on_click=diminuisci_contatore)
    row = ft.Row([text_tipo, text_marca, text_anno, bottonplus, contatore, bottonminus],
                 alignment=ft.MainAxisAlignment.CENTER)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    bottone = ft.Button(content='Aggiungi Strumento', on_click=aggiunta_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        text_titolo,
        row,
        bottone,
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()
ft.run(main)
