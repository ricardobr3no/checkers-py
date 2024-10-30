import arcade
import arcade.gui

space = lambda height: arcade.gui.UISpace(height=height)


class Menu(arcade.View):
    def __init__(self):
        super().__init__()

        # Criar os botões
        label = arcade.gui.UILabel(text="MENU", font_size=32, font_name="comic sans MS")
        label_total_pieces = arcade.gui.UILabel(
            text=f"RED: {12}\nWHITE: {12}", font_size=24
        )
        restart_button = arcade.gui.UIFlatButton(text="Restart", width=200)
        quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        # logica dos botoes
        @restart_button.event("on_click")
        def on_click_restart(event):
            print("restart")
            arcade.get_window().setup()

        @quit_button.event("on_click")
        def on_click_quit(event):
            print("saindo...")
            arcade.close_window()

        # Organizar os botões em um layout vertical
        vertical_box = arcade.gui.UIBoxLayout()
        vertical_box.add(label)
        vertical_box.add(space(40))
        vertical_box.add(label_total_pieces)
        vertical_box.add(space(20))
        vertical_box.add(restart_button)
        vertical_box.add(space(20))
        vertical_box.add(quit_button)

        # Centralizar o layout na tela
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        self.ui_manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="right", align_x=-45, child=vertical_box)
        )

    def on_draw(self):
        self.ui_manager.draw()
